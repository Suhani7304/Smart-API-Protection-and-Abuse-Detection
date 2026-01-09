# 🚆 Smart API Protection & Abuse Detection System

A **production-inspired FastAPI backend security system** designed to protect APIs from **abuse, bot attacks, and excessive automated requests**.  
This project simulates how real-world platforms like **train ticket booking systems, e-commerce flash sales, and payment gateways** secure their critical APIs.

---

## 📌 Why This Project Exists

Modern APIs face serious challenges:
- Bots booking all tickets instantly
- Brute-force and flooding attacks
- Abuse of critical endpoints like booking & payments
- No visibility into abnormal user behavior

### Example Problem
When **train ticket booking opens**, bots can send hundreds of requests per second and book all tickets before real users get a chance.

👉 This project demonstrates **how such abuse can be detected and controlled**.

---

## 🎯 Project Objectives

- Prevent automated & abusive API access
- Protect high-value endpoints (e.g. `/book-ticket`)
- Track request behavior using sessions
- Log API activity for analysis & auditing
- Design scalable, real-world security middleware

---

## 🧠 Features Implemented (Current)

### 1️⃣ Rate Limiting Middleware
- Limits requests **per IP + endpoint**
- Sliding time-window algorithm
- Different rules for different APIs

**Example rules:**
| Endpoint | Limit |
|-------|------|
| `/health` | 30 requests / 60 sec |
| `/book-ticket` | 5 requests / 10 sec |

➡️ Prevents bots from flooding booking APIs.

---

### 2️⃣ Request Logging
Every API request logs:
- Client IP
- Endpoint
- HTTP method
- Status code
- Response time
- User agent
- Session ID (if available)

This enables:
- Abuse detection
- Debugging
- Monitoring real traffic patterns

---

### 3️⃣ Session Management (Cookie-Based)
- Unique session IDs generated using UUID
- Stored securely as HTTP-only cookies
- Persists across requests within the browser

Helps in:
- Tracking repeat abusive behavior
- Differentiating real users from bots

---

### 4️⃣ Session Activity Database Model
Each user action is recorded with:
- Session ID
- IP address
- Action performed
- Timestamp

This data can later be used for:
- Behavioral analysis
- Automated blocking
- ML-based abuse detection

---

## 🚆 Real-World Example: Train Ticket Booking

### Problem
- Bots try to book all seats instantly
- Genuine users fail despite being on time

### How This System Helps
- Strict rate limiting on `/book-ticket`
- Session-based tracking
- Automatic throttling using HTTP 429 responses

---

## 🛠️ Tech Stack

### Backend
- **Python**
- **FastAPI**
- **Uvicorn (ASGI Server)**

### Database
- **MySQL**
- **SQLAlchemy ORM**

### Security Concepts Used
- Middleware-based request interception
- Sliding window rate limiting
- Session tracking via cookies
- Abuse detection patterns

### Tools
- Git & GitHub
- Swagger UI (OpenAPI)

---

