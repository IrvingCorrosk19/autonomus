#!/bin/bash
# Script para ejecutar todas las pruebas

echo "=========================================="
echo "Ejecutando pruebas del Autonomous CRM"
echo "=========================================="
echo ""

# Verificar que el servidor esté corriendo
echo "Verificando que el servidor esté corriendo..."
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Servidor está corriendo"
else
    echo "❌ Servidor no está corriendo. Inicia con:"
    echo "   uvicorn app.main:app --reload"
    exit 1
fi

echo ""
echo "Ejecutando pruebas..."
python scripts/test_complete.py

