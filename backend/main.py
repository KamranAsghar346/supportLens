import os
import time
import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, Depends, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy import func
from openai import OpenAI

from database import engine, get_db, Base
from models import Trace, CategoryEnum
from log_config import configure_logging, get_logger

configure_logging()
logger = get_logger("main")

# Process start time for uptime
_process_start_time = time.time()

# ---------------------------------------------------------------------------
# LLM availability
# ---------------------------------------------------------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


def _llm_available() -> bool:
    """True if LLM is configured and reachable."""
    return bool(OPENAI_API_KEY)


def _probe_llm() -> tuple[bool, str]:
    """Probe LLM provider. Returns (success, message)."""
    if not OPENAI_API_KEY or not _client:
        return False, "not_configured"
    try:
        _client.models.list()
        return True, "ok"
    except Exception as e:
        return False, str(e)[:100]


@asynccontextmanager
async def lifespan(application):
    """Startup: create tables, seed if empty. Shutdown: cleanup."""
    db = next(get_db())
    try:
        Base.metadata.create_all(bind=engine)
        count = db.query(func.count(Trace.id)).scalar()
        if count == 0:
            from seed import seed_database
            seed_database(db)
            logger.info("seeded_database", trace_count=22)
    finally:
        db.close()
    yield


app = FastAPI(title="SupportLens API", version="1.0.0", lifespan=lifespan)

# CORS — allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# LLM Prompts
# ---------------------------------------------------------------------------

CHATBOT_SYSTEM_PROMPT = """You are a friendly and professional customer support agent for BillEase, a SaaS billing and subscription management platform.

Your responsibilities:
- Help customers with billing questions, invoices, payment methods, and pricing
- Assist with refund requests and charge disputes
- Guide users through account access issues (login problems, password resets, MFA)
- Process cancellation and downgrade requests
- Answer general product questions

Guidelines:
- Be concise, empathetic, and helpful
- If you cannot resolve an issue, let the customer know you will escalate it
- Never share sensitive account details; ask the customer to verify their identity if needed
- Keep responses to 2-4 sentences"""

CLASSIFICATION_PROMPT = """You are a classification engine. Your task is to categorize a customer support conversation into exactly ONE of the following categories:

1. **Billing** — Questions about invoices, charges, payment methods, pricing, or subscription fees.
2. **Refund** — Requests to return a product, get money back, dispute a charge, or process a credit.
3. **Account Access** — Issues logging in, resetting passwords, locked accounts, or MFA/2FA problems.
4. **Cancellation** — Requests to cancel a subscription, downgrade a plan, or close an account.
5. **General Inquiry** — Anything that does not clearly fit the above categories: feature questions, product info, how-to questions, feedback, etc.

Rules:
- Return ONLY the category name, nothing else.
- If the conversation touches multiple categories, choose the PRIMARY intent of the customer's message.
- For example, if a customer asks about a billing charge AND requests a refund, classify as "Refund" because the refund is the actionable request.
- If a customer wants to cancel because of a billing issue, classify as "Cancellation" because that is the primary ask.

Customer message: {user_message}

Bot response: {bot_response}

Category:"""

# Valid category names for matching LLM output
VALID_CATEGORIES = {
    "billing": CategoryEnum.BILLING,
    "refund": CategoryEnum.REFUND,
    "account access": CategoryEnum.ACCOUNT_ACCESS,
    "cancellation": CategoryEnum.CANCELLATION,
    "general inquiry": CategoryEnum.GENERAL_INQUIRY,
}


def classify_trace(user_message: str, bot_response: str) -> CategoryEnum:
    """Classify a trace using the LLM, or GENERAL_INQUIRY if LLM unavailable."""
    if not _client:
        logger.warning("llm_classification_skipped", reason="no_api_key")
        return CategoryEnum.GENERAL_INQUIRY
    prompt = CLASSIFICATION_PROMPT.format(
        user_message=user_message, bot_response=bot_response
    )
    try:
        response = _client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=20,
        )
        raw = response.choices[0].message.content.strip().lower()
    except Exception as e:
        logger.warning("llm_classification_failed", error=str(e)[:200])
        return CategoryEnum.GENERAL_INQUIRY
    category = VALID_CATEGORIES.get(raw)
    if category is None:
        for key, val in VALID_CATEGORIES.items():
            if key in raw:
                return val
        logger.info("llm_unexpected_category", raw=raw)
        return CategoryEnum.GENERAL_INQUIRY
    return category


def generate_chat_response(user_message: str) -> tuple[str, int]:
    """Generate a chatbot response, or fallback message if LLM unavailable."""
    start = time.time()
    if not _client:
        elapsed_ms = int((time.time() - start) * 1000)
        return (
            "I'm currently unable to process your request. The LLM service is not configured. Please try again later or contact support.",
            elapsed_ms,
        )
    try:
        response = _client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": CHATBOT_SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            temperature=0.7,
            max_tokens=300,
        )
        elapsed_ms = int((time.time() - start) * 1000)
        return response.choices[0].message.content.strip(), elapsed_ms
    except Exception as e:
        elapsed_ms = int((time.time() - start) * 1000)
        logger.warning("llm_chat_failed", error=str(e)[:200])
        return (
            "I encountered an error processing your request. Please try again later.",
            elapsed_ms,
        )


# ---------------------------------------------------------------------------
# Pydantic schemas
# ---------------------------------------------------------------------------

class ChatRequest(BaseModel):
    user_message: str


class TraceCreate(BaseModel):
    user_message: str
    bot_response: str
    response_time_ms: int


class TraceResponse(BaseModel):
    id: str
    user_message: str
    bot_response: str
    category: str
    timestamp: datetime
    response_time_ms: int

    class Config:
        from_attributes = True


class CategoryStat(BaseModel):
    category: str
    count: int
    percentage: float


class AnalyticsResponse(BaseModel):
    total_traces: int
    categories: list[CategoryStat]
    average_response_time_ms: float


class HealthResponse(BaseModel):
    status: str  # "healthy" | "degraded" | "unhealthy"
    database: str  # "ok" | "error"
    llm: str  # "ok" | "not_configured" | "error"
    uptime_seconds: float
    message: Optional[str] = None


# ---------------------------------------------------------------------------
# Request logging middleware
# ---------------------------------------------------------------------------

@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())[:8]
    start = time.time()
    status_code = 500
    try:
        response = await call_next(request)
        status_code = response.status_code
        return response
    except Exception as e:
        logger.exception("request_failed", request_id=request_id, path=request.url.path, error=str(e))
        raise
    finally:
        # Skip logging for /health to avoid log flooding from orchestrator polls
        if request.url.path != "/health":
            duration_ms = round((time.time() - start) * 1000)
            logger.info(
                "request",
                request_id=request_id,
                method=request.method,
                path=request.url.path,
                status=status_code,
                duration_ms=duration_ms,
            )


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/health", response_model=HealthResponse)
def health(db: Session = Depends(get_db)):
    """
    Health check probing database and LLM.
    - healthy: DB ok, LLM ok or not_configured (read-only mode)
    - degraded: DB ok, LLM not_configured (chat/classification unavailable)
    - unhealthy: DB unreachable
    """
    uptime = round(time.time() - _process_start_time, 1)
    db_ok = False
    try:
        db.execute(text("SELECT 1"))
        db_ok = True
    except Exception as e:
        logger.warning("health_db_failed", error=str(e))
        return HealthResponse(
            status="unhealthy",
            database="error",
            llm="unknown",
            uptime_seconds=uptime,
            message=f"Database unreachable: {str(e)[:100]}",
        )
    llm_ok, llm_msg = _probe_llm()
    if not db_ok:
        return HealthResponse(
            status="unhealthy",
            database="error",
            llm=llm_msg,
            uptime_seconds=uptime,
        )
    if llm_msg == "not_configured":
        return HealthResponse(
            status="degraded",
            database="ok",
            llm="not_configured",
            uptime_seconds=uptime,
            message="Read-only mode: traces and analytics work; chat and classification require OPENAI_API_KEY",
        )
    if not llm_ok:
        return HealthResponse(
            status="degraded",
            database="ok",
            llm="error",
            uptime_seconds=uptime,
            message=f"LLM probe failed: {llm_msg}",
        )
    return HealthResponse(
        status="healthy",
        database="ok",
        llm="ok",
        uptime_seconds=uptime,
    )

@app.post("/chat", response_model=TraceResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Combined endpoint: generates a chatbot response, classifies the trace,
    saves it, and returns the full trace. This is what the frontend chatbot uses.
    """
    bot_response, response_time_ms = generate_chat_response(request.user_message)
    category = classify_trace(request.user_message, bot_response)

    trace = Trace(
        id=str(uuid.uuid4()),
        user_message=request.user_message,
        bot_response=bot_response,
        category=category,
        timestamp=datetime.now(timezone.utc),
        response_time_ms=response_time_ms,
    )
    db.add(trace)
    db.commit()
    db.refresh(trace)

    return TraceResponse(
        id=trace.id,
        user_message=trace.user_message,
        bot_response=trace.bot_response,
        category=trace.category.value,
        timestamp=trace.timestamp,
        response_time_ms=trace.response_time_ms,
    )


@app.post("/traces", response_model=TraceResponse)
def create_trace(trace_data: TraceCreate, db: Session = Depends(get_db)):
    """
    POST /traces — receives a trace (user message + bot response),
    classifies it via LLM, saves it, and returns it with classification.
    """
    category = classify_trace(trace_data.user_message, trace_data.bot_response)

    trace = Trace(
        id=str(uuid.uuid4()),
        user_message=trace_data.user_message,
        bot_response=trace_data.bot_response,
        category=category,
        timestamp=datetime.now(timezone.utc),
        response_time_ms=trace_data.response_time_ms,
    )
    db.add(trace)
    db.commit()
    db.refresh(trace)

    return TraceResponse(
        id=trace.id,
        user_message=trace.user_message,
        bot_response=trace.bot_response,
        category=trace.category.value,
        timestamp=trace.timestamp,
        response_time_ms=trace.response_time_ms,
    )


@app.get("/traces", response_model=list[TraceResponse])
def get_traces(
    category: Optional[str] = Query(None, description="Filter by category"),
    db: Session = Depends(get_db),
):
    """
    GET /traces — returns all traces, most recent first.
    Supports optional filtering by category.
    """
    query = db.query(Trace).order_by(Trace.timestamp.desc())

    if category:
        cat_enum = VALID_CATEGORIES.get(category.lower())
        if cat_enum is None:
            raise HTTPException(status_code=400, detail=f"Invalid category: {category}")
        query = query.filter(Trace.category == cat_enum)

    traces = query.all()
    return [
        TraceResponse(
            id=t.id,
            user_message=t.user_message,
            bot_response=t.bot_response,
            category=t.category.value,
            timestamp=t.timestamp,
            response_time_ms=t.response_time_ms,
        )
        for t in traces
    ]


@app.get("/analytics", response_model=AnalyticsResponse)
def get_analytics(db: Session = Depends(get_db)):
    """
    GET /analytics — returns aggregate stats: total traces,
    breakdown by category, average response time.
    """
    total = db.query(func.count(Trace.id)).scalar() or 0
    avg_rt = db.query(func.avg(Trace.response_time_ms)).scalar() or 0

    category_counts = (
        db.query(Trace.category, func.count(Trace.id))
        .group_by(Trace.category)
        .all()
    )

    categories = []
    for cat, count in category_counts:
        categories.append(
            CategoryStat(
                category=cat.value,
                count=count,
                percentage=round((count / total) * 100, 1) if total > 0 else 0,
            )
        )

    # Ensure all 5 categories are represented
    existing = {c.category for c in categories}
    for cat_enum in CategoryEnum:
        if cat_enum.value not in existing:
            categories.append(CategoryStat(category=cat_enum.value, count=0, percentage=0))

    return AnalyticsResponse(
        total_traces=total,
        categories=categories,
        average_response_time_ms=round(avg_rt, 1),
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
