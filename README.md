# Kiambu eCitizen

A streamlined payment portal for Kiambu County services, enabling citizens to pay for services like business permits, market fees, and water bills via M-Pesa.

## Features
- Pay for county services (business permits, market fees, etc.)
- M-Pesa integration (mock STK push)
- User management (create/fetch users by phone)
- Tracks applications & payments

## Tech Stack
- **Backend**: FastAPI + SQLAlchemy (SQLite)
- **Frontend**: Streamlit
- **Payments**: Mock M-Pesa STK push

## Setup
1. Clone repo
2. cd backend
3. uv venv
4. source .venv/bin/activate
5. uv pip install -r requirements.txt
6. uvicorn main:app --reload --port 8001

### In another terminal
1. cd frontend
2. uv venv
3. source .venv/bin/activate
4. uv pip install -r requirements.txt
5. streamlit run frontend.py

## Endpoints
- `POST /users`: Create/get user
- `GET /services`: List services
- `POST /applications`: Apply for service
- `POST /payments/stk`: Send mock M-Pesa STK

## Notes
- Uses SQLite for simplicity. Replace with Postgres in prod.
- M-Pesa integration is mocked. Use real Daraja API in prod.