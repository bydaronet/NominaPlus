#!/bin/bash
# Script para configurar la base de datos

echo "=========================================="
echo "Configuración de Base de Datos - NominaPlus"
echo "=========================================="
echo ""

# Verificar si existe .env
if [ ! -f .env ]; then
    echo "Creando archivo .env..."
    cat > .env << EOF
# Database Configuration
# Opción 1: PostgreSQL (recomendado para producción)
# DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/nominaplus

# Opción 2: SQLite (para desarrollo/pruebas)
DATABASE_URL=sqlite:///nominaplus.db

# Flask Configuration
SECRET_KEY=dev-secret-key-cambiar-en-produccion-$(openssl rand -hex 16)
FLASK_ENV=development
FLASK_DEBUG=True

# Application Configuration
APP_NAME=NominaPlus
APP_VERSION=1.0.0
EOF
    echo "✓ Archivo .env creado"
else
    echo "✓ Archivo .env ya existe"
fi

echo ""
echo "¿Qué base de datos deseas usar?"
echo "1) SQLite (simple, no requiere instalación adicional)"
echo "2) PostgreSQL (recomendado para producción)"
echo ""
read -p "Selecciona una opción (1 o 2): " opcion

if [ "$opcion" = "2" ]; then
    echo ""
    echo "Configurando PostgreSQL..."
    echo "Por favor, proporciona los siguientes datos:"
    read -p "Usuario de PostgreSQL: " db_user
    read -p "Contraseña: " -s db_pass
    echo ""
    read -p "Nombre de la base de datos [nominaplus]: " db_name
    db_name=${db_name:-nominaplus}
    read -p "Host [localhost]: " db_host
    db_host=${db_host:-localhost}
    read -p "Puerto [5432]: " db_port
    db_port=${db_port:-5432}
    
    # Actualizar .env
    sed -i "s|^# DATABASE_URL=postgresql://.*|DATABASE_URL=postgresql://${db_user}:${db_pass}@${db_host}:${db_port}/${db_name}|" .env
    sed -i "s|^DATABASE_URL=sqlite:///.*|# DATABASE_URL=sqlite:///nominaplus.db|" .env
    
    echo ""
    echo "✓ Configuración de PostgreSQL guardada en .env"
    echo ""
    echo "Asegúrate de que PostgreSQL esté instalado y corriendo:"
    echo "  sudo apt install postgresql postgresql-contrib"
    echo "  sudo systemctl start postgresql"
    echo "  sudo -u postgres createdb $db_name"
else
    echo ""
    echo "✓ Usando SQLite (configuración por defecto)"
    echo "  La base de datos se creará automáticamente en: nominaplus.db"
fi

echo ""
echo "=========================================="
echo "Configuración completada!"
echo "=========================================="
echo ""
echo "Ahora puedes ejecutar la aplicación:"
echo "  source venv/bin/activate"
echo "  python app.py"
echo ""

