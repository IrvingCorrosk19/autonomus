# Autonomous CRM - Parte 2: Flujos 9-22 y Recursos Adicionales

---

## **FLUJO 9: Cierre Automático de Caso**

**Responsabilidad:** Detectar resolución exitosa y cerrar tickets automáticamente

### Endpoint
```python
POST /api/v1/cases/evaluate-closure
```

### Implementación

```python
# app/services/case_closure.py
from typing import Optional
from app.schemas.case import Case, ClosureDecision

class CaseClosureService:
    """
    Evalúa si un caso puede cerrarse basándose en:
    1. Confirmación explícita del cliente ("todo bien", "resuelto", etc)
    2. Silencio del cliente después de resolución (72h)
    3. Métricas de satisfacción positivas
    """
    
    async def evaluate_closure(
        self,
        case: Case,
        latest_message: str
    ) -> ClosureDecision:
        """
        Determina si el caso debe cerrarse.
        
        Returns:
            ClosureDecision con:
            - should_close: bool
            - confidence: 0-1
            - reason: str
            - requires_survey: bool
        """
        
        # Detección de confirmación explícita
        confirmation_patterns = [
            "todo bien",
            "resuelto",
            "gracias, perfecto",
            "ya está solucionado",
            "no necesito nada más"
        ]
        
        if any(pattern in latest_message.lower() for pattern in confirmation_patterns):
            return ClosureDecision(
                should_close=True,
                confidence=0.95,
                reason="Confirmación explícita del cliente",
                requires_survey=True,
                closure_type="customer_confirmed"
            )
        
        # Usar IA para detección más sofisticada
        ai_decision = await self.ai.evaluate_case_closure(
            case_history=case.conversation_history,
            latest_message=latest_message
        )
        
        if ai_decision.should_close and ai_decision.confidence > 0.8:
            # Enviar mensaje de confirmación antes de cerrar
            await self._send_closure_confirmation(case)
            
            # Programar cierre en 24h si no hay respuesta
            await self._schedule_auto_closure(case, hours=24)
            
            return ai_decision
        
        return ClosureDecision(
            should_close=False,
            reason="Requiere más interacción"
        )
    
    async def _send_closure_confirmation(self, case: Case):
        """Envía mensaje pidiendo confirmación de cierre."""
        message = await self.ai.generate_message(
            template="closure_confirmation",
            context={"case_id": case.id, "issue": case.description},
            prompt="""
            Genera un mensaje breve preguntando si el problema está resuelto.
            Debe ser amigable y dar opción de reabrir si hay algo más.
            
            Ejemplo: "Perfecto! Me alegra haber podido ayudarte. ¿Está todo resuelto 
            o hay algo más en lo que pueda ayudarte? 😊"
            """
        )
        
        await self._send_message(case.customer, message)
    
    async def close_case(
        self,
        case: Case,
        reason: str,
        collect_feedback: bool = True
    ):
        """
        Cierra el caso y opcionalmente recopila feedback.
        """
        case.status = CaseStatus.CLOSED
        case.closed_at = datetime.utcnow()
        case.closure_reason = reason
        
        # Guardar evidencia de resolución
        await self._save_closure_evidence(case)
        
        # Enviar encuesta de satisfacción
        if collect_feedback:
            await self._send_satisfaction_survey(case)
        
        # Actualizar métricas
        await self._update_case_metrics(case)
        
        logger.info(
            "case_closed",
            case_id=case.id,
            resolution_time=case.resolution_time_hours,
            satisfaction_predicted=case.predicted_csat
        )
```

### Modelo de Datos

```python
# app/models/case.py
from sqlalchemy import Column, String, DateTime, Enum, Float
import enum

class CaseStatus(enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    WAITING_CUSTOMER = "waiting_customer"
    RESOLVED = "resolved"
    CLOSED = "closed"

class Case(Base):
    __tablename__ = "cases"
    
    id = Column(String, primary_key=True)
    customer_id = Column(String, ForeignKey("customers.id"))
    description = Column(String)
    status = Column(Enum(CaseStatus), default=CaseStatus.OPEN)
    priority = Column(Integer)  # 1-5
    
    opened_at = Column(DateTime, nullable=False)
    closed_at = Column(DateTime, nullable=True)
    resolution_time_hours = Column(Float, nullable=True)
    
    closure_reason = Column(String)
    customer_satisfaction = Column(Integer, nullable=True)  # 1-5
    predicted_csat = Column(Float)  # ML prediction
```

---

## **FLUJO 10: Nutrición Inteligente de Leads**

**Responsabilidad:** Secuencias de contenido dinámicas para educar y calentar leads

### Arquitectura de Nurturing

```python
# app/services/nurturing.py
from datetime import datetime, timedelta
from typing import List

class NurturingEngine:
    """
    Motor de nutrición con IA que adapta contenido según:
    - Comportamiento del lead (opens, clicks, respuestas)
    - Score dinámico (sube/baja según engagement)
    - Fase del buyer journey (awareness, consideration, decision)
    - Intereses detectados
    """
    
    def __init__(self):
        self.campaigns = {
            "cold_to_warm": ColdToWarmCampaign(),
            "product_education": ProductEducationCampaign(),
            "case_study_series": CaseStudyCampaign(),
            "objection_handling": ObjectionHandlingCampaign()
        }
    
    async def process_lead(self, lead: Lead):
        """
        Evalúa al lead y decide qué campaña/contenido enviar.
        """
        # Determinar fase del buyer journey
        journey_stage = await self._identify_journey_stage(lead)
        
        # Seleccionar campaña apropiada
        campaign = self._select_campaign(lead, journey_stage)
        
        # IA genera contenido personalizado
        content = await campaign.generate_next_content(lead)
        
        # Enviar en el timing óptimo
        optimal_time = await self._predict_best_send_time(lead)
        await self._schedule_send(lead, content, send_at=optimal_time)
        
        logger.info(
            "nurturing_content_scheduled",
            lead_id=lead.id,
            campaign=campaign.name,
            journey_stage=journey_stage,
            send_at=optimal_time
        )

class ColdToWarmCampaign:
    """
    Secuencia de 7 días para leads fríos.
    
    Día 1: Contenido educativo general
    Día 3: Caso de éxito relevante
    Día 5: Comparativa de soluciones
    Día 7: Oferta especial + call to action
    """
    
    async def generate_next_content(self, lead: Lead) -> NurturingContent:
        day = (datetime.now() - lead.entered_campaign_at).days
        
        if day == 0:
            return await self._generate_educational_content(lead)
        elif day == 2:
            return await self._generate_case_study(lead)
        elif day == 4:
            return await self._generate_comparison(lead)
        elif day == 6:
            return await self._generate_offer(lead)
        
        return None  # Campaña completada
    
    async def _generate_educational_content(self, lead: Lead):
        """IA genera artículo/video educativo personalizado."""
        prompt = f"""
        Genera un mensaje de nurturing educativo para:
        
        Lead: {lead.name}
        Industria: {lead.industry}
        Interés inicial: {lead.initial_interest}
        
        OBJETIVO: Educar sin vender
        FORMATO: Mensaje corto + link a recurso
        TONO: Experto pero accesible
        
        Ejemplo estructura:
        "Hola {lead.name}! 👋
        
        Vi que te interesó [producto]. Aquí tienes una guía que explica 
        [concepto clave] de forma simple.
        
        [Link a recurso]
        
        Si tienes dudas, aquí estoy!"
        """
        
        return await self.ai.generate_content(prompt)
```

### Métricas de Nurturing

```python
# Tracking de efectividad
class NurturingMetrics:
    - open_rate: float          # % que abrieron mensaje
    - click_rate: float         # % que hicieron click
    - response_rate: float      # % que respondieron
    - conversion_rate: float    # % que pasaron a MQL/SQL
    - score_improvement: int    # Cambio en lead score
    - avg_time_to_convert: int  # Días hasta conversión
```

---

## **FLUJO 11: IA Closer (Cierre de Ventas)**

**Responsabilidad:** IA especializada en cerrar ventas y manejar objeciones

### Implementación

```python
# app/services/ai_closer.py
from typing import List, Dict

class AICloser:
    """
    Agente de IA entrenado específicamente para:
    1. Detectar señales de compra
    2. Manejar objeciones comunes
    3. Crear urgencia apropiada
    4. Facilitar el cierre
    """
    
    async def respond_to_sales_opportunity(
        self,
        message: str,
        customer_context: CustomerContext,
        product_interest: Product
    ) -> ClosingResponse:
        """
        Genera respuesta optimizada para cierre de venta.
        """
        
        # Detectar objeciones en el mensaje
        objections = await self._detect_objections(message)
        
        # Detectar señales de compra
        buying_signals = await self._detect_buying_signals(message)
        
        if objections:
            # Manejar objeciones con IA
            response = await self._handle_objections(
                objections=objections,
                product=product_interest,
                customer=customer_context
            )
        elif buying_signals:
            # Cliente listo para comprar → facilitar
            response = await self._facilitate_purchase(
                product=product_interest,
                customer=customer_context
            )
        else:
            # Empujar suavemente hacia decisión
            response = await self._nudge_towards_decision(
                product=product_interest,
                customer=customer_context
            )
        
        return response
    
    async def _handle_objections(
        self,
        objections: List[str],
        product: Product,
        customer: CustomerContext
    ) -> str:
        """
        Maneja objeciones comunes con técnicas de ventas.
        
        Objeciones típicas:
        - Precio ("muy caro")
        - Timing ("no es el momento")
        - Autoridad ("tengo que consultarlo")
        - Necesidad ("no estoy seguro si lo necesito")
        - Confianza ("no los conozco")
        """
        
        objection_type = self._classify_objection(objections[0])
        
        # Base de conocimiento de rebuttals
        rebuttal_strategies = {
            "price": """
                Enfócate en valor, no precio:
                1. ROI / Ahorro a largo plazo
                2. Comparar con costo de NO tenerlo
                3. Opciones de financiamiento
                4. Garantía de satisfacción
            """,
            "timing": """
                Crear urgencia apropiada:
                1. Costo de esperar (problemas actuales)
                2. Oferta limitada (si aplica)
                3. Facilitar inicio gradual
            """,
            "authority": """
                Ayudar a justificar ante superiores:
                1. Proveer materiales de presentación
                2. Ofrecer demo/trial
                3. Compartir casos de éxito similares
            """
        }
        
        prompt = f"""
        Cliente tiene objeción de tipo: {objection_type}
        
        Mensaje exacto: "{objections[0]}"
        
        Contexto del cliente:
        - Industria: {customer.industry}
        - Tamaño: {customer.company_size}
        - Presupuesto estimado: {customer.estimated_budget}
        
        Producto: {product.name} - ${product.price}
        
        ESTRATEGIA:
        {rebuttal_strategies[objection_type]}
        
        INSTRUCCIONES:
        1. Empatiza con la objeción
        2. Usa la estrategia apropiada
        3. Incluye datos/pruebas concretas
        4. Termina con pregunta que facilite avanzar
        5. NUNCA ser insistente o agresivo
        
        TONO: Consultivo, no vendedor
        LONGITUD: 3-4 oraciones máximo
        """
        
        return await self.ai.generate_response(prompt)
    
    async def _detect_buying_signals(self, message: str) -> List[str]:
        """
        Detecta señales de alta intención de compra:
        - Preguntas sobre proceso de compra
        - Solicitud de cotización
        - Preguntas sobre plazos de entrega
        - Comparación de opciones (ej: "cuál es mejor X o Y")
        - Preguntas sobre garantía/soporte
        """
        signals = []
        
        buying_signal_patterns = {
            "purchase_process": ["cómo compro", "proceso de compra", "cómo pago"],
            "pricing_details": ["cotización", "factura", "cuánto cuesta exactamente"],
            "delivery": ["cuándo me llega", "tiempo de entrega", "envío"],
            "comparison": ["diferencia entre", "cuál es mejor", "recomiendas"],
            "guarantees": ["garantía", "devolución", "qué pasa si"]
        }
        
        for signal_type, patterns in buying_signal_patterns.items():
            if any(pattern in message.lower() for pattern in patterns):
                signals.append(signal_type)
        
        return signals
    
    async def _facilitate_purchase(
        self,
        product: Product,
        customer: CustomerContext
    ) -> str:
        """
        Cuando el cliente está listo, facilitar el proceso.
        """
        prompt = f"""
        Cliente muestra señales claras de querer comprar {product.name}.
        
        OBJETIVO: Hacer el proceso de compra lo más fácil posible
        
        MENSAJE DEBE INCLUIR:
        1. Resumen rápido de lo que va a recibir
        2. Precio final claro
        3. Opciones de pago simples
        4. Timeline de entrega
        5. Link directo para procesar orden O instrucciones claras
        6. Tranquilidad (garantías, soporte)
        
        FORMATO:
        - Bullet points para claridad
        - Call to action claro
        - Tono: Confiado pero servicial
        
        Ejemplo:
        "¡Excelente! Te confirmo los detalles:
        
        📦 {product.name}
        💰 ${product.price} (envío gratis)
        🚚 Entrega en 24-48 hrs
        ✅ Garantía 30 días
        
        Para procesar tu orden:
        👉 [Link de pago]
        
        ¿Procedo? 😊"
        """
        
        return await self.ai.generate_response(prompt)
```

### Métricas de Cierre

```python
class ClosingMetrics(Base):
    __tablename__ = "closing_metrics"
    
    conversation_id = Column(String, primary_key=True)
    objections_detected = Column(JSON)      # Lista de objeciones
    objections_overcome = Column(JSON)      # Cuáles se superaron
    buying_signals = Column(JSON)           # Señales detectadas
    close_attempted = Column(Boolean)       # Si se intentó cerrar
    close_successful = Column(Boolean)      # Si se cerró
    conversation_length = Column(Integer)   # # de mensajes
    time_to_close_minutes = Column(Float)   # Tiempo desde primer contacto
```

---

## **FLUJO 12: Recuperación de Carrito Abandonado**

**Responsabilidad:** Detectar y recuperar carritos abandonados con IA

### Implementación

```python
# app/services/cart_recovery.py
from datetime import datetime, timedelta

class CartRecoveryService:
    """
    Sistema de recuperación de carritos con secuencia inteligente:
    
    1 hora: Recordatorio suave
    24 horas: Incentivo (descuento 5-10%)
    48 horas: Urgencia (stock limitado)
    72 horas: Última oportunidad (descuento mayor)
    """
    
    async def detect_abandoned_carts(self):
        """
        Job que corre cada hora para detectar carritos abandonados.
        """
        # Carritos con productos pero sin compra en X tiempo
        abandoned = await db.query(Cart).filter(
            Cart.status == "pending",
            Cart.last_activity < datetime.now() - timedelta(hours=1),
            Cart.recovery_attempt_count < 3
        ).all()
        
        for cart in abandoned:
            await self._trigger_recovery_sequence(cart)
    
    async def _trigger_recovery_sequence(self, cart: Cart):
        """Inicia secuencia de recuperación personalizada."""
        hours_abandoned = (datetime.now() - cart.last_activity).total_seconds() / 3600
        
        if hours_abandoned >= 72:
            await self._send_final_offer(cart)
        elif hours_abandoned >= 48:
            await self._send_urgency_message(cart)
        elif hours_abandoned >= 24:
            await self._send_incentive_message(cart)
        elif hours_abandoned >= 1:
            await self._send_gentle_reminder(cart)
    
    async def _send_gentle_reminder(self, cart: Cart):
        """Recordatorio 1 hora después."""
        products_text = self._format_cart_items(cart)
        
        message = await self.ai.generate_message(
            template="cart_recovery_gentle",
            context={"cart": cart, "customer": cart.customer},
            prompt=f"""
            Genera recordatorio suave de carrito abandonado.
            
            Cliente: {cart.customer.name}
            Productos en carrito: {products_text}
            Valor total: ${cart.total_amount}
            
            TONO: Amigable, útil (no vendedor)
            OBJETIVO: Recordar sin presionar
            
            Ejemplo:
            "Hola {cart.customer.name}! 👋
            
            Vi que dejaste algunos productos en tu carrito:
            {products_text}
            
            ¿Te ayudo con algo o tienes alguna duda?
            
            [Link al carrito]"
            """
        )
        
        await self._send_message(cart.customer, message)
        cart.recovery_attempt_count += 1
    
    async def _send_incentive_message(self, cart: Cart):
        """Incentivo después de 24h."""
        discount_code = await self._generate_discount_code(cart, percentage=10)
        
        message = await self.ai.generate_message(
            template="cart_recovery_incentive",
            context={
                "cart": cart,
                "discount": 10,
                "code": discount_code
            },
            prompt=f"""
            Genera mensaje con incentivo para recuperar carrito.
            
            INCLUIR:
            - Recordatorio amigable
            - Código de descuento 10%
            - Urgencia suave (válido 24h)
            - Link directo a checkout
            
            TONO: Generoso, creando valor
            """
        )
        
        await self._send_message(cart.customer, message)
        cart.recovery_attempt_count += 1
    
    async def _send_final_offer(self, cart: Cart):
        """Última oportunidad con mejor oferta."""
        discount_code = await self._generate_discount_code(cart, percentage=15)
        
        message = await self.ai.generate_message(
            template="cart_recovery_final",
            context={
                "cart": cart,
                "discount": 15,
                "code": discount_code
            },
            prompt=f"""
            Mensaje de última oportunidad.
            
            INCLUIR:
            - Reconocimiento de que no completó compra
            - Mejor oferta (15% descuento)
            - Urgencia real (expira en 24h)
            - Opción de contacto si tiene dudas
            
            TONO: Último intento pero respetuoso
            """
        )
        
        await self._send_message(cart.customer, message)
        cart.recovery_attempt_count += 1
        cart.final_attempt = True
```

### Modelo de Datos

```python
class Cart(Base):
    __tablename__ = "carts"
    
    id = Column(String, primary_key=True)
    customer_id = Column(String, ForeignKey("customers.id"))
    items = Column(JSON)  # [{"product_id": "...", "quantity": 2}]
    total_amount = Column(Float)
    
    created_at = Column(DateTime)
    last_activity = Column(DateTime)
    status = Column(String)  # pending, recovered, abandoned
    
    recovery_attempt_count = Column(Integer, default=0)
    discount_codes_used = Column(JSON)
    recovered_at = Column(DateTime, nullable=True)
    recovery_channel = Column(String, nullable=True)  # whatsapp, email, etc
```

---

## **FLUJO 13: Recordatorios de Pago**

**Responsabilidad:** Recordatorios automáticos de facturas pendientes

### Implementación

```python
# app/services/payment_reminder.py

class PaymentReminderService:
    """
    Secuencia de recordatorios de pago:
    
    - 7 días antes: Recordatorio amistoso
    - 3 días antes: Recordatorio con detalles
    - Día de vencimiento: Urgencia educada
    - 1 día después: Cortés pero firme
    - 7 días después: Escalamiento
    """
    
    async def send_reminders(self):
        """Job diario para enviar recordatorios."""
        
        # Facturas próximas a vencer (7 días)
        upcoming = await self._get_invoices_due_in(days=7)
        for invoice in upcoming:
            await self._send_friendly_reminder(invoice)
        
        # Facturas vencidas (1 día)
        overdue_1d = await self._get_overdue_invoices(days=1)
        for invoice in overdue_1d:
            await self._send_polite_overdue_reminder(invoice)
        
        # Facturas muy vencidas (7+ días)
        overdue_7d = await self._get_overdue_invoices(days=7)
        for invoice in overdue_7d:
            await self._escalate_overdue_invoice(invoice)
    
    async def _send_friendly_reminder(self, invoice: Invoice):
        """Recordatorio 7 días antes de vencimiento."""
        message = await self.ai.generate_message(
            template="payment_reminder_upcoming",
            context={"invoice": invoice},
            prompt=f"""
            Genera recordatorio de pago amigable.
            
            Factura #{invoice.number}
            Monto: ${invoice.amount}
            Vence: {invoice.due_date}
            
            TONO: Servicial, no cobranza
            OBJETIVO: Recordar para evitar retrasos
            
            DEBE INCLUIR:
            - Resumen de factura
            - Métodos de pago disponibles
            - Link de pago directo
            - Agradecimiento por ser cliente
            
            Ejemplo:
            "Hola {invoice.customer.name}!
            
            Te recuerdo que tu factura #{invoice.number} de ${invoice.amount} 
            vence el {invoice.due_date}.
            
            Puedes pagar fácilmente aquí: [link]
            
            Métodos: Tarjeta, transferencia, ACH
            
            ¡Gracias por tu preferencia! 😊"
            """
        )
        
        await self._send_message(invoice.customer, message)
    
    async def _send_polite_overdue_reminder(self, invoice: Invoice):
        """Recordatorio cortés para facturas vencidas recientemente."""
        message = await self.ai.generate_message(
            template="payment_reminder_overdue",
            context={"invoice": invoice},
            prompt=f"""
            Genera recordatorio para factura vencida hace 1 día.
            
            TONO: Cortés pero firme
            ASUNCIÓN: Puede ser olvido genuino
            
            DEBE INCLUIR:
            - Mención de que venció ayer
            - Monto + recargo por mora (si aplica)
            - Urgencia de regularizar
            - Facilidades de pago si existen
            - Opción de contactar si hay problema
            
            NO DEBE:
            - Ser agresivo o amenazante
            - Asumir mala fe
            """
        )
        
        await self._send_message(invoice.customer, message)
        
        # Notificar al equipo de finanzas
        await self._notify_finance_team(invoice)
```

---

## **FLUJO 14: Generación Automática de Contenido**

**Responsabilidad:** Crear contenido visual y textual con IA para marketing

### Endpoint
```python
POST /api/v1/content/generate
```

### Request
```json
{
  "content_type": "image|video|text|carousel",
  "purpose": "product_launch|promotion|educational|engagement",
  "product_id": "prod_123",
  "target_audience": "millennials_tech_savvy",
  "tone": "professional|casual|humorous",
  "platform": "instagram|facebook|tiktok"
}
```

### Implementación

```python
# app/services/content_generator.py
from typing import List
from app.ai.image_gen import DALLEAdapter, MidjourneyAdapter
from app.ai.video_gen import RunwayAdapter

class ContentGenerator:
    """
    Genera contenido multimodal para redes sociales:
    - Imágenes (DALL-E, Midjourney)
    - Videos cortos (Runway, Pika)
    - Copy (GPT-5)
    - Carruseles
    """
    
    def __init__(self):
        self.image_gen = DALLEAdapter()
        self.video_gen = RunwayAdapter()
        self.text_gen = GPT5Adapter()
    
    async def generate_product_post(
        self,
        product: Product,
        platform: str,
        purpose: str
    ) -> GeneratedContent:
        """
        Genera post completo (imagen + copy) para producto.
        """
        
        # 1. Generar imagen del producto
        image_prompt = await self._build_image_prompt(product, platform)
        image_url = await self.image_gen.generate(
            prompt=image_prompt,
            style="photorealistic" if platform == "instagram" else "creative"
        )
        
        # 2. Generar copy
        copy = await self._generate_copy(product, platform, purpose)
        
        # 3. Generar hashtags
        hashtags = await self._generate_hashtags(product, platform)
        
        # 4. Guardar en storage
        asset = await self._save_to_storage(
            image_url=image_url,
            copy=copy,
            hashtags=hashtags,
            product_id=product.id
        )
        
        return GeneratedContent(
            asset_url=asset.url,
            copy=copy,
            hashtags=hashtags,
            platform=platform,
            recommended_post_time=await self._predict_best_time(platform)
        )
    
    async def _build_image_prompt(
        self,
        product: Product,
        platform: str
    ) -> str:
        """
        Construye prompt optimizado para generación de imagen.
        """
        platform_specs = {
            "instagram": "1:1 aspect ratio, vibrant colors, lifestyle context",
            "facebook": "16:9 aspect ratio, clear product focus",
            "tiktok": "9:16 vertical, dynamic, youth-oriented"
        }
        
        return f"""
        Product: {product.name}
        Category: {product.category}
        Key features: {product.key_features}
        
        Platform: {platform}
        Requirements: {platform_specs[platform]}
        
        Style: Professional product photography
        Lighting: Natural, soft shadows
        Background: Clean, modern, branded
        Composition: Rule of thirds
        
        Additional elements:
        - Show product in use if applicable
        - Include lifestyle elements
        - Brand colors: {product.brand_colors}
        
        Quality: Photorealistic, 4K, professional
        """
    
    async def _generate_copy(
        self,
        product: Product,
        platform: str,
        purpose: str
    ) -> str:
        """IA genera copy optimizado para plataforma."""
        
        platform_guidelines = {
            "instagram": {
                "max_length": 2200,
                "optimal_length": 150,
                "tone": "visual, storytelling, emojis ok",
                "cta_style": "link in bio"
            },
            "facebook": {
                "max_length": 63206,
                "optimal_length": 250,
                "tone": "conversational, detailed",
                "cta_style": "direct link"
            },
            "tiktok": {
                "max_length": 150,
                "optimal_length": 100,
                "tone": "casual, trendy, hooks matter",
                "cta_style": "comment or duet"
            }
        }
        
        guidelines = platform_guidelines[platform]
        
        prompt = f"""
        Genera copy para post de {platform} sobre:
        
        PRODUCTO: {product.name}
        PROPÓSITO: {purpose}  # launch, promotion, education, etc
        
        GUIDELINES DE {platform.upper()}:
        - Longitud óptima: {guidelines['optimal_length']} caracteres
        - Tono: {guidelines['tone']}
        - CTA: {guidelines['cta_style']}
        
        ESTRUCTURA:
        1. Hook (primera línea debe captar atención)
        2. Beneficio clave (qué gana el usuario)
        3. Descripción breve
        4. Call to action
        5. Hashtags (generar por separado)
        
        REGLAS:
        - Emojis: Sí (pero no exagerar)
        - Longitud: {guidelines['optimal_length']}-{guidelines['optimal_length']*1.5} caracteres
        - Mencionar precio solo si es muy competitivo
        - Enfocarse en valor, no features
        """
        
        return await self.text_gen.generate(prompt)
    
    async def generate_video_ad(
        self,
        product: Product,
        duration_seconds: int = 15
    ) -> str:
        """
        Genera video corto de producto usando IA.
        
        Pasos:
        1. Generar storyboard con GPT
        2. Generar frames clave con DALL-E
        3. Animar con Runway/Pika
        4. Añadir voiceover con ElevenLabs
        5. Añadir música de fondo
        """
        
        # 1. Storyboard
        storyboard = await self._generate_storyboard(product, duration_seconds)
        
        # 2. Generar frames
        frames = []
        for scene in storyboard.scenes:
            frame = await self.image_gen.generate(scene.visual_description)
            frames.append(frame)
        
        # 3. Animar
        video_url = await self.video_gen.animate_frames(
            frames=frames,
            transitions=storyboard.transitions,
            duration=duration_seconds
        )
        
        # 4. Voiceover
        script = storyboard.narration
        voiceover_url = await self.voice_gen.generate(
            text=script,
            voice="professional_male"  # o female, según brand
        )
        
        # 5. Combinar todo
        final_video = await self._combine_video_elements(
            video_url=video_url,
            voiceover_url=voiceover_url,
            background_music="upbeat_commercial"
        )
        
        return final_video
```

---

## **FLUJO 15: Publicación Automática en Redes**

**Responsabilidad:** Publicar contenido en plataformas sociales vía APIs

### Implementación

```python
# app/services/publisher.py
from app.integrations.meta_graph import MetaGraphAPI
from app.integrations.tiktok import TikTokAPI

class SocialMediaPublisher:
    """
    Publica contenido en múltiples plataformas automáticamente.
    """
    
    def __init__(self):
        self.meta = MetaGraphAPI()  # Facebook + Instagram
        self.tiktok = TikTokAPI()
    
    async def publish_post(
        self,
        content: GeneratedContent,
        platforms: List[str],
        schedule_time: Optional[datetime] = None
    ) -> PublicationResult:
        """
        Publica o programa contenido en plataformas especificadas.
        """
        results = {}
        
        for platform in platforms:
            try:
                if schedule_time and schedule_time > datetime.now():
                    # Programar para después
                    result = await self._schedule_post(
                        platform=platform,
                        content=content,
                        schedule_time=schedule_time
                    )
                else:
                    # Publicar inmediatamente
                    result = await self._publish_now(platform, content)
                
                results[platform] = result
                
            except Exception as e:
                logger.error(
                    "publication_failed",
                    platform=platform,
                    error=str(e)
                )
                results[platform] = {"status": "error", "error": str(e)}
        
        return PublicationResult(results=results)
    
    async def _publish_now(
        self,
        platform: str,
        content: GeneratedContent
    ) -> Dict:
        """Publicación inmediata."""
        
        if platform == "instagram":
            return await self.meta.publish_instagram_post(
                image_url=content.asset_url,
                caption=f"{content.copy}\n\n{' '.join(content.hashtags)}",
                location_id=content.location_id if content.location_id else None
            )
        
        elif platform == "facebook":
            return await self.meta.publish_facebook_post(
                image_url=content.asset_url,
                message=f"{content.copy}\n\n{' '.join(content.hashtags)}",
                link=content.link if content.link else None
            )
        
        elif platform == "tiktok":
            return await self.tiktok.upload_video(
                video_url=content.asset_url,
                caption=content.copy,
                hashtags=content.hashtags
            )
        
        else:
            raise ValueError(f"Platform {platform} not supported")
```

### Integración Meta Graph API

```python
# app/integrations/meta_graph.py
import httpx

class MetaGraphAPI:
    BASE_URL = "https://graph.facebook.com/v18.0"
    
    async def publish_instagram_post(
        self,
        image_url: str,
        caption: str,
        location_id: Optional[str] = None
    ):
        """
        Publica imagen en Instagram Business Account.
        
        Proceso de 2 pasos:
        1. Create Media Container
        2. Publish Container
        """
        
        # Paso 1: Crear container
        container_payload = {
            "image_url": image_url,
            "caption": caption,
            "access_token": settings.META_ACCESS_TOKEN
        }
        
        if location_id:
            container_payload["location_id"] = location_id
        
        async with httpx.AsyncClient() as client:
            container_response = await client.post(
                f"{self.BASE_URL}/{settings.INSTAGRAM_BUSINESS_ACCOUNT_ID}/media",
                data=container_payload
            )
            container_response.raise_for_status()
            container_id = container_response.json()["id"]
            
            # Paso 2: Publicar
            publish_response = await client.post(
                f"{self.BASE_URL}/{settings.INSTAGRAM_BUSINESS_ACCOUNT_ID}/media_publish",
                data={
                    "creation_id": container_id,
                    "access_token": settings.META_ACCESS_TOKEN
                }
            )
            publish_response.raise_for_status()
            
            return publish_response.json()
```

---

## **FLUJO 16: Programador Inteligente de Publicación**

**Responsabilidad:** Predecir mejor momento para publicar usando ML

### Implementación

```python
# app/services/scheduler.py
from sklearn.ensemble import RandomForestRegressor
import pandas as pd

class IntelligentScheduler:
    """
    Predice el mejor momento para publicar basándose en:
    - Engagement histórico por hora/día
    - Audiencia activa (Analytics API)
    - Tipo de contenido
    - Competencia (actividad de otros posts)
    """
    
    def __init__(self):
        self.model = self._load_or_train_model()
    
    async def predict_best_time(
        self,
        platform: str,
        content_type: str,
        target_audience: str
    ) -> datetime:
        """
        Retorna el mejor momento para publicar en las próximas 7 días.
        """
        
        # Obtener datos históricos de engagement
        historical_data = await self._get_historical_engagement(
            platform=platform,
            days=90
        )
        
        # Obtener patrones de audiencia
        audience_insights = await self._get_audience_insights(platform)
        
        # Generar candidatos (próximos 7 días, cada hora)
        candidates = self._generate_time_candidates(days=7)
        
        # Predecir engagement para cada candidato
        predictions = []
        for candidate_time in candidates:
            features = self._extract_features(
                time=candidate_time,
                platform=platform,
                content_type=content_type,
                historical_data=historical_data,
                audience_insights=audience_insights
            )
            
            predicted_engagement = self.model.predict([features])[0]
            
            predictions.append({
                "time": candidate_time,
                "predicted_engagement": predicted_engagement
            })
        
        # Retornar el mejor
        best = max(predictions, key=lambda x: x["predicted_engagement"])
        
        logger.info(
            "optimal_time_predicted",
            platform=platform,
            best_time=best["time"],
            predicted_engagement=best["predicted_engagement"]
        )
        
        return best["time"]
    
    def _extract_features(
        self,
        time: datetime,
        platform: str,
        content_type: str,
        historical_data: pd.DataFrame,
        audience_insights: Dict
    ) -> List[float]:
        """
        Extrae features para el modelo ML:
        - hour_of_day (0-23)
        - day_of_week (0-6)
        - is_weekend (0/1)
        - avg_engagement_this_hour (histórico)
        - audience_active_percentage (de Analytics API)
        - content_type_encoded
        - season (0-3)
        """
        
        hour = time.hour
        day_of_week = time.weekday()
        is_weekend = 1 if day_of_week >= 5 else 0
        
        # Engagement promedio para esta hora/día (histórico)
        avg_engagement = historical_data[
            (historical_data['hour'] == hour) &
            (historical_data['day_of_week'] == day_of_week)
        ]['engagement'].mean()
        
        # % de audiencia activa (de Meta/TikTok Analytics)
        audience_active = audience_insights.get(f"{day_of_week}_{hour}", 0)
        
        # Codificar tipo de contenido
        content_type_map = {"image": 0, "video": 1, "carousel": 2, "reel": 3}
        content_encoded = content_type_map.get(content_type, 0)
        
        # Estacionalidad
        season = (time.month % 12) // 3
        
        return [
            hour,
            day_of_week,
            is_weekend,
            avg_engagement,
            audience_active,
            content_encoded,
            season
        ]
    
    def _train_model(self, historical_data: pd.DataFrame):
        """
        Entrena modelo de predicción de engagement.
        """
        X = historical_data[[
            'hour', 'day_of_week', 'is_weekend',
            'avg_engagement', 'audience_active',
            'content_type', 'season'
        ]]
        y = historical_data['engagement']
        
        model = RandomForestRegressor(n_estimators=100, max_depth=10)
        model.fit(X, y)
        
        return model
```

---

## **FLUJO 17: Respuesta Automática a Comentarios**

**Responsabilidad:** Monitorear y responder comentarios en posts automáticamente

### Implementación

```python
# app/services/comment_responder.py

class CommentResponder:
    """
    Responde automáticamente a comentarios en redes sociales.
    
    Capacidades:
    - Detectar preguntas frecuentes
    - Responder con información relevante
    - Escalar comentarios negativos
    - Agradecer comentarios positivos
    - Detectar spam
    """
    
    async def process_comment(
        self,
        comment: Comment,
        post: Post
    ):
        """
        Procesa un comentario nuevo y decide si/cómo responder.
        """
        
        # 1. Clasificar tipo de comentario
        comment_type = await self._classify_comment(comment)
        
        # 2. Detectar sentimiento
        sentiment = await self.sentiment_analyzer.analyze(comment.text)
        
        # 3. Decidir acción
        if comment_type == "spam":
            await self._hide_or_delete_comment(comment)
            return
        
        if comment_type == "question":
            response = await self._answer_question(comment, post)
            await self._reply_to_comment(comment, response)
        
        elif comment_type == "complaint" or sentiment.score < -0.5:
            # Respuesta empática + escalamiento
            response = await self._handle_complaint(comment)
            await self._reply_to_comment(comment, response)
            await self._escalate_to_team(comment, "negative_comment")
        
        elif comment_type == "praise" or sentiment.score > 0.7:
            response = await self._thank_positive_comment(comment)
            await self._reply_to_comment(comment, response)
        
        else:
            # Comentario neutral, IA decide si vale la pena responder
            should_respond = await self._should_respond_to_neutral(comment)
            if should_respond:
                response = await self._generate_contextual_response(comment, post)
                await self._reply_to_comment(comment, response)
    
    async def _answer_question(
        self,
        comment: Comment,
        post: Post
    ) -> str:
        """
        Responde preguntas comunes automáticamente.
        """
        
        # Base de conocimiento de FAQs
        faq_match = await self.knowledge_base.search_faq(comment.text)
        
        if faq_match and faq_match.confidence > 0.8:
            # Pregunta frecuente con respuesta conocida
            return await self._personalize_faq_response(
                faq_answer=faq_match.answer,
                commenter_name=comment.author_name
            )
        
        # Si no hay match en FAQs, usar IA
        prompt = f"""
        Usuario preguntó en post de Instagram:
        
        POST: {post.caption}
        PRODUCTO: {post.product.name if post.product else "N/A"}
        
        COMENTARIO: "{comment.text}"
        
        CONTEXTO: Comentario público en red social
        
        INSTRUCCIONES:
        1. Responde de forma breve (1-2 oraciones)
        2. Tono amigable, profesional
        3. Usa el nombre del usuario si está disponible: {comment.author_name}
        4. Si la pregunta requiere info privada (precio personalizado, etc), 
           pídele que te envíe DM
        5. Agradece su interés
        
        EJEMPLOS:
        Q: "Cuánto cuesta?"
        A: "Hola Juan! Los precios varían según configuración. Te envío info por DM 😊"
        
        Q: "Tienen en color azul?"
        A: "Sí María! Tenemos en azul, rojo y negro. ¿Cuál prefieres?"
        """
        
        return await self.ai.generate_response(prompt)
    
    async def _handle_complaint(self, comment: Comment) -> str:
        """
        Maneja comentarios negativos con empatía.
        """
        prompt = f"""
        Cliente dejó comentario negativo:
        
        "{comment.text}"
        
        OBJETIVO:
        1. Mostrar empatía
        2. Disculparse si es apropiado (sin admitir culpa legal)
        3. Ofrecer resolución por DM o privado
        4. Mantener profesionalismo
        
        TONO: Empático, profesional, no defensivo
        LONGITUD: 2-3 oraciones
        
        IMPORTANTE: Llevar conversación a DM para resolver privadamente
        
        Ejemplo:
        "Lamentamos mucho tu experiencia, [nombre]. Tu satisfacción es importante 
        para nosotros. ¿Podrías enviarnos un DM para ayudarte personalmente? 🙏"
        """
        
        return await self.ai.generate_response(prompt)
```

---

## **FLUJO 18: Deduplicación Automática**

**Responsabilidad:** Identificar y fusionar registros duplicados

### Implementación

```python
# app/services/deduplicator.py
from fuzzywuzzy import fuzz

class Deduplicator:
    """
    Detecta y fusiona duplicados usando:
    - Fuzzy matching en nombres
    - Comparación de emails/teléfonos
    - IA para casos ambiguos
    """
    
    async def find_duplicates(self) -> List[DuplicateGroup]:
        """
        Job que corre diariamente para detectar duplicados.
        """
        
        # Obtener todos los leads/contactos
        all_contacts = await db.query(Contact).all()
        
        duplicates = []
        processed = set()
        
        for contact in all_contacts:
            if contact.id in processed:
                continue
            
            # Buscar potenciales duplicados
            potential_dupes = await self._find_potential_duplicates(contact)
            
            if potential_dupes:
                # Usar IA para confirmar si son duplicados
                confirmed_dupes = await self._confirm_duplicates_with_ai(
                    contact,
                    potential_dupes
                )
                
                if confirmed_dupes:
                    duplicates.append(DuplicateGroup(
                        primary=contact,
                        duplicates=confirmed_dupes
                    ))
                    
                    processed.update([d.id for d in confirmed_dupes])
        
        return duplicates
    
    async def _find_potential_duplicates(
        self,
        contact: Contact
    ) -> List[Contact]:
        """
        Encuentra potenciales duplicados usando reglas básicas.
        """
        potentials = []
        
        # Regla 1: Email exacto
        if contact.email:
            email_matches = await db.query(Contact).filter(
                Contact.email == contact.email,
                Contact.id != contact.id
            ).all()
            potentials.extend(email_matches)
        
        # Regla 2: Teléfono exacto
        if contact.phone:
            phone_matches = await db.query(Contact).filter(
                Contact.phone == contact.phone,
                Contact.id != contact.id
            ).all()
            potentials.extend(phone_matches)
        
        # Regla 3: Nombre muy similar (fuzzy match)
        all_contacts = await db.query(Contact).filter(
            Contact.id != contact.id
        ).all()
        
        for other in all_contacts:
            similarity = fuzz.ratio(
                contact.name.lower(),
                other.name.lower()
            )
            
            if similarity > 85:  # 85% similar
                potentials.append(other)
        
        return list(set(potentials))  # Dedup la lista de potenciales
    
    async def _confirm_duplicates_with_ai(
        self,
        contact: Contact,
        potentials: List[Contact]
    ) -> List[Contact]:
        """
        IA decide si son duplicados reales o falsos positivos.
        """
        confirmed = []
        
        for potential in potentials:
            prompt = f"""
            Determina si estos dos registros son la misma persona:
            
            REGISTRO 1:
            - Nombre: {contact.name}
            - Email: {contact.email or "N/A"}
            - Teléfono: {contact.phone or "N/A"}
            - Empresa: {contact.company or "N/A"}
            - Dirección: {contact.address or "N/A"}
            
            REGISTRO 2:
            - Nombre: {potential.name}
            - Email: {potential.email or "N/A"}
            - Teléfono: {potential.phone or "N/A"}
            - Empresa: {potential.company or "N/A"}
            - Dirección: {potential.address or "N/A"}
            
            CRITERIOS:
            - Email o teléfono idéntico = casi seguro duplicado
            - Nombre muy similar + mismo empresa = probablemente duplicado
            - Pequeñas variaciones (typos, abreviaturas) = considerar duplicado
            - Personas diferentes con apellido común = NO duplicado
            
            RESPONDE JSON:
            {{
              "is_duplicate": true/false,
              "confidence": 0.95,
              "reasoning": "Email idéntico y nombre similar con typo"
            }}
            """
            
            result = await self.ai.evaluate(prompt)
            
            if result.is_duplicate and result.confidence > 0.8:
                confirmed.append(potential)
        
        return confirmed
    
    async def merge_duplicates(
        self,
        primary: Contact,
        duplicates: List[Contact]
    ):
        """
        Fusiona duplicados en el registro primario.
        
        Estrategia:
        - Primario: El más completo o más reciente
        - Consolidar todos los campos no-null
        - Mantener historial de interacciones de todos
        - Soft-delete los duplicados (no eliminar físicamente)
        """
        
        # Consolidar datos
        merged_data = self._consolidate_fields(primary, duplicates)
        
        # Actualizar primario
        for field, value in merged_data.items():
            setattr(primary, field, value)
        
        # Transferir historial
        for dupe in duplicates:
            await self._transfer_history(from_contact=dupe, to_contact=primary)
        
        # Marcar duplicados como merged
        for dupe in duplicates:
            dupe.status = "merged"
            dupe.merged_into = primary.id
            dupe.merged_at = datetime.utcnow()
        
        await db.commit()
        
        logger.info(
            "duplicates_merged",
            primary_id=primary.id,
            merged_count=len(duplicates)
        )
```

---

## **FLUJO 19: Limpieza y Normalización de Datos**

**Responsabilidad:** Estandarizar y corregir datos automáticamente

### Implementación

```python
# app/services/data_cleaner.py
import re
import phonenumbers

class DataCleaner:
    """
    Limpia y normaliza datos:
    - Emails: lowercase, trim, validación
    - Teléfonos: formato internacional estándar
    - Nombres: capitalización correcta
    - Direcciones: estandarización
    """
    
    async def clean_contact(self, contact: Contact) -> Contact:
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
        
        return contact
    
    def _clean_email(self, email: str) -> str:
        """
        Limpia y valida email.
        """
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
                logger.info("email_typo_corrected", original=email, corrected=email)
        
        return email
    
    def _clean_phone(
        self,
        phone: str,
        default_country: str = "PA"
    ) -> str:
        """
        Normaliza teléfono a formato internacional E.164.
        
        Ejemplo: "+507 6123-4567" → "+50761234567"
        """
        try:
            # Parsear usando librería phonenumbers
            parsed = phonenumbers.parse(phone, default_country)
            
            # Validar
            if not phonenumbers.is_valid_number(parsed):
                logger.warning("invalid_phone_number", phone=phone)
                return None
            
            # Formatear a E.164
            formatted = phonenumbers.format_number(
                parsed,
                phonenumbers.PhoneNumberFormat.E164
            )
            
            return formatted
            
        except phonenumbers.phonenumberutil.NumberParseException:
            logger.warning("phone_parse_error", phone=phone)
            return None
    
    def _clean_name(self, name: str) -> str:
        """
        Capitaliza nombre correctamente.
        
        "JUAN PÉREZ" → "Juan Pérez"
        "maria rodriguez" → "Maria Rodriguez"
        """
        # Title case básico
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
    
    async def _ai_assisted_cleaning(self, contact: Contact) -> Contact:
        """
        IA ayuda con casos ambiguos o complejos.
        
        Ejemplo: Detectar si "Apple" es empresa o apellido
        """
        prompt = f"""
        Revisa y sugiere correcciones para este contacto:
        
        Nombre: {contact.name}
        Email: {contact.email}
        Teléfono: {contact.phone}
        Empresa: {contact.company}
        
        INSTRUCCIONES:
        1. Detecta inconsistencias obvias
        2. Sugiere formato correcto
        3. Identifica campos en lugar equivocado (ej: empresa en campo nombre)
        
        RESPONDE JSON:
        {{
          "corrections": {{
            "name": "Nombre corregido",
            "company": "Empresa corregida"
          }},
          "confidence": 0.9,
          "issues_found": ["nombre all caps", "empresa no reconocida"]
        }}
        """
        
        result = await self.ai.evaluate(prompt)
        
        if result.confidence > 0.8:
            for field, corrected_value in result.corrections.items():
                setattr(contact, field, corrected_value)
        
        return contact
```

---

## **FLUJO 20: Enriquecimiento de Datos**

**Responsabilidad:** Agregar atributos predictivos y datos externos

### Implementación

```python
# app/services/enrichment.py
from typing import Dict

class DataEnrichmentService:
    """
    Enriquece contactos con:
    - Poder adquisitivo estimado
    - Customer Lifetime Value (CLV) predicho
    - Intereses/preferencias detectados
    - Datos demográficos
    - Información de empresa (si B2B)
    """
    
    async def enrich_contact(self, contact: Contact) -> Contact:
        """
        Enriquece contacto con múltiples fuentes.
        """
        
        # 1. Enriquecimiento basado en datos públicos
        if contact.email:
            public_data = await self._enrich_from_email(contact.email)
            contact.social_profiles = public_data.get("social_profiles")
            contact.company_info = public_data.get("company")
        
        # 2. Predicciones de ML
        contact.predicted_clv = await self._predict_clv(contact)
        contact.purchasing_power = await self._estimate_purchasing_power(contact)
        
        # 3. Intereses detectados de conversaciones
        contact.interests = await self._detect_interests(contact)
        
        # 4. Segmentación automática
        contact.segment = await self._assign_segment(contact)
        
        return contact
    
    async def _enrich_from_email(self, email: str) -> Dict:
        """
        Usa APIs como Clearbit, FullContact para enriquecer.
        """
        # Ejemplo con Clearbit API
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://person.clearbit.com/v2/combined/find?email={email}",
                headers={"Authorization": f"Bearer {settings.CLEARBIT_API_KEY}"}
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "social_profiles": {
                        "linkedin": data.get("person", {}).get("linkedin", {}).get("handle"),
                        "twitter": data.get("person", {}).get("twitter", {}).get("handle")
                    },
                    "company": {
                        "name": data.get("company", {}).get("name"),
                        "domain": data.get("company", {}).get("domain"),
                        "size": data.get("company", {}).get("metrics", {}).get("employees")
                    }
                }
        
        return {}
    
    async def _predict_clv(self, contact: Contact) -> float:
        """
        Predice Customer Lifetime Value usando ML.
        
        Features:
        - Frecuencia de compra histórica
        - Valor promedio de orden
        - Antigüedad del cliente
        - Engagement en marketing
        - Categorías de productos comprados
        """
        
        # Si es cliente nuevo, usar modelo basado en leads similares
        if not contact.purchase_history:
            return await self._predict_clv_new_customer(contact)
        
        features = {
            "purchase_frequency": len(contact.purchases),
            "avg_order_value": sum(p.amount for p in contact.purchases) / len(contact.purchases),
            "customer_age_days": (datetime.now() - contact.created_at).days,
            "email_open_rate": contact.email_engagement.open_rate if contact.email_engagement else 0,
            "product_categories": len(set(p.product.category for p in contact.purchases))
        }
        
        # Modelo pre-entrenado
        predicted_clv = self.clv_model.predict([list(features.values())])[0]
        
        return round(predicted_clv, 2)
    
    async def _detect_interests(self, contact: Contact) -> List[str]:
        """
        Detecta intereses analizando conversaciones y comportamiento.
        """
        
        # Obtener todas las conversaciones
        conversations = await db.query(Message).filter(
            Message.customer_id == contact.id
        ).all()
        
        all_messages = " ".join([m.content for m in conversations])
        
        # IA extrae temas/intereses
        prompt = f"""
        Analiza estas conversaciones y extrae los intereses/preferencias del cliente:
        
        CONVERSACIONES:
        {all_messages[:2000]}  # Limitar a 2000 chars
        
        CONTEXTO: Cliente de {contact.company or "particular"}
        
        INSTRUCCIONES:
        1. Identifica temas recurrentes
        2. Detecta preferencias mencionadas
        3. Infiere intereses basándose en preguntas/comentarios
        
        RESPONDE JSON:
        {{
          "interests": ["technology", "sustainability", "premium_products"],
          "preferences": {{
            "price_sensitivity": "low",
            "brand_loyalty": "high",
            "decision_speed": "fast"
          }}
        }}
        """
        
        result = await self.ai.extract_insights(prompt)
        
        return result.interests
```

---

## **FLUJO 21: Predicción de Cierre de Venta**

**Responsabilidad:** Predecir probabilidad de cierre usando ML

### Implementación

```python
# app/services/sales_predictor.py
from sklearn.ensemble import GradientBoostingClassifier
import numpy as np

class SalesPredictor:
    """
    Modelo ML que predice probabilidad de cierre de una oportunidad.
    
    Features usadas:
    - Lead score
    - Engagement (emails abiertos, respuestas, etc)
    - Tiempo en pipeline
    - Valor de oportunidad
    - Sentimiento promedio
    - Cantidad de interacciones
    - Competencia identificada
    """
    
    def __init__(self):
        self.model = self._load_model()
    
    async def predict_close_probability(
        self,
        opportunity: Opportunity
    ) -> ClosePrediction:
        """
        Predice probabilidad de cierre (0-100%).
        """
        
        # Extraer features
        features = await self._extract_features(opportunity)
        
        # Predecir
        probability = self.model.predict_proba([features])[0][1]  # Prob de cierre
        
        # Interpretar
        if probability > 0.8:
            likelihood = "very_high"
            recommendation = "Priorizar, listo para cerrar"
        elif probability > 0.6:
            likelihood = "high"
            recommendation = "Empujar hacia cierre esta semana"
        elif probability > 0.4:
            likelihood = "medium"
            recommendation = "Continuar nurturing, no forzar cierre"
        else:
            likelihood = "low"
            recommendation = "Re-calificar o mover a nurturing de largo plazo"
        
        return ClosePrediction(
            probability=round(probability * 100, 2),
            likelihood=likelihood,
            recommendation=recommendation,
            key_factors=self._identify_key_factors(features)
        )
    
    async def _extract_features(
        self,
        opportunity: Opportunity
    ) -> List[float]:
        """
        Extrae features numéricas para el modelo.
        """
        
        contact = opportunity.contact
        
        return [
            # Lead quality
            contact.lead_score / 100,
            
            # Engagement
            contact.email_open_rate if contact.email_engagement else 0,
            contact.message_response_rate if contact.message_stats else 0,
            
            # Temporal
            (datetime.now() - opportunity.created_at).days,  # Días en pipeline
            1 if (datetime.now() - opportunity.last_interaction).days < 7 else 0,  # Activo recientemente
            
            # Valor
            np.log1p(opportunity.estimated_value),  # Log del valor
            
            # Sentimiento
            opportunity.avg_sentiment_score,
            
            # Interacciones
            opportunity.interaction_count,
            
            # Competencia
            1 if opportunity.has_identified_competition else 0,
            
            # Decisión
            1 if opportunity.decision_maker_engaged else 0,
            
            # Urgencia
            opportunity.urgency_score / 10
        ]
    
    def _identify_key_factors(self, features: List[float]) -> List[str]:
        """
        Identifica los factores más importantes para la predicción.
        """
        # Feature importance del modelo
        importances = self.model.feature_importances_
        
        feature_names = [
            "lead_score", "email_engagement", "message_response",
            "days_in_pipeline", "recent_activity", "deal_value",
            "sentiment", "interaction_count", "competition",
            "decision_maker", "urgency"
        ]
        
        # Top 3 factores
        top_indices = np.argsort(importances)[-3:][::-1]
        
        return [feature_names[i] for i in top_indices]
```

---

## **FLUJO 22: Alertas Inteligentes**

**Responsabilidad:** Detectar anomalías y enviar notificaciones proactivas

### Implementación

```python
# app/services/alerts.py
from typing import List
from enum import Enum

class AlertType(Enum):
    SALES_DROP = "sales_drop"
    ANGRY_CUSTOMER = "angry_customer"
    CHURN_RISK = "churn_risk"
    HOT_LEAD = "hot_lead"
    INVENTORY_LOW = "inventory_low"
    COMPETITOR_MENTION = "competitor_mention"
    PAYMENT_OVERDUE = "payment_overdue"

class IntelligentAlerts:
    """
    Sistema de alertas que detecta:
    - Ventas inusualmente bajas
    - Clientes molestos/riesgo de churn
    - Leads extremadamente calientes
    - Stock bajo
    - Menciones de competencia
    - Pagos vencidos
    """
    
    async def check_all_alerts(self):
        """
        Job que corre cada hora para verificar condiciones de alerta.
        """
        
        # Alertas de ventas
        await self._check_sales_anomalies()
        
        # Alertas de clientes
        await self._check_customer_risks()
        
        # Alertas de leads
        await self._check_hot_leads()
        
        # Alertas operacionales
        await self._check_inventory()
        await self._check_overdue_payments()
    
    async def _check_sales_anomalies(self):
        """
        Detecta drops anormales en ventas.
        """
        
        # Ventas últimos 7 días vs promedio histórico
        recent_sales = await self._get_sales_last_n_days(7)
        historical_avg = await self._get_avg_daily_sales(days=90)
        
        drop_percentage = ((historical_avg - recent_sales) / historical_avg) * 100
        
        if drop_percentage > 30:  # 30% menos que promedio
            await self._send_alert(
                alert_type=AlertType.SALES_DROP,
                severity="high",
                message=f"⚠️ Ventas bajaron {drop_percentage:.1f}% vs promedio histórico",
                data={
                    "recent_sales": recent_sales,
                    "historical_avg": historical_avg,
                    "drop_percentage": drop_percentage
                },
                recipients=["sales_manager@company.com"]
            )
    
    async def _check_customer_risks(self):
        """
        Identifica clientes en riesgo de churn.
        """
        
        # Clientes con sentimiento muy negativo reciente
        at_risk = await db.query(Customer).join(Conversation).filter(
            Conversation.avg_sentiment < -0.7,
            Conversation.updated_at > datetime.now() - timedelta(days=7)
        ).all()
        
        for customer in at_risk:
            await self._send_alert(
                alert_type=AlertType.CHURN_RISK,
                severity="critical",
                message=f"🚨 Cliente {customer.name} en alto riesgo de churn",
                data={
                    "customer_id": customer.id,
                    "sentiment_score": customer.recent_sentiment,
                    "last_interaction": customer.last_interaction
                },
                recipients=["customer_success@company.com", customer.account_manager_email]
            )
    
    async def _check_hot_leads(self):
        """
        Notifica sobre leads muy calientes que requieren atención urgente.
        """
        
        hot_leads = await db.query(Lead).filter(
            Lead.score > 90,
            Lead.assigned_to == None,  # No asignados aún
            Lead.created_at > datetime.now() - timedelta(hours=1)
        ).all()
        
        if hot_leads:
            await self._send_alert(
                alert_type=AlertType.HOT_LEAD,
                severity="high",
                message=f"🔥 {len(hot_leads)} leads calientes sin asignar",
                data={
                    "leads": [{"id": l.id, "score": l.score, "name": l.name} for l in hot_leads]
                },
                recipients=["sales_team@company.com"]
            )
    
    async def _send_alert(
        self,
        alert_type: AlertType,
        severity: str,
        message: str,
        data: Dict,
        recipients: List[str]
    ):
        """
        Envía alerta por múltiples canales.
        """
        
        alert = Alert(
            type=alert_type.value,
            severity=severity,
            message=message,
            data=data,
            created_at=datetime.now()
        )
        
        await db.add(alert)
        await db.commit()
        
        # Email
        for email in recipients:
            await self.email_service.send_alert_email(
                to=email,
                subject=f"[{severity.upper()}] {alert_type.value}",
                body=message,
                data=data
            )
        
        # Slack/Teams (si configurado)
        if settings.SLACK_WEBHOOK_URL:
            await self._send_slack_alert(message, severity, data)
        
        # SMS para alertas críticas
        if severity == "critical":
            await self._send_sms_alert(recipients, message)
        
        logger.warning(
            "alert_triggered",
            type=alert_type.value,
            severity=severity,
            recipients=recipients
        )
```

---

## 📊 Modelos de Base de Datos Completos

```python
# app/models/__init__.py
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, JSON, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum
from datetime import datetime

# ============= LEADS & CONTACTS =============

class LeadStatus(enum.Enum):
    NEW = "new"
    QUALIFIED = "qualified"
    NURTURING = "nurturing"
    CONVERTED = "converted"
    LOST = "lost"

class Lead(Base):
    __tablename__ = "leads"
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String)
    phone = Column(String)
    company = Column(String)
    
    # Classification
    score = Column(Integer, default=0)  # 0-100
    category = Column(String)  # hot, warm, cold
    status = Column(Enum(LeadStatus), default=LeadStatus.NEW)
    
    # Source
    source = Column(String)  # whatsapp, instagram, messenger, website
    campaign_id = Column(String, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    converted_at = Column(DateTime, nullable=True)
    
    # Relationships
    classifications = relationship("LeadClassification", back_populates="lead")
    intents = relationship("LeadIntent", back_populates="lead")
    conversations = relationship("Conversation", back_populates="lead")

class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(String, primary_key=True)
    lead_id = Column(String, ForeignKey("leads.id"), nullable=True)
    
    name = Column(String, nullable=False)
    email = Column(String)
    phone = Column(String)
    company = Column(String)
    industry = Column(String)
    
    # Enrichment
    predicted_clv = Column(Float)
    purchasing_power = Column(String)  # low, medium, high
    interests = Column(JSON)  # ["tech", "sustainability"]
    segment = Column(String)  # vip, regular, at_risk
    
    # Engagement
    total_purchases = Column(Integer, default=0)
    total_spent = Column(Float, default=0.0)
    avg_order_value = Column(Float)
    last_purchase_date = Column(DateTime)
    
    # Status
    status = Column(String, default="active")  # active, inactive, churned
    churn_risk_score = Column(Float)  # 0-1
    
    # Relationships
    purchases = relationship("Purchase", back_populates="customer")
    conversations = relationship("Conversation", back_populates="customer")
    carts = relationship("Cart", back_populates="customer")

# ============= CONVERSATIONS & MESSAGES =============

class ConversationStatus(enum.Enum):
    ACTIVE = "active"
    WAITING_CUSTOMER = "waiting_customer"
    WAITING_AGENT = "waiting_agent"
    RESOLVED = "resolved"
    CLOSED = "closed"

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(String, primary_key=True)
    lead_id = Column(String, ForeignKey("leads.id"), nullable=True)
    customer_id = Column(String, ForeignKey("customers.id"), nullable=True)
    
    channel = Column(String)  # whatsapp, instagram, messenger
    status = Column(Enum(ConversationStatus), default=ConversationStatus.ACTIVE)
    
    # Analytics
    message_count = Column(Integer, default=0)
    avg_sentiment_score = Column(Float)
    bot_handled = Column(Boolean, default=True)
    escalated = Column(Boolean, default=False)
    escalation_reason = Column(String, nullable=True)
    
    # Timestamps
    started_at = Column(DateTime, default=datetime.utcnow)
    last_message_at = Column(DateTime)
    closed_at = Column(DateTime, nullable=True)
    
    # Relationships
    messages = relationship("Message", back_populates="conversation")
    lead = relationship("Lead", back_populates="conversations")
    customer = relationship("Customer", back_populates="conversations")

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(String, primary_key=True)
    conversation_id = Column(String, ForeignKey("conversations.id"))
    
    content = Column(Text, nullable=False)
    sender = Column(String)  # customer, bot, agent
    direction = Column(String)  # inbound, outbound
    
    # AI Analysis
    intent = Column(String, nullable=True)
    sentiment = Column(String, nullable=True)
    sentiment_score = Column(Float, nullable=True)
    
    # Timestamps
    sent_at = Column(DateTime, default=datetime.utcnow)
    delivered_at = Column(DateTime, nullable=True)
    read_at = Column(DateTime, nullable=True)
    
    # Relationship
    conversation = relationship("Conversation", back_populates="messages")

# ============= AI ANALYSIS =============

class LeadClassification(Base):
    __tablename__ = "lead_classifications"
    
    id = Column(String, primary_key=True)
    lead_id = Column(String, ForeignKey("leads.id"))
    
    score = Column(Integer, nullable=False)
    category = Column(String)
    reasoning = Column(Text)
    recommended_action = Column(String)
    
    ai_model = Column(String)
    classified_at = Column(DateTime, default=datetime.utcnow)
    
    lead = relationship("Lead", back_populates="classifications")

class LeadIntent(Base):
    __tablename__ = "lead_intents"
    
    id = Column(String, primary_key=True)
    lead_id = Column(String, ForeignKey("leads.id"))
    message_id = Column(String, ForeignKey("messages.id"), nullable=True)
    
    primary_intent = Column(String, nullable=False)
    secondary_intents = Column(JSON)
    confidence = Column(Float)
    entities = Column(JSON)
    
    detected_at = Column(DateTime, default=datetime.utcnow)
    
    lead = relationship("Lead", back_populates="intents")

# ============= E-COMMERCE =============

class Cart(Base):
    __tablename__ = "carts"
    
    id = Column(String, primary_key=True)
    customer_id = Column(String, ForeignKey("customers.id"))
    
    items = Column(JSON)
    total_amount = Column(Float)
    
    status = Column(String, default="pending")
    recovery_attempt_count = Column(Integer, default=0)
    discount_codes_used = Column(JSON)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    last_activity = Column(DateTime)
    recovered_at = Column(DateTime, nullable=True)
    
    customer = relationship("Customer", back_populates="carts")

class Purchase(Base):
    __tablename__ = "purchases"
    
    id = Column(String, primary_key=True)
    customer_id = Column(String, ForeignKey("customers.id"))
    
    items = Column(JSON)
    total_amount = Column(Float)
    status = Column(String)
    
    purchased_at = Column(DateTime, default=datetime.utcnow)
    
    customer = relationship("Customer", back_populates="purchases")

# ============= CONTENT & PUBLISHING =============

class GeneratedContent(Base):
    __tablename__ = "generated_content"
    
    id = Column(String, primary_key=True)
    content_type = Column(String)  # image, video, text
    platform = Column(String)  # instagram, facebook, tiktok
    
    asset_url = Column(String)
    copy = Column(Text)
    hashtags = Column(JSON)
    
    status = Column(String, default="draft")  # draft, scheduled, published
    scheduled_for = Column(DateTime, nullable=True)
    published_at = Column(DateTime, nullable=True)
    
    # Performance
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    engagement_rate = Column(Float)
    
    created_at = Column(DateTime, default=datetime.utcnow)

# ============= ANALYTICS =============

class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(String, primary_key=True)
    type = Column(String)  # sales_drop, churn_risk, hot_lead, etc
    severity = Column(String)  # low, medium, high, critical
    message = Column(Text)
    data = Column(JSON)
    
    status = Column(String, default="active")  # active, acknowledged, resolved
    acknowledged_by = Column(String, nullable=True)
    acknowledged_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
```

---

## 🧪 Testing

```python
# tests/test_services/test_lead_classifier.py
import pytest
from app.services.lead_classifier import LeadClassifier
from app.ai.openai_adapter import OpenAIAdapter

@pytest.mark.asyncio
async def test_classify_hot_lead():
    """Test que un mensaje de compra urgente genera score alto."""
    
    classifier = LeadClassifier(ai_adapter=OpenAIAdapter())
    
    request = LeadClassificationRequest(
        message="Necesito 500 laptops para mañana, mi presupuesto es $500K",
        sender_metadata={
            "name": "CEO Tech Corp",
            "previous_interactions": 0
        }
    )
    
    result = await classifier.classify(request)
    
    assert result.score > 80, "Hot lead should have score > 80"
    assert result.category == "hot"
    assert "urgency" in result.reasoning.lower()
```

---

## 🚀 Deployment

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  fastapi:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/crm
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - META_ACCESS_TOKEN=${META_ACCESS_TOKEN}
    depends_on:
      - postgres
      - redis
  
  postgres:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: crm
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
  
  n8n:
    image: n8nio/n8n
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=admin123
    volumes:
      - n8n_data:/home/node/.n8n
      - ./n8n/workflows:/workflows

volumes:
  postgres_data:
  n8n_data:
```

---

## 📈 Monitoreo

```python
# app/core/monitoring.py
from prometheus_client import Counter, Histogram, Gauge

# Métricas
messages_received = Counter('messages_received_total', 'Total messages received', ['channel'])
classification_time = Histogram('lead_classification_seconds', 'Time to classify lead')
active_conversations = Gauge('active_conversations', 'Number of active conversations')

# Uso
messages_received.labels(channel='whatsapp').inc()
with classification_time.time():
    await classifier.classify(lead)
```

---

## 🎓 Conclusión

Este documento proporciona especificaciones completas para implementar un CRM Autónomo de clase empresarial con:

✅ 22 flujos de trabajo automatizados
✅ Integración multi-canal (WhatsApp, IG, Messenger)
✅ IA multi-modelo (GPT, Gemini, Claude)
✅ Orquestación con n8n
✅ Base de datos PostgreSQL completa
✅ Testing comprehensivo
✅ Deployment production-ready
✅ Monitoreo y alertas

**Próximos pasos para Cursor:**
1. Generar estructura de proyecto completa
2. Implementar flujos 1-5 primero (core functionality)
3. Configurar integraciones de IA
4. Setup de base de datos con migraciones
5. Conectar con n8n
6. Desplegar en staging
7. Testing de integración
8. Desplegar en producción

