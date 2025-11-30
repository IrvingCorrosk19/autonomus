"""
Modelos de base de datos
"""
from app.models.lead import Lead, LeadStatus
from app.models.message import Message, MessageChannel, RawMessage
from app.models.conversation import Conversation, ConversationStatus
from app.models.classification import LeadClassification
from app.models.intent import LeadIntent, IntentType
from app.models.sentiment import SentimentAnalysis
from app.models.customer import Customer
from app.models.case import Case, CaseStatus
from app.models.cart import Cart
from app.models.purchase import Purchase
from app.models.invoice import Invoice
from app.models.content import GeneratedContent
from app.models.alert import Alert

__all__ = [
    "Lead",
    "LeadStatus",
    "Message",
    "MessageChannel",
    "RawMessage",
    "Conversation",
    "ConversationStatus",
    "LeadClassification",
    "LeadIntent",
    "IntentType",
    "SentimentAnalysis",
    "Customer",
    "Case",
    "CaseStatus",
    "Cart",
    "Purchase",
    "Invoice",
    "GeneratedContent",
    "Alert",
]

