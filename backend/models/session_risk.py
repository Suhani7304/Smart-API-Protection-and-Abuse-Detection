from sqlalchemy import Column, Integer, String, DateTime, func
from datetime import datetime
from database import Base

class SessionRisk(Base):
    __tablename__ = "session_risk"

    session_id = Column(String, primary_key=True)
    ip_address = Column(String)
    risk_score = Column(Integer, default=0)
    last_updated = Column(DateTime, server_default=func.now(),
        onupdate=func.now(),
        nullable=False)
