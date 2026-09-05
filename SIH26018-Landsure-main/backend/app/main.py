import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.database.session import init_db, SessionLocal
from app.api import api_router
from app.models.users import User
from app.core.dependencies import get_password_hash

# Initialize database schema tables
init_db()

def seed_default_users():
    """Ensure default official users exist in database on startup."""
    db = SessionLocal()
    try:
        if not db.query(User).filter(User.username == "revenue_officer").first():
            officer = User(
                username="revenue_officer",
                email="officer@revenue.gov.in",
                hashed_password=get_password_hash("sih2026password"),
                role="Official",
                is_active=True
            )
            db.add(officer)

        if not db.query(User).filter(User.username == "admin").first():
            admin = User(
                username="admin",
                email="admin@revenue.gov.in",
                hashed_password=get_password_hash("sih2026admin"),
                role="Admin",
                is_active=True
            )
            db.add(admin)

        if not db.query(User).filter(User.username == "admin_sih").first():
            admin_sih = User(
                username="admin_sih",
                email="admin_sih@revenue.gov.in",
                hashed_password=get_password_hash("sih2026admin"),
                role="Admin",
                is_active=True
            )
            db.add(admin_sih)

        db.commit()
    except Exception as e:
        print(f"Error auto-seeding users: {e}")
        db.rollback()
    finally:
        db.close()

# Auto-seed users on initialization
seed_default_users()

app = FastAPI(
    title="LandSure AI - Land Record Digitization & Validation API",
    description="SIH26018 Production-Ready Multilingual Land Records Digitization Backend Services",
    version="2.0.0"
)

import traceback
from fastapi.responses import JSONResponse

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    err_tb = traceback.format_exc()
    print("GLOBAL UNCAUGHT EXCEPTION:", err_tb)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error", "error_message": str(exc), "traceback": err_tb}
    )

# Robust Production CORS Configuration for Vercel, Render & Localhost
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://.*",
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "https://sih-26018-land-digitization.vercel.app",
        "https://sih26018-land-digitization.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Static Files for serving original and preprocessed images securely
uploads_abs_path = os.path.abspath(settings.UPLOAD_DIR)
preprocessed_abs_path = os.path.abspath(settings.PREPROCESSED_DIR)

os.makedirs(uploads_abs_path, exist_ok=True)
os.makedirs(preprocessed_abs_path, exist_ok=True)

app.mount("/static/uploads", StaticFiles(directory=uploads_abs_path), name="uploads")
app.mount("/static/preprocessed", StaticFiles(directory=preprocessed_abs_path), name="preprocessed")

# Register API Router
app.include_router(api_router, prefix="/api")

@app.get("/")
def read_root():
    return {
        "status": "Healthy",
        "service": "LandSure AI Land Record Digitization API",
        "version": "2.0.0",
        "docs": "/docs"
    }
