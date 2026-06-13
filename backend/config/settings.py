import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Server
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    PORT = int(os.getenv("PORT", 8000))
    HOST = os.getenv("HOST", "0.0.0.0")
    
    # IBM Quantum
    IBM_QUANTUM_TOKEN = os.getenv("IBM_QUANTUM_TOKEN", "")
    IBM_QUANTUM_INSTANCE = os.getenv("IBM_QUANTUM_INSTANCE", "mindtechindustries")
    
    # BlackSky Module Targets
    CRYO_OS_TARGET = float(os.getenv("CRYO_OS_TARGET", 19.5))
    GATE_SMOOTH_TARGET = float(os.getenv("GATE_SMOOTH_TARGET", 47.4))
    NODE_LINK_TARGET = float(os.getenv("NODE_LINK_TARGET", 316.0))
    
    # IBM Verified Results (from EntangleGuard)
    IBM_JOB_ID = os.getenv("IBM_JOB_ID", "d55p3jgnsj9s73b32lj0")
    QUANTUM_CORRELATION = float(os.getenv("QUANTUM_CORRELATION", 0.984))
    CHSH_SCORE = float(os.getenv("CHSH_SCORE", 2.76))
    
    # Patent
    PATENT_NUMBER = os.getenv("PATENT_NUMBER", "2026/05142")
    PATENT_FILING_DATE = os.getenv("PATENT_FILING_DATE", "2026-05-12")
    
    # CORS
    CORS_ORIGINS = [
        "http://localhost:3000",
        "http://localhost:5500",
        "https://*.onrender.com",
        "https://*.netlify.app"
    ]

settings = Settings()