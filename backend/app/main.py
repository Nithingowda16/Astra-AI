from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from datetime import datetime

from backend.app.core.config import settings
from backend.app.core.database import SessionLocal, engine, Base
from backend.app.models.customer import Customer
from backend.app.models.user import User
from backend.app.core.security import hash_password, get_current_user
from backend.app.seed.seed_data import seed_database
from backend.app.api import (
    auth,
    dashboard,
    transactions,
    customers,
    alerts,
    investigations,
    regulatory,
    copilot
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("compliance_copilot")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing database and checking seed state...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Check if DB has data; if not, auto-seed
        cust_count = db.query(Customer).count()
        if cust_count == 0:
            logger.info("Empty database detected. Seeding initial compliance records...")
            seed_database(db)
        else:
            logger.info(f"Database contains {cust_count} customer profiles. Ready.")

        # Ensure default Admin and User credentials exist
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            admin_pwd, admin_salt = hash_password("AdminPassword123!")
            admin_user = User(
                username="admin",
                email="admin@compliance.ai",
                full_name="Chief Compliance Officer",
                hashed_password=admin_pwd,
                salt=admin_salt,
                role="admin",
                is_active=True,
                created_at=datetime.utcnow()
            )
            db.add(admin_user)
            db.commit()

        user_acc = db.query(User).filter(User.username == "user").first()
        if not user_acc:
            user_pwd, user_salt = hash_password("UserPassword123!")
            user_acc = User(
                username="user",
                email="user@compliance.ai",
                full_name="Compliance User",
                hashed_password=user_pwd,
                salt=user_salt,
                role="user",
                is_active=True,
                created_at=datetime.utcnow()
            )
            db.add(user_acc)
            db.commit()

        user_count = db.query(User).count()
        logger.info(f"Security system verified with {user_count} registered users.")
    except Exception as e:
        logger.error(f"Error during database startup check: {e}")
    finally:
        db.close()
    yield
    logger.info("Shutting down Compliance Copilot service...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Risk, Fraud & Regulatory Intelligence Copilot - End-to-end Compliance Platform Prototype",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Authentication Router (public login & register, self-contained dependencies)
app.include_router(auth.router, prefix=settings.API_V1_STR)

# Register Protected API Routers under /api (Secured via Bearer JWT)
app.include_router(dashboard.router, prefix=settings.API_V1_STR, dependencies=[Depends(get_current_user)])
app.include_router(transactions.router, prefix=settings.API_V1_STR, dependencies=[Depends(get_current_user)])
app.include_router(customers.router, prefix=settings.API_V1_STR, dependencies=[Depends(get_current_user)])
app.include_router(alerts.router, prefix=settings.API_V1_STR, dependencies=[Depends(get_current_user)])
app.include_router(investigations.router, prefix=settings.API_V1_STR, dependencies=[Depends(get_current_user)])
app.include_router(regulatory.router, prefix=settings.API_V1_STR, dependencies=[Depends(get_current_user)])
app.include_router(copilot.router, prefix=settings.API_V1_STR, dependencies=[Depends(get_current_user)])


@app.get("/")
def root():
    return {
        "service": settings.PROJECT_NAME,
        "status": "operational",
        "docs_url": "/docs",
        "story": "DETECT -> EXPLAIN -> INVESTIGATE -> PROVIDE EVIDENCE -> REPORT"
    }

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "regulatory_kb": "Demo Regulatory Knowledge Base v1.0",
        "engine": "Explainable Rule-Based Risk Engine"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
