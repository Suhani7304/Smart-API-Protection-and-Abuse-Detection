from sqlalchemy import Column, Integer, String, DateTime, func
from datetime import datetime
from ..database import Base

# stores risk for each ip and system responds acc to that
class SessionRisk(Base):
    __tablename__ = "session_risk"

    session_id = Column(String(100), primary_key=True)
    ip_address = Column(String(45))
    risk_score = Column(Integer, default=0)
    last_updated = Column(DateTime, server_default=func.now(),
        onupdate=func.now(),
        nullable=False)
