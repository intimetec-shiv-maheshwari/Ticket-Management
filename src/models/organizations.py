import secrets;
from sqlalchemy import Boolean, Column, String;
from sqlalchemy.orm import relationship;

from src.utils.db import Base;


def generate_organization_id() -> str:
    return secrets.token_hex(8);


class Organization(Base):
    __tablename__ = "Organization";
    id = Column[str](String(16), primary_key=True, default=generate_organization_id);
    name = Column[str](String, index=True);
    description = Column[str](String);
    country = Column[str](String, index=True);
    active = Column[Boolean](Boolean, default=True);
    roles = relationship("Roles", back_populates="organization");


