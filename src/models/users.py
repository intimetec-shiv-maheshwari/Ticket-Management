import secrets;

from sqlalchemy import Boolean, Column, ForeignKey, String;
from sqlalchemy.orm import relationship;

from src.utils.db import Base;


def generate_user_id() -> str:
    return secrets.token_hex(8);


class Users(Base):
    __tablename__ = "User";
    id = Column(String(16), primary_key=True, default=generate_user_id);
    name = Column(String, index=True, nullable=False);
    email = Column(String, unique=True, index=True, nullable=False);
    password = Column(String, nullable=False);
    organization_id = Column(
        String(16),
        ForeignKey("Organization.id"),
        nullable=False,
        index=True,
    );
    active = Column(Boolean, default=True);
    role_id = Column(String(16), ForeignKey("Role.id"), nullable=False, index=True);
    role = relationship("Roles", backref="users");
    organization = relationship("Organization", backref="users");
