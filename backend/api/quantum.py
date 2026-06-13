from fastapi import APIRouter, HTTPException
from datetime import datetime

from ..services.ibm_service import ibm_service
from ..config.settings import settings

router = APIRouter(prefix="/quantum", tags=["Quantum"])

@router.get("/status")
async def quantum_status():
    """Get IBM quantum verification status"""
    return ibm_service.get_verification_status()

@router.get("/blacksky-targets")
async def blacksky_targets():
    """Get BlackSky module performance targets"""
    return ibm_service.get_blacksky_targets()

@router.get("/patent")
async def patent_info():
    """Get patent information"""
    return {
        "patent_number": settings.PATENT_NUMBER,
        "filing_date": settings.PATENT_FILING_DATE,
        "status": "provisional",
        "title": "Adaptive Learning Ecosystem with Integrated Safety Monitoring and Optional Quantum-Secure Verification"
    }

@router.get("/valuation")
async def valuation():
    """Get portfolio valuation estimate"""
    return {
        "valuation_usd": {
            "low": 100_000_000,
            "high": 200_000_000,
            "currency": "USD"
        },
        "valuation_zar": {
            "low": 1_850_000_000,
            "high": 3_700_000_000,
            "currency": "ZAR",
            "exchange_rate": 18.5
        },
        "based_on": "IBM-verified entanglement + BlackSky engineering targets"
    }