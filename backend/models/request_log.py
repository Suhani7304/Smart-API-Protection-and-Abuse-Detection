from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from datetime import datetime 
from database import Base

class APIRequestLog(Base):
    __tablename__ = "api_requests"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String(45))
    method = Column(String(10))
    endpoint = Column(String(255))
    user_agent = Column(Text) #text does not have fix max length
    api_key = Column(String(100))
    session_id = Column(String(100))
    status_code = Column(Integer)
    response_time_ms = Column(Float)
