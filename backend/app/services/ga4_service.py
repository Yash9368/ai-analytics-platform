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

            return AnalyticsOverview(
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

        return AnalyticsOverview()

    # ============================================
    # Traffic Over Time
    # ============================================
    def get_traffic(self, date_range: str = "28d") -> list[TrafficDataPoint]:
        """
        Get daily traffic data for time-series charts.
        
        Returns: List of {date, users, sessions, pageViews} per day.
        """
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

        return data_points

    # ============================================
    # Device Breakdown
    # ============================================
    def get_devices(self, date_range: str = "28d") -> list[DeviceData]:
        """
        Get visitor breakdown by device category.
        
        Returns: List of {name, value (%), color} per device type.
        """
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
            return []

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
        return devices

    # ============================================
    # Top Pages
    # ============================================
    def get_top_pages(self, date_range: str = "28d", limit: int = 10) -> list[TopPageData]:
        """
        Get most viewed pages.
        
        Returns: List of {page, views, avgTime} sorted by views.
        """
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

        return pages

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
