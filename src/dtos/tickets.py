from datetime import datetime;
from typing import Literal;

from pydantic import BaseModel, ConfigDict, Field, field_serializer;

from src.utils.helpers import format_utc_datetime;

TicketStatus = Literal["open", "in_progress", "resolved", "closed"];
TicketPriority = Literal["low", "medium", "high", "critical"];


class TicketCreateDTO(BaseModel):
    user_id: str = Field(min_length=16, max_length=16);
    subject: str;
    description: str;
    organization_id: str = Field(min_length=16, max_length=16);
    status: TicketStatus = "open";
    priority: TicketPriority = "medium";
    assigned_to_id: str | None = Field(default=None, min_length=16, max_length=16);
    category: str;


class TicketDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True);

    id: str = Field(min_length=16, max_length=16);
    user_id: str = Field(min_length=16, max_length=16);
    subject: str;
    description: str;
    organization_id: str = Field(min_length=16, max_length=16);
    status: TicketStatus;
    priority: TicketPriority;
    assigned_to_id: str | None = Field(default=None, min_length=16, max_length=16);
    category: str;
    created_at: datetime;
    updated_at: datetime;

    @field_serializer("created_at", "updated_at")
    def serialize_utc_timestamps(self, value: datetime) -> str:
        return format_utc_datetime(value);
