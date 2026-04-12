from sqlalchemy import Column, Integer, String, Float, DateTime, func
from datetime import datetime
from ..database import Base

# it stores the time taken between diff requests
class TimingMetrics(Base):
    __tablename__ = "timing_metrics"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(128), index=True)
    action = Column(String(50))
    delta_ms = Column(Float)
    risk_score = Column(Integer)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
