from datetime import date, datetime, timezone


def convert_datetime_to_iso_8601_with_z_suffix(dt: datetime) -> str:
    return dt.isoformat()


def transform_to_utc_datetime(dt: datetime) -> datetime:
    return datetime.fromisoformat(dt)
