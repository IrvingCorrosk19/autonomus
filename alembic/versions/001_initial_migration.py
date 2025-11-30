"""Initial migration

Revision ID: 001_initial
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Leads
    op.create_table(
        'leads',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('phone', sa.String(), nullable=True),
        sa.Column('company', sa.String(), nullable=True),
        sa.Column('score', sa.Integer(), nullable=True),
        sa.Column('category', sa.String(), nullable=True),
        sa.Column('status', sa.Enum('NEW', 'QUALIFIED', 'NURTURING', 'CONVERTED', 'LOST', name='leadstatus'), nullable=True),
        sa.Column('source', sa.String(), nullable=True),
        sa.Column('campaign_id', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('converted_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Customers
    op.create_table(
        'customers',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('lead_id', sa.String(), nullable=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('phone', sa.String(), nullable=True),
        sa.Column('company', sa.String(), nullable=True),
        sa.Column('industry', sa.String(), nullable=True),
        sa.Column('predicted_clv', sa.Float(), nullable=True),
        sa.Column('purchasing_power', sa.String(), nullable=True),
        sa.Column('interests', sa.JSON(), nullable=True),
        sa.Column('segment', sa.String(), nullable=True),
        sa.Column('total_purchases', sa.Integer(), nullable=True),
        sa.Column('total_spent', sa.Float(), nullable=True),
        sa.Column('avg_order_value', sa.Float(), nullable=True),
        sa.Column('last_purchase_date', sa.DateTime(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('churn_risk_score', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['lead_id'], ['leads.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Conversations
    op.create_table(
        'conversations',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('lead_id', sa.String(), nullable=True),
        sa.Column('customer_id', sa.String(), nullable=True),
        sa.Column('channel', sa.String(), nullable=False),
        sa.Column('status', sa.Enum('ACTIVE', 'WAITING_CUSTOMER', 'WAITING_AGENT', 'RESOLVED', 'CLOSED', name='conversationstatus'), nullable=True),
        sa.Column('message_count', sa.Integer(), nullable=True),
        sa.Column('avg_sentiment_score', sa.Float(), nullable=True),
        sa.Column('bot_handled', sa.Boolean(), nullable=True),
        sa.Column('escalated', sa.Boolean(), nullable=True),
        sa.Column('escalation_reason', sa.String(), nullable=True),
        sa.Column('started_at', sa.DateTime(), nullable=False),
        sa.Column('last_message_at', sa.DateTime(), nullable=True),
        sa.Column('closed_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ),
        sa.ForeignKeyConstraint(['lead_id'], ['leads.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Raw Messages
    op.create_table(
        'raw_messages',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('channel', sa.Enum('WHATSAPP', 'INSTAGRAM', 'MESSENGER', name='messagechannel'), nullable=False),
        sa.Column('sender_id', sa.String(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('metadata', sa.JSON(), nullable=True),
        sa.Column('received_at', sa.DateTime(), nullable=False),
        sa.Column('processed', sa.Boolean(), nullable=True),
        sa.Column('processing_error', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Messages
    op.create_table(
        'messages',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('conversation_id', sa.String(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('sender', sa.String(), nullable=False),
        sa.Column('direction', sa.String(), nullable=False),
        sa.Column('intent', sa.String(), nullable=True),
        sa.Column('sentiment', sa.String(), nullable=True),
        sa.Column('sentiment_score', sa.Float(), nullable=True),
        sa.Column('sent_at', sa.DateTime(), nullable=False),
        sa.Column('delivered_at', sa.DateTime(), nullable=True),
        sa.Column('read_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Lead Classifications
    op.create_table(
        'lead_classifications',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('lead_id', sa.String(), nullable=False),
        sa.Column('score', sa.Integer(), nullable=False),
        sa.Column('category', sa.String(), nullable=True),
        sa.Column('reasoning', sa.Text(), nullable=True),
        sa.Column('recommended_action', sa.String(), nullable=True),
        sa.Column('ai_model', sa.String(), nullable=True),
        sa.Column('classified_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['lead_id'], ['leads.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Lead Intents
    op.create_table(
        'lead_intents',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('lead_id', sa.String(), nullable=False),
        sa.Column('message_id', sa.String(), nullable=True),
        sa.Column('primary_intent', sa.String(), nullable=False),
        sa.Column('secondary_intents', sa.JSON(), nullable=True),
        sa.Column('confidence', sa.Float(), nullable=True),
        sa.Column('entities', sa.JSON(), nullable=True),
        sa.Column('detected_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['lead_id'], ['leads.id'], ),
        sa.ForeignKeyConstraint(['message_id'], ['messages.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Sentiment Analyses
    op.create_table(
        'sentiment_analyses',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('message_id', sa.String(), nullable=True),
        sa.Column('conversation_id', sa.String(), nullable=True),
        sa.Column('sentiment', sa.String(), nullable=False),
        sa.Column('score', sa.Float(), nullable=False),
        sa.Column('confidence', sa.Float(), nullable=True),
        sa.Column('emotions', sa.JSON(), nullable=True),
        sa.Column('urgency_level', sa.String(), nullable=True),
        sa.Column('churn_risk', sa.Float(), nullable=True),
        sa.Column('ai_model', sa.String(), nullable=True),
        sa.Column('analyzed_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ),
        sa.ForeignKeyConstraint(['message_id'], ['messages.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Cases
    op.create_table(
        'cases',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('customer_id', sa.String(), nullable=True),
        sa.Column('conversation_id', sa.String(), nullable=True),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('status', sa.Enum('OPEN', 'IN_PROGRESS', 'WAITING_CUSTOMER', 'RESOLVED', 'CLOSED', name='casestatus'), nullable=True),
        sa.Column('priority', sa.Integer(), nullable=True),
        sa.Column('opened_at', sa.DateTime(), nullable=False),
        sa.Column('closed_at', sa.DateTime(), nullable=True),
        sa.Column('resolution_time_hours', sa.Float(), nullable=True),
        sa.Column('closure_reason', sa.String(), nullable=True),
        sa.Column('customer_satisfaction', sa.Integer(), nullable=True),
        sa.Column('predicted_csat', sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ),
        sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Carts
    op.create_table(
        'carts',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('customer_id', sa.String(), nullable=False),
        sa.Column('items', sa.JSON(), nullable=False),
        sa.Column('total_amount', sa.Float(), nullable=False),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('last_activity', sa.DateTime(), nullable=False),
        sa.Column('recovery_attempt_count', sa.Integer(), nullable=True),
        sa.Column('discount_codes_used', sa.JSON(), nullable=True),
        sa.Column('recovered_at', sa.DateTime(), nullable=True),
        sa.Column('recovery_channel', sa.String(), nullable=True),
        sa.Column('final_attempt', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Purchases
    op.create_table(
        'purchases',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('customer_id', sa.String(), nullable=False),
        sa.Column('items', sa.JSON(), nullable=False),
        sa.Column('total_amount', sa.Float(), nullable=False),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('purchased_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Invoices
    op.create_table(
        'invoices',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('customer_id', sa.String(), nullable=False),
        sa.Column('purchase_id', sa.String(), nullable=True),
        sa.Column('number', sa.String(), nullable=False),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('issued_at', sa.DateTime(), nullable=False),
        sa.Column('due_date', sa.DateTime(), nullable=False),
        sa.Column('paid_at', sa.DateTime(), nullable=True),
        sa.Column('late_fee', sa.Float(), nullable=True),
        sa.Column('reminder_count', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ),
        sa.ForeignKeyConstraint(['purchase_id'], ['purchases.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('number')
    )
    
    # Generated Content
    op.create_table(
        'generated_content',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('content_type', sa.String(), nullable=False),
        sa.Column('platform', sa.String(), nullable=False),
        sa.Column('asset_url', sa.String(), nullable=True),
        sa.Column('copy', sa.Text(), nullable=True),
        sa.Column('hashtags', sa.JSON(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('scheduled_for', sa.DateTime(), nullable=True),
        sa.Column('published_at', sa.DateTime(), nullable=True),
        sa.Column('views', sa.Integer(), nullable=True),
        sa.Column('likes', sa.Integer(), nullable=True),
        sa.Column('comments', sa.Integer(), nullable=True),
        sa.Column('shares', sa.Integer(), nullable=True),
        sa.Column('engagement_rate', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Alerts
    op.create_table(
        'alerts',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('severity', sa.String(), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('data', sa.JSON(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('acknowledged_by', sa.String(), nullable=True),
        sa.Column('acknowledged_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('alerts')
    op.drop_table('generated_content')
    op.drop_table('invoices')
    op.drop_table('purchases')
    op.drop_table('carts')
    op.drop_table('cases')
    op.drop_table('sentiment_analyses')
    op.drop_table('lead_intents')
    op.drop_table('lead_classifications')
    op.drop_table('messages')
    op.drop_table('raw_messages')
    op.drop_table('conversations')
    op.drop_table('customers')
    op.drop_table('leads')

