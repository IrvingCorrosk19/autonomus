"""
FLUJOS 18-20: Deduplicación, Limpieza y Enriquecimiento de Datos
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.deduplicator import Deduplicator
from app.services.data_cleaner import DataCleaner
from app.services.enrichment import DataEnrichmentService
from app.api.deps import get_database
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.post("/deduplicate")
async def deduplicate_data(
    db: AsyncSession = Depends(get_database)
):
    """
    FLUJO 18: Detecta y fusiona registros duplicados.
    """
    try:
        deduplicator = Deduplicator()
        duplicates = await deduplicator.find_duplicates(db)
        return {"status": "completed", "duplicates_found": len(duplicates)}
    except Exception as e:
        logger.error("deduplication_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/clean")
async def clean_data(
    contact_id: str,
    db: AsyncSession = Depends(get_database)
):
    """
    FLUJO 19: Limpia y normaliza datos de un contacto.
    """
    try:
        from app.models.customer import Customer
        contact = await db.get(Customer, contact_id)
        if not contact:
            raise HTTPException(status_code=404, detail="Contact not found")
        
        cleaner = DataCleaner()
        cleaned = await cleaner.clean_contact(contact, db)
        return {"status": "cleaned", "contact_id": contact_id}
    except Exception as e:
        logger.error("data_cleaning_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/enrich")
async def enrich_data(
    contact_id: str,
    db: AsyncSession = Depends(get_database)
):
    """
    FLUJO 20: Enriquece contacto con datos externos y predicciones.
    """
    try:
        from app.models.customer import Customer
        contact = await db.get(Customer, contact_id)
        if not contact:
            raise HTTPException(status_code=404, detail="Contact not found")
        
        enrichment = DataEnrichmentService()
        enriched = await enrichment.enrich_contact(contact, db)
        return {"status": "enriched", "contact_id": contact_id}
    except Exception as e:
        logger.error("data_enrichment_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

