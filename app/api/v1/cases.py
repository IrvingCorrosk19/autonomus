"""
FLUJO 9: Cierre Automático de Caso
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.case_closure import CaseClosureService
from app.api.deps import get_database
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.post("/evaluate-closure")
async def evaluate_case_closure(
    case_id: str,
    latest_message: str,
    db: AsyncSession = Depends(get_database)
):
    """
    Evalúa si un caso puede cerrarse automáticamente.
    """
    try:
        from app.models.case import Case
        case = await db.get(Case, case_id)
        if not case:
            raise HTTPException(status_code=404, detail="Case not found")
        
        service = CaseClosureService()
        result = await service.evaluate_closure(case, latest_message, db)
        return result
    except Exception as e:
        logger.error("case_closure_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

