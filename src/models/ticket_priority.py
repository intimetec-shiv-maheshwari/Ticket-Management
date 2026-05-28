from sqlalchemy import Column, Integer, String;
from sqlalchemy.orm import relationship;

from src.utils.db import Base;


class TicketPriority(Base):
    __tablename__ = "TicketPriority";
    id = Column(Integer, primary_key=True, autoincrement=False);
    label = Column(String, unique=True, nullable=False, index=True);

    tickets = relationship("Ticket", back_populates="priority_ref");
