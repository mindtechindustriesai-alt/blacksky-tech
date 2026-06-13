from fastapi import APIRouter, HTTPException
from datetime import datetime

from ..models.blacksky_modules import LicenseRequest, LicenseResponse
from ..services.ibm_service import ibm_service

router = APIRouter(prefix="/license", tags=["License"])

@router.post("/generate")
async def generate_license(request: LicenseRequest):
    """Generate a commercial license for BlackSky modules"""
    
    # Calculate base fee
    module_count = len(request.modules)
    base_fee = 2_500_000  # $2.5M base
    
    # Module multiplier
    module_multiplier = max(1, module_count)
    
    # Exclusivity premium
    exclusivity_premium = 0
    if "Exclusive" in request.exclusivity:
        exclusivity_premium = 1_000_000
    if request.exclusivity == "Exclusive-Worldwide":
        exclusivity_premium = 3_000_000
    
    # Jurisdiction factor
    jurisdiction_factors = {
        "Delaware": 1.2,
        "UK": 1.1,
        "Singapore": 1.05,
        "South Africa": 1.0,
        "EU": 1.15
    }
    jurisdiction_factor = jurisdiction_factors.get(request.jurisdiction, 1.0)
    
    # Total calculation
    total_usd = (base_fee * module_multiplier * jurisdiction_factor) + exclusivity_premium
    total_zar = total_usd * 18.5
    
    # Generate license text
    license_text = f"""
BLACKSKY QUANTUM MODULES LICENSE AGREEMENT
==============================================

THIS LICENSE AGREEMENT is made and entered into as of {datetime.now().strftime('%B %d, %Y')},
by and between BLACKSKY TECHNOLOGIES (the "Licensor") and {request.licensee_name} (the "Licensee").

1. LICENSE GRANT
   Licensor hereby grants to Licensee a {request.license_type.lower()} license to use the following
   BLACKSKY Quantum Modules: {', '.join(request.modules)}.

2. FEES AND PAYMENT
   Licensee shall pay Licensor the total fee of ${total_usd:,.2f} USD ({total_zar:,.2f} ZAR).

3. INTELLECTUAL PROPERTY
   All rights, title, and interest in the BLACKSKY Modules remain with BLACKSKY TECHNOLOGIES.
   IBM Job ID: {ibm_service.get_verification_status()['job_id']}
   Quantum Correlation: {ibm_service.get_verification_status()['correlation']*100:.1f}%

4. GOVERNING LAW
   This Agreement shall be governed by the laws of {request.jurisdiction}.

5. EXCLUSIVITY
   This license is granted on a {request.exclusivity.lower()} basis.

6. CONFIDENTIALITY
   Licensee agrees to maintain strict confidentiality of all BLACKSKY materials.

IN WITNESS WHEREOF, the parties have executed this Agreement as of the date first written above.

BLACKSKY TECHNOLOGIES                     LICENSEE
_________________________                _________________________
Authorized Signatory                      {request.licensee_name} Representative
"""
    
    return LicenseResponse(
        license_agreement=license_text,
        estimated_fee_usd=total_usd,
        estimated_fee_zar=total_zar,
        generated_at=datetime.now()
    )