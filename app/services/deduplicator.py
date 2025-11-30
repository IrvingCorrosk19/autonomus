"""
FLUJO 18: Deduplicación Automática
"""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.customer import Customer
from app.models.lead import Lead
from app.ai.base import AIAdapter
from app.ai.factory import AIAdapterFactory
from app.core.logging import get_logger
from fuzzywuzzy import fuzz

logger = get_logger(__name__)


class Deduplicator:
    """
    Detecta y fusiona duplicados usando:
    - Fuzzy matching en nombres
    - Comparación de emails/teléfonos
    - IA para casos ambiguos
    """
    
    def __init__(self, ai_adapter: Optional[AIAdapter] = None):
        self.ai = ai_adapter or AIAdapterFactory.get_default_adapter()
    
    async def find_duplicates(self, db: AsyncSession) -> List[Dict]:
        """
        Job que corre diariamente para detectar duplicados.
        """
        # Obtener todos los contactos
        stmt = select(Customer)
        result = await db.execute(stmt)
        all_contacts = result.scalars().all()
        
        duplicates = []
        processed = set()
        
        for contact in all_contacts:
            if contact.id in processed:
                continue
            
            # Buscar potenciales duplicados
            potential_dupes = await self._find_potential_duplicates(contact, db)
            
            if potential_dupes:
                # Usar IA para confirmar si son duplicados
                confirmed_dupes = await self._confirm_duplicates_with_ai(
                    contact,
                    potential_dupes
                )
                
                if confirmed_dupes:
                    duplicates.append({
                        "primary": contact,
                        "duplicates": confirmed_dupes
                    })
                    processed.update([d.id for d in confirmed_dupes])
        
        return duplicates
    
    async def _find_potential_duplicates(
        self,
        contact: Customer,
        db: AsyncSession
    ) -> List[Customer]:
        """Encuentra potenciales duplicados usando reglas básicas"""
        potentials = []
        
        # Regla 1: Email exacto
        if contact.email:
            stmt = select(Customer).where(
                Customer.email == contact.email,
                Customer.id != contact.id
            )
            result = await db.execute(stmt)
            potentials.extend(result.scalars().all())
        
        # Regla 2: Teléfono exacto
        if contact.phone:
            stmt = select(Customer).where(
                Customer.phone == contact.phone,
                Customer.id != contact.id
            )
            result = await db.execute(stmt)
            potentials.extend(result.scalars().all())
        
        # Regla 3: Nombre muy similar (fuzzy match)
        stmt = select(Customer).where(Customer.id != contact.id)
        result = await db.execute(stmt)
        all_others = result.scalars().all()
        
        for other in all_others:
            if contact.name and other.name:
                similarity = fuzz.ratio(
                    contact.name.lower(),
                    other.name.lower()
                )
                if similarity > 85:  # 85% similar
                    potentials.append(other)
        
        return list(set(potentials))
    
    async def _confirm_duplicates_with_ai(
        self,
        contact: Customer,
        potentials: List[Customer]
    ) -> List[Customer]:
        """IA decide si son duplicados reales"""
        if not self.ai:
            # Sin IA, usar solo reglas básicas
            return potentials
        
        confirmed = []
        
        for potential in potentials:
            prompt = f"""
            Determina si estos dos registros son la misma persona:
            
            REGISTRO 1:
            - Nombre: {contact.name}
            - Email: {contact.email or 'N/A'}
            - Teléfono: {contact.phone or 'N/A'}
            
            REGISTRO 2:
            - Nombre: {potential.name}
            - Email: {potential.email or 'N/A'}
            - Teléfono: {potential.phone or 'N/A'}
            
            CRITERIOS:
            - Email o teléfono idéntico = casi seguro duplicado
            - Nombre muy similar = probablemente duplicado
            
            Responde: "duplicado" o "diferente"
            """
            
            response = await self.ai.generate_response(prompt)
            if "duplicado" in response.lower():
                confirmed.append(potential)
        
        return confirmed
    
    async def merge_duplicates(
        self,
        primary: Customer,
        duplicates: List[Customer],
        db: AsyncSession
    ):
        """
        Fusiona duplicados en el registro primario.
        """
        # Consolidar datos
        for dupe in duplicates:
            # Transferir datos faltantes
            if not primary.email and dupe.email:
                primary.email = dupe.email
            if not primary.phone and dupe.phone:
                primary.phone = dupe.phone
            # TODO: Transferir historial de interacciones
        
        # Marcar duplicados como merged
        for dupe in duplicates:
            dupe.status = "merged"
            # TODO: Agregar campo merged_into
        
        await db.commit()
        
        logger.info(
            "duplicates_merged",
            primary_id=primary.id,
            merged_count=len(duplicates)
        )

