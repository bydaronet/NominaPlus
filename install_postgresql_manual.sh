#!/bin/bash
# Versión simplificada del script de instalación (sin interacción)

echo "Instalando PostgreSQL..."
sudo apt update
sudo apt install -y postgresql postgresql-contrib

echo "Iniciando servicio PostgreSQL..."
sudo systemctl start postgresql
sudo systemctl enable postgresql

echo "✓ PostgreSQL instalado y configurado"
echo ""
echo "Ahora ejecuta: ./install_postgresql.sh"
echo "O configura manualmente siguiendo POSTGRESQL_SETUP.md"

