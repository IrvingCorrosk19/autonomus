"""
FLUJO 19: Limpieza y Normalización de Datos
"""
import re
import phonenumbers
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.customer import Customer
from app.models.lead import Lead
from app.ai.base import AIAdapter
from app.ai.factory import AIAdapterFactory
from app.core.logging import get_logger

logger = get_logger(__name__)


class DataCleaner:
    """
    Limpia y normaliza datos:
    - Emails: lowercase, trim, validación
    - Teléfonos: formato internacional estándar
    - Nombres: capitalización correcta
    - Direcciones: estandarización
    """
    
    def __init__(self, ai_adapter: Optional[AIAdapter] = None):
        self.ai = ai_adapter or AIAdapterFactory.get_default_adapter()
    
    async def clean_contact(self, contact: Customer, db: AsyncSession) -> Customer:
        """
        Limpia todos los campos de un contacto.
        """
        # Email
        if contact.email:
            contact.email = self._clean_email(contact.email)
        
        # Teléfono
        if contact.phone:
            contact.phone = self._clean_phone(contact.phone, default_country="PA")
        
        # Nombre
        if contact.name:
            contact.name = self._clean_name(contact.name)
        
        # Empresa
        if contact.company:
            contact.company = self._clean_company_name(contact.company)
        
        # Usar IA para campos ambiguos
        contact = await self._ai_assisted_cleaning(contact)
        
        await db.commit()
        return contact
    
    def _clean_email(self, email: str) -> Optional[str]:
        """Limpia y valida email"""
        email = email.strip().lower()
        
        # Validación básica
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            logger.warning("invalid_email_format", email=email)
            return None
        
        # Correcciones comunes
        typo_corrections = {
            "@gmial.com": "@gmail.com",
            "@gmai.com": "@gmail.com",
            "@hotmial.com": "@hotmail.com",
            "@yahooo.com": "@yahoo.com"
        }
        
        for typo, correct in typo_corrections.items():
            if typo in email:
                email = email.replace(typo, correct)
                logger.info("email_typo_corrected", corrected=email)
        
        return email
    
    def _clean_phone(
        self,
        phone: str,
        default_country: str = "PA"
    ) -> Optional[str]:
        """Normaliza teléfono a formato internacional E.164"""
        try:
            parsed = phonenumbers.parse(phone, default_country)
            
            if not phonenumbers.is_valid_number(parsed):
                logger.warning("invalid_phone_number", phone=phone)
                return None
            
            formatted = phonenumbers.format_number(
                parsed,
                phonenumbers.PhoneNumberFormat.E164
            )
            
            return formatted
            
        except phonenumbers.phonenumberutil.NumberParseException:
            logger.warning("phone_parse_error", phone=phone)
            return None
    
    def _clean_name(self, name: str) -> str:
        """Capitaliza nombre correctamente"""
        name = name.strip().title()
        
        # Excepciones (prefijos, sufijos)
        exceptions = ["de", "del", "la", "los", "van", "von", "da", "di"]
        
        words = name.split()
        corrected = []
        
        for i, word in enumerate(words):
            if i > 0 and word.lower() in exceptions:
                corrected.append(word.lower())
            else:
                corrected.append(word)
        
        return " ".join(corrected)
    
    def _clean_company_name(self, company: str) -> str:
        """Limpia nombre de empresa"""
        return company.strip().title()
    
    async def _ai_assisted_cleaning(self, contact: Customer) -> Customer:
        """IA ayuda con casos ambiguos o complejos"""
        if not self.ai:
            return contact
        
        prompt = f"""
        Revisa y sugiere correcciones para este contacto:
        
        Nombre: {contact.name}
        Email: {contact.email}
        Teléfono: {contact.phone}
        Empresa: {contact.company}
        
        INSTRUCCIONES:
        1. Detecta inconsistencias obvias
        2. Sugiere formato correcto
        3. Identifica campos en lugar equivocado
        
        Responde con correcciones sugeridas.
        """
        
        # TODO: Parsear respuesta de IA y aplicar correcciones
        return contact

