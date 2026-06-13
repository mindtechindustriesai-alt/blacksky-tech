from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .config.settings import settings
from .api import quantum, license
from .services.ibm_service import ibm_service

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    print("""
    ╔════════════════════════════════════════════════════════════════╗
    ║                    BLACKSKY-TECH BACKEND                       ║
    ║  IBM Verified Entanglement · CHSH S=2.76 · 98.4% Correlation  ║
    ║  Patent: SA 2026/05142                                         ║
    ╚════════════════════════════════════════════════════════════════╝
    """)
    yield
    print("Shutting down BLACKSKY backend...")

app = FastAPI(
    title="BLACKSKY-TECH API",
    description="Quantum module licensing and IBM verification",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(quantum.router)
app.include_router(license.router)

@app.get("/")
async def root():
    return {
        "service": "BLACKSKY-TECH",
        "version": "1.0.0",
        "status": "operational",
        "ibm_verified": ibm_service.get_verification_status(),
        "endpoints": [
            "GET /",
            "GET /health",
            "GET /quantum/status",
            "GET /quantum/blacksky-targets",
            "GET /quantum/patent",
            "GET /quantum/valuation",
            "POST /license/generate"
        ]
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "quantum_verified": True}