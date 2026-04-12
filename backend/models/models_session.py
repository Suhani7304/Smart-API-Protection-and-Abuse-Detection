from sqlalchemy import Column, Integer, String, DateTime, func
from datetime import datetime
from ..database import Base

# store session info
class SessionActivity(Base):
    __tablename__ = "session_activity"

    id = Column(Integer, primary_key=True)
    session_id = Column(String(100))
    ip_address = Column(String(45))
    action = Column(String(50))
    timestamp = Column(DateTime, server_default=func.now(), nullable=False)
