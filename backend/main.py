from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from pathlib import Path
from app.config import settings
from app.database import create_tables
import uvicorn

# Import all routers
from app.routes import (
    auth,
    goals,
    tasks,
    notes,
    files,
    spreadsheets,
    ai_chat
)


# Lifespan context manager for startup and shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: ensure tables are created
    try:
        create_tables()
        print("Database tables created/verified successfully")
    except Exception as e:
        print(f"Database initialization notice: {e}")
    yield
    # Shutdown
    print("Shutting down Cosmic Assistant...")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="Cosmic Assistant - Agentic AI for Personal Productivity",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS if hasattr(settings, "CORS_ORIGINS") else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "database": "connected"
    }


# Include all feature routers with /api prefix
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(goals.router, prefix="/api/goals", tags=["Goals"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])
app.include_router(notes.router, prefix="/api/notes", tags=["Notes"])
app.include_router(files.router, prefix="/api/files", tags=["Files"])
app.include_router(spreadsheets.router, prefix="/api/spreadsheets", tags=["Spreadsheets"])
app.include_router(ai_chat.router, prefix="/api/ai", tags=["AI Assistant"])

# Serve the web application from the same deployment as the API.
frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
if frontend_dir.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )