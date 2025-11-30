"""
FLUJO 10: Nutrición Inteligente de Leads
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.nurturing import NurturingEngine
from app.api.deps import get_database
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.post("/process")
async def process_nurturing(
    lead_id: str,
    db: AsyncSession = Depends(get_database)
):
    """
    Procesa un lead para nutrición inteligente.
    """
    try:
        from app.models.lead import Lead
        lead = await db.get(Lead, lead_id)
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")
        
        engine = NurturingEngine()
        await engine.process_lead(lead, db)
        
        return {"status": "processed", "lead_id": lead_id}
    except Exception as e:
        logger.error("nurturing_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

