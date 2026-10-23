from datetime import datetime
from typing import Dict, Any
import zoneinfo
from pydantic import BaseModel, Field, field_validator


class DateTimeInput(BaseModel):
    timezone: str = Field(default="UTC", description="IANA timezone name, e.g., 'Asia/Kolkata' or 'UTC'")

    @field_validator("timezone")
    @classmethod
    def validate_timezone(cls, v: str) -> str:
        if not v or not isinstance(v, str):
            raise ValueError("Timezone must be a non-empty string.")
        tz_name = v.strip()
        try:
            zoneinfo.ZoneInfo(tz_name)
        except Exception:
            raise ValueError(f"Invalid IANA timezone identifier: '{v}'. Example valid timezones: 'UTC', 'Asia/Kolkata', 'America/New_York'")
        return tz_name


def get_current_datetime(timezone: str = "UTC") -> Dict[str, Any]:
    """
    Returns the current ISO formatted date and time for a given valid IANA timezone.
    """
    try:
        validated = DateTimeInput(timezone=timezone)
    except Exception as e:
        return {"error": str(e), "success": False}

    try:
        tz = zoneinfo.ZoneInfo(validated.timezone)
        now = datetime.now(tz)
        return {
            "datetime": now.isoformat(),
            "timezone": validated.timezone,
            "success": True
        }
    except Exception as e:
        return {"error": f"Failed to retrieve datetime for timezone '{timezone}': {str(e)}", "success": False}