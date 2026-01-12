from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from database import Base

class TimingMetrics(Base):
    __tablename__ = "timing_metrics"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(128), index=True)
    action = Column(String(50))
    delta_ms = Column(Float)
    risk_score = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
