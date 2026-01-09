from fastapi import FastAPI, Request, Response
from middleware.request_logger import request_logger_middleware
from database import engine, Base
import models
from middleware.rate_limiter import rate_limiter_middleware
import uuid

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/start-session")
def start_session(request: Request, response: Response):
    session_id = request.cookies.get("session_id")
    if not session_id:
        session_id = str(uuid.uuid4())
        response.set_cookie(
            key="session_id",
            value=session_id,
            httponly=True,
            max_age=1800 #30min        
        )
    return {"session_id": session_id}

@app.middleware("http")
async def log_requests(request: Request, call_next):
    return await request_logger_middleware(request, call_next)

@app.middleware("http")
async def rate_limit(request: Request, call_next):
    return await rate_limiter_middleware(request, call_next)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/book-ticket")
def book_ticket():
    return {"message": "Ticket booking endpoint"}

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
