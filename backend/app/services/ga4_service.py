"""
Google Analytics 4 Data API Service

This is the core analytics service that communicates with the
GA4 Data API using Service Account authentication.

Supports two authentication methods:
  1. JSON key file (local development)
  2. JSON string in environment variable (production/Render)

API Reference: https://developers.google.com/analytics/devguides/reporting/data/v1
"""

import os
import json
import logging
from pathlib import Path
from typing import Optional

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    RunReportRequest,
    DateRange,
    Dimension,
    Metric,
    OrderBy,
)
from google.oauth2 import service_account

from app.config.settings import settings
from app.utils.date_helpers import get_date_range, format_duration
from app.schemas.analytics import (
    AnalyticsOverview,
    TrafficDataPoint,
    DeviceData,
    TopPageData,
)

logger = logging.getLogger(__name__)

# ============================================
# Device category → color mapping
# ============================================
DEVICE_COLORS = {
    "desktop": "#4f8cff",
    "mobile": "#a855f7",
    "tablet": "#22d3ee",
    "smart tv": "#34d399",
    "other": "#fb923c",
}


class GA4Service:
    """
    Service class for querying GA4 Data API.
    
    Usage:
        service = GA4Service()
        overview = service.get_overview("28d")
    """

    def __init__(self):
        """Initialize the GA4 Data API client with credentials."""
        self.property_id = settings.GA4_PROPERTY_ID
        self.client: Optional[BetaAnalyticsDataClient] = None
        self._realtime_cache = None
        self._overview_cache = {}
        self._initialize_client()

    def _initialize_client(self):
        """
        Try to authenticate with GA4 using available credentials.
        Supports: OAuth token.json, local JSON file, or JSON string in env var.
        """
        try:
            credentials = None
            scopes = ["https://www.googleapis.com/auth/analytics.readonly"]

            # Method 1: OAuth token.json (User Consent Flow)
            token_path = Path(__file__).parent.parent.parent / "credentials" / "token.json"
            if token_path.exists():
                logger.info("Using OAuth2 credentials from token.json")
                from google.oauth2.credentials import Credentials
                credentials = Credentials.from_authorized_user_file(str(token_path), scopes)

            # Method 2: JSON credentials as environment variable string
            elif os.getenv("GA4_CREDENTIALS_JSON"):
                ga4_creds_json = os.getenv("GA4_CREDENTIALS_JSON")
                logger.info("Using GA4 credentials from environment variable")
                creds_dict = json.loads(ga4_creds_json)
                credentials = service_account.Credentials.from_service_account_info(
                    creds_dict,
                    scopes=scopes,
                )

            # Method 3: JSON key file path (local development)
            elif settings.GA4_CREDENTIALS_PATH:
                creds_path = Path(settings.GA4_CREDENTIALS_PATH)
                if creds_path.exists():
                    logger.info(f"Using GA4 credentials from file: {creds_path}")
                    credentials = service_account.Credentials.from_service_account_file(
                        str(creds_path),
                        scopes=scopes,
                    )
                else:
                    logger.warning(f"Credentials file not found: {creds_path}")

            if credentials:
                self.client = BetaAnalyticsDataClient(credentials=credentials)
                logger.info("✅ GA4 Data API client initialized successfully")
            else:
                logger.error(
                    "❌ No GA4 credentials found. "
                    "Set GA4_CREDENTIALS_JSON env var or place key file at GA4_CREDENTIALS_PATH"
                )

        except Exception as e:
            logger.error(f"❌ Failed to initialize GA4 client: {e}")
            self.client = None

    def _run_report(self, request: RunReportRequest):
        """Execute a GA4 report request with error handling."""
        if not self.client:
            raise ConnectionError("GA4 client not initialized. Check credentials.")
        
        if not self.property_id:
            raise ValueError("GA4_PROPERTY_ID not set in environment variables.")

        return self.client.run_report(request)

    # ============================================
    # Overview Metrics
    # ============================================
    def get_overview(self, date_range: str = "28d") -> AnalyticsOverview:
        """
        Get high-level analytics overview metrics.
        
        Returns: totalUsers, sessions, pageViews, bounceRate, etc.
        """
        import time

        # Check cache (valid for 1 hour)
        now = time.time()
        cache_key = f"overview_{date_range}"
        if cache_key in self._overview_cache:
            cache_entry = self._overview_cache[cache_key]
            if now - cache_entry["timestamp"] < 3600:
                logger.info(f"Serving overview API response for {date_range} from cache")
                return cache_entry["data"]

        start_date, end_date = get_date_range(date_range)

        request = RunReportRequest(
            property=f"properties/{self.property_id}",
            date_ranges=[
                # Current period
                DateRange(start_date=start_date, end_date=end_date),
            ],
            metrics=[
                Metric(name="totalUsers"),
                Metric(name="sessions"),
                Metric(name="screenPageViews"),
                Metric(name="bounceRate"),
                Metric(name="averageSessionDuration"),
                Metric(name="newUsers"),
            ],
        )

        response = self._run_report(request)

        if response.rows:
            row = response.rows[0]
            metrics = row.metric_values

            avg_duration = float(metrics[4].value) if metrics[4].value else 0

            result = AnalyticsOverview(
                totalUsers=int(metrics[0].value),
                totalSessions=int(metrics[1].value),
                pageViews=int(metrics[2].value),
                bounceRate=round(float(metrics[3].value) * 100, 1),
                avgSessionDuration=format_duration(avg_duration),
                newUsers=int(metrics[5].value),
                # Trends will be calculated when we add comparison periods
                usersTrend=0.0,
                sessionsTrend=0.0,
                pageViewsTrend=0.0,
                bounceTrend=0.0,
            )
            
            self._overview_cache[cache_key] = {
                "data": result,
                "timestamp": now
            }
            
            return result

        result_empty = AnalyticsOverview()
        self._overview_cache[cache_key] = {
            "data": result_empty,
            "timestamp": now
        }
        return result_empty

    # ============================================
    # Traffic Over Time
    # ============================================
    def get_traffic(self, date_range: str = "28d") -> list[TrafficDataPoint]:
        """
        Get daily traffic data for time-series charts.
        
        Returns: List of {date, users, sessions, pageViews} per day.
        """
        import time
        now = time.time()
        cache_key = f"traffic_{date_range}"
        if cache_key in self._overview_cache:
            cache_entry = self._overview_cache[cache_key]
            if now - cache_entry["timestamp"] < 3600:
                logger.info(f"Serving traffic API response for {date_range} from cache")
                return cache_entry["data"]

        start_date, end_date = get_date_range(date_range)

        request = RunReportRequest(
            property=f"properties/{self.property_id}",
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
            dimensions=[Dimension(name="date")],
            metrics=[
                Metric(name="totalUsers"),
                Metric(name="sessions"),
                Metric(name="screenPageViews"),
            ],
            order_bys=[
                OrderBy(
                    dimension=OrderBy.DimensionOrderBy(dimension_name="date"),
                    desc=False,
                )
            ],
        )

        response = self._run_report(request)
        data_points = []

        for row in response.rows:
            raw_date = row.dimension_values[0].value  # "20240115"
            # Format: YYYYMMDD → "Jan 15"
            try:
                from datetime import datetime
                dt = datetime.strptime(raw_date, "%Y%m%d")
                formatted_date = dt.strftime("%b %d")
            except ValueError:
                formatted_date = raw_date

            data_points.append(
                TrafficDataPoint(
                    date=formatted_date,
                    users=int(row.metric_values[0].value),
                    sessions=int(row.metric_values[1].value),
                    pageViews=int(row.metric_values[2].value),
                )
            )

        self._overview_cache[cache_key] = {
            "data": data_points,
            "timestamp": now
        }
        return data_points

    # ============================================
    # Device Breakdown
    # ============================================
    def get_devices(self, date_range: str = "28d") -> list[DeviceData]:
        """
        Get visitor breakdown by device category.
        
        Returns: List of {name, value (%), color} per device type.
        """
        import time
        now = time.time()
        cache_key = f"devices_{date_range}"
        if cache_key in self._overview_cache:
            cache_entry = self._overview_cache[cache_key]
            if now - cache_entry["timestamp"] < 3600:
                logger.info(f"Serving devices API response for {date_range} from cache")
                return cache_entry["data"]

        start_date, end_date = get_date_range(date_range)

        request = RunReportRequest(
            property=f"properties/{self.property_id}",
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
            dimensions=[Dimension(name="deviceCategory")],
            metrics=[Metric(name="totalUsers")],
        )

        response = self._run_report(request)

        # Calculate total for percentages
        total = sum(int(row.metric_values[0].value) for row in response.rows)
        if total == 0:
            result_empty = []
            self._overview_cache[cache_key] = {
                "data": result_empty,
                "timestamp": now
            }
            return result_empty

        devices = []
        for row in response.rows:
            device_name = row.dimension_values[0].value.lower()
            count = int(row.metric_values[0].value)
            percentage = round((count / total) * 100, 1)

            devices.append(
                DeviceData(
                    name=device_name.capitalize(),
                    value=percentage,
                    color=DEVICE_COLORS.get(device_name, "#64748b"),
                )
            )

        # Sort by percentage descending
        devices.sort(key=lambda d: d.value, reverse=True)
        
        self._overview_cache[cache_key] = {
            "data": devices,
            "timestamp": now
        }
        return devices

    # ============================================
    # Top Pages
    # ============================================
    def get_top_pages(self, date_range: str = "28d", limit: int = 10) -> list[TopPageData]:
        """
        Get most viewed pages.
        
        Returns: List of {page, views, avgTime} sorted by views.
        """
        import time
        now = time.time()
        cache_key = f"top_pages_{date_range}_{limit}"
        if cache_key in self._overview_cache:
            cache_entry = self._overview_cache[cache_key]
            if now - cache_entry["timestamp"] < 3600:
                logger.info(f"Serving top pages API response for {date_range} from cache")
                return cache_entry["data"]

        start_date, end_date = get_date_range(date_range)

        request = RunReportRequest(
            property=f"properties/{self.property_id}",
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
            dimensions=[Dimension(name="pagePath")],
            metrics=[
                Metric(name="screenPageViews"),
                Metric(name="averageSessionDuration"),
            ],
            order_bys=[
                OrderBy(
                    metric=OrderBy.MetricOrderBy(metric_name="screenPageViews"),
                    desc=True,
                )
            ],
            limit=limit,
        )

        response = self._run_report(request)
        pages = []

        for row in response.rows:
            avg_time = float(row.metric_values[1].value) if row.metric_values[1].value else 0

            pages.append(
                TopPageData(
                    page=row.dimension_values[0].value,
                    views=int(row.metric_values[0].value),
                    avgTime=format_duration(avg_time),
                )
            )

        self._overview_cache[cache_key] = {
            "data": pages,
            "timestamp": now
        }
        return pages

    # ============================================
    # Real-time Reporting
    # ============================================
    def get_realtime(self) -> dict:
        """
        Get near real-time analytics data (last 30 minutes).
        Returns active users, device category breakdown, top pages, and minute-by-minute traffic.
        """
        import time
        from google.analytics.data_v1beta.types import RunRealtimeReportRequest

        if not self.client:
            raise ConnectionError("GA4 client not initialized. Check credentials.")

        # Check in-memory cache (valid for 15 seconds)
        now = time.time()
        if self._realtime_cache and now - self._realtime_cache["timestamp"] < 15:
            logger.info("Serving realtime API response from cache")
            return self._realtime_cache["data"]

        # 1. Request KPI totals (activeUsers, screenPageViews, eventCount)
        total_request = RunRealtimeReportRequest(
            property=f"properties/{self.property_id}",
            metrics=[
                Metric(name="activeUsers"),
                Metric(name="screenPageViews"),
                Metric(name="eventCount")
            ]
        )
        total_response = self.client.run_realtime_report(total_request)
        
        active_users = 0
        page_views = 0
        event_count = 0
        
        if total_response.rows:
            metrics_values = total_response.rows[0].metric_values
            active_users = int(metrics_values[0].value) if len(metrics_values) > 0 and metrics_values[0].value else 0
            page_views = int(metrics_values[1].value) if len(metrics_values) > 1 and metrics_values[1].value else 0
            event_count = int(metrics_values[2].value) if len(metrics_values) > 2 and metrics_values[2].value else 0

        # 2. Request device breakdown in real-time
        device_request = RunRealtimeReportRequest(
            property=f"properties/{self.property_id}",
            metrics=[Metric(name="activeUsers")],
            dimensions=[Dimension(name="deviceCategory")],
        )
        device_response = self.client.run_realtime_report(device_request)
        devices = []
        for row in device_response.rows:
            count = int(row.metric_values[0].value)
            device = row.dimension_values[0].value.lower()
            devices.append({
                "name": device.capitalize(),
                "value": count,
                "color": DEVICE_COLORS.get(device, "#64748b")
            })

        # 3. Request top active pages in real-time
        page_request = RunRealtimeReportRequest(
            property=f"properties/{self.property_id}",
            metrics=[Metric(name="activeUsers")],
            dimensions=[Dimension(name="unifiedScreenName")],
            limit=5
        )
        page_response = self.client.run_realtime_report(page_request)
        active_pages = []
        for row in page_response.rows:
            active_pages.append({
                "page": row.dimension_values[0].value,
                "activeUsers": int(row.metric_values[0].value)
            })

        # 4. Request minute-by-minute timeline (last 30 minutes)
        timeline_request = RunRealtimeReportRequest(
            property=f"properties/{self.property_id}",
            metrics=[Metric(name="activeUsers"), Metric(name="screenPageViews")],
            dimensions=[Dimension(name="minutesAgo")],
        )
        timeline_response = self.client.run_realtime_report(timeline_request)
        
        timeline_dict = {i: {"users": 0, "pageViews": 0} for i in range(30)}
        for row in timeline_response.rows:
            try:
                min_ago = int(row.dimension_values[0].value)
                if 0 <= min_ago < 30:
                    timeline_dict[min_ago] = {
                        "users": int(row.metric_values[0].value),
                        "pageViews": int(row.metric_values[1].value)
                    }
            except (ValueError, IndexError):
                continue
                
        timeline = []
        for i in range(29, -1, -1):
            timeline.append({
                "date": f"{i}m ago" if i > 0 else "Now",
                "users": timeline_dict[i]["users"],
                "pageViews": timeline_dict[i]["pageViews"]
            })

        result = {
            "activeUsers": active_users,
            "pageViews": page_views,
            "eventCount": event_count,
            "avgEventsPerUser": round(event_count / active_users, 1) if active_users > 0 else 0.0,
            "devices": devices,
            "activePages": active_pages,
            "timeline": timeline
        }
        
        self._realtime_cache = {
            "data": result,
            "timestamp": now
        }
        
        return result

    # ============================================
    # Health Check
    # ============================================
    def is_connected(self) -> bool:
        """Check if GA4 client is properly initialized."""
        return self.client is not None and bool(self.property_id)


# ============================================
# Singleton instance
# ============================================
ga4_service = GA4Service()
