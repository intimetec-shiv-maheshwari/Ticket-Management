from datetime import datetime, timezone

UTC_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"


def utc_now() -> datetime:
    """Current UTC time with no sub-second precision."""
    return datetime.now(timezone.utc).replace(microsecond=0)


def format_utc_datetime(value: datetime) -> str:
    """Format a datetime as UTC string: 2026-05-25T18:11:40."""
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    else:
        value = value.astimezone(timezone.utc)
    return value.replace(microsecond=0).strftime(UTC_DATETIME_FORMAT)
