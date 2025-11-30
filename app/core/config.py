"""
Configuración de la aplicación usando Pydantic Settings
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Configuración de la aplicación"""
    
    # App
    APP_NAME: str = "Autonomous CRM"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str
    DATABASE_SYNC_URL: str
    
    # Security
    SECRET_KEY: str
    WEBHOOK_VERIFY_TOKEN: str
    
    # OpenAI
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4-turbo-preview"
    
    # Anthropic Claude
    ANTHROPIC_API_KEY: Optional[str] = None
    ANTHROPIC_MODEL: str = "claude-3-sonnet-20240229"
    
    # Google Gemini
    GOOGLE_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-pro"
    
    # Meta APIs
    META_ACCESS_TOKEN: Optional[str] = None
    META_APP_SECRET: Optional[str] = None
    WHATSAPP_PHONE_NUMBER_ID: Optional[str] = None
    INSTAGRAM_BUSINESS_ACCOUNT_ID: Optional[str] = None
    FACEBOOK_PAGE_ID: Optional[str] = None
    
    # n8n
    N8N_WEBHOOK_URL: str = "http://localhost:5678/webhook"
    N8N_API_KEY: Optional[str] = None
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    
    # Enrichment APIs
    CLEARBIT_API_KEY: Optional[str] = None
    FULLCONTACT_API_KEY: Optional[str] = None
    
    # Storage
    STORAGE_TYPE: str = "local"
    STORAGE_PATH: str = "./storage"
    
    # Jobs intervals
    FOLLOW_UP_CHECK_INTERVAL_HOURS: int = 1
    CART_RECOVERY_CHECK_INTERVAL_HOURS: int = 1
    PAYMENT_REMINDER_CHECK_INTERVAL_HOURS: int = 24
    ALERTS_CHECK_INTERVAL_HOURS: int = 1
    
    # Limits
    MAX_MESSAGE_LENGTH: int = 4096
    MAX_CONVERSATION_HISTORY: int = 50
    LEAD_SCORE_THRESHOLD_HOT: int = 80
    LEAD_SCORE_THRESHOLD_WARM: int = 50
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignorar variables extra en .env


settings = Settings()

