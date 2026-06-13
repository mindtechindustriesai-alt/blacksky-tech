from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BlackSkyModule(BaseModel):
    name: str
    industry_benchmark: str
    benchmark_value: float
    blacksky_performance: float
    improvement_percent: float
    status: str

class BlackSkyPortfolio(BaseModel):
    timestamp: datetime
    modules: dict
    valuation_range_usd: tuple
    valuation_range_zar: tuple

class IBMVerification(BaseModel):
    job_id: str
    correlation: float
    chsh_score: float
    backend: str
    verified_at: datetime
    reproducible: bool

class LicenseRequest(BaseModel):
    licensee_name: str
    license_type: str  # Perpetual, Annual, Per-Seat, Revenue-Share, OEM
    modules: list
    jurisdiction: str
    exclusivity: str

class LicenseResponse(BaseModel):
    license_agreement: str
    estimated_fee_usd: float
    estimated_fee_zar: float
    generated_at: datetime