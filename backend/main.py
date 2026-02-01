from fastapi import FastAPI, Request, Response
from database import engine, Base
import models
from middleware.request_logger import request_logger_middleware
from middleware.rate_limiter import rate_limiter_middleware
from middleware.flow_validator import flow_validator_middleware
from middleware.session_manager import session_middleware
from middleware.timing_engine import timing_engine_middleware
from middleware.response_engine import response_engine_middleware

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.middleware("http")
async def session_handler(request: Request, call_next):
    return await session_middleware(request, call_next)

@app.middleware("http")
async def rate_limit(request: Request, call_next):
    return await rate_limiter_middleware(request, call_next)

@app.middleware("http")
async def flow_check(request: Request, call_next):
    return await flow_validator_middleware(request, call_next)

@app.middleware("http")
async def timing_engine(request: Request, call_next):
    return await timing_engine_middleware(request, call_next)

@app.middleware("http")
async def response_engine(request: Request, call_next):
    return await response_engine_middleware(request, call_next)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    return await request_logger_middleware(request, call_next)

@app.get("/")
def index():
    return {"message": "Welcome to Smart Ticket Booking"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/search")
def search():
    return {"message": "Search trains"}

@app.get("/select-seat")
def select_seat():
    return {"message": "Seat selected"}

@app.get("/confirm")
def confirm():
    return {"message": "Booking confirmed"}

@app.get("/pay")
def pay():
    return {"message": "Payment successful"}
