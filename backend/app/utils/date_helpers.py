"""
Date Helper Utilities

Converts frontend date range strings (like "7d", "28d", "90d")
into start_date/end_date strings that the GA4 Data API understands.

GA4 Date API accepts:
  - Relative dates: "today", "yesterday", "NdaysAgo"
  - Absolute dates: "YYYY-MM-DD"
"""

from datetime import datetime, timedelta


def get_date_range(date_range: str) -> tuple[str, str]:
    """
    Convert a date range shorthand to (start_date, end_date) tuple.
    
    Args:
        date_range: One of "today", "yesterday", "7d", "28d", "90d", "12m"
    
    Returns:
        Tuple of (start_date, end_date) in GA4 format
    """
    today = datetime.now()
    
    range_map = {
        "today": ("today", "today"),
        "yesterday": ("yesterday", "yesterday"),
        "7d": ("7daysAgo", "today"),
        "28d": ("28daysAgo", "today"),
        "90d": ("90daysAgo", "today"),
        "12m": ("365daysAgo", "today"),
    }
    
    if date_range in range_map:
        return range_map[date_range]
    
    # Default to last 28 days
    return ("28daysAgo", "today")


def format_duration(seconds: float) -> str:
    """
    Convert seconds to human-readable duration string.
    
    Args:
        seconds: Duration in seconds
    
    Returns:
        Formatted string like "4m 32s"
    """
    if seconds < 0:
        return "0s"
    
    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)
    
    if minutes > 0:
        return f"{minutes}m {remaining_seconds}s"
    return f"{remaining_seconds}s"
