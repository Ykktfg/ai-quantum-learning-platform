from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from app.core.exceptions import global_exception_handler
from app.core.validation import validation_exception_handler

from app.db.database import Base, engine
from app.db import models

from app.api.routes.health import router as health_router
from app.api.routes.auth import router as auth_router
from app.api.routes.users import router as user_router
from app.api.routes.courses import router as course_router
from app.api.routes.enrollments import router as enrollment_router
from app.api.routes.progress import router as progress_router
from app.api.routes.circuits import router as circuit_router
from app.api.routes.simulation import router as simulation_router
from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.activity import router as activity_router
from app.api.routes.analytics import router as analytics_router
from app.api.routes import lessons


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="AI Quantum Learning Platform API",
    description=(
        "Backend API for the SIH AI-Powered Interactive "
        "Quantum Computing Learning Platform"
    ),
    version="1.0.0",
)


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

Base.metadata.create_all(
    bind=engine
)


# ============================================================
# GLOBAL EXCEPTION HANDLERS
# ============================================================

app.add_exception_handler(
    Exception,
    global_exception_handler,
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,
)


# ============================================================
# CORS CONFIGURATION
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# HEALTH ROUTES
# ============================================================

app.include_router(
    health_router,
    prefix="/api",
    tags=["Health"],
)


# ============================================================
# AUTHENTICATION ROUTES
# ============================================================

app.include_router(
    auth_router,
    prefix="/api",
    tags=["Authentication"],
)


# ============================================================
# USER ROUTES
# ============================================================

app.include_router(
    user_router,
    prefix="/api",
    tags=["Users"],
)


# ============================================================
# COURSE ROUTES
# ============================================================

app.include_router(
    course_router,
    prefix="/api",
    tags=["Courses"],
)


# ============================================================
# ENROLLMENT ROUTES
# ============================================================

app.include_router(
    enrollment_router,
    prefix="/api",
    tags=["Enrollments"],
)


# ============================================================
# LESSON ROUTES
# ============================================================

app.include_router(
    lessons.router,
    prefix="/api",
    tags=["Lessons"],
)


# ============================================================
# PROGRESS ROUTES
# ============================================================

app.include_router(
    progress_router,
    prefix="/api",
    tags=["Progress"],
)


# ============================================================
# CIRCUIT ROUTES
# ============================================================

app.include_router(
    circuit_router,
    prefix="/api",
    tags=["Circuits"],
)


# ============================================================
# SIMULATION ROUTES
# ============================================================

app.include_router(
    simulation_router,
    prefix="/api",
    tags=["Simulation"],
)


# ============================================================
# DASHBOARD ROUTES
# ============================================================

app.include_router(
    dashboard_router,
    prefix="/api",
    tags=["Dashboard"],
)


# ============================================================
# ACTIVITY ROUTES
# ============================================================

app.include_router(
    activity_router,
    prefix="/api",
    tags=["Activity"],
)


# ============================================================
# ANALYTICS ROUTES
# ============================================================

app.include_router(
    analytics_router,
    prefix="/api",
    tags=["Analytics"],
)


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():
    return {
        "message": "AI Quantum Learning Platform Backend",
        "status": "running",
    }