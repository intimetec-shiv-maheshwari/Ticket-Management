import secrets;

from sqlalchemy import Boolean, Column, ForeignKey, String;
from sqlalchemy.orm import relationship;

from src.utils.db import Base;


def generate_role_id() -> str:
    return secrets.token_hex(8);

class Roles(Base):
    __tablename__ = "Role";
    id = Column(String(16), primary_key=True, default=generate_role_id);
    name = Column(String, index=True, nullable=False);
    description = Column(String);
    organization_id = Column(String(16), ForeignKey("Organization.id"), nullable=False);
    organization = relationship("Organization", back_populates="roles");
    active = Column(Boolean, default=True);