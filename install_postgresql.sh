#!/bin/bash
# Script para instalar y configurar PostgreSQL para NominaPlus

echo "=========================================="
echo "Instalación de PostgreSQL para NominaPlus"
echo "=========================================="
echo ""

# Verificar si PostgreSQL ya está instalado
if command -v psql &> /dev/null; then
    echo "✓ PostgreSQL ya está instalado"
    psql --version
    echo ""
else
    echo "Instalando PostgreSQL..."
    sudo apt update
    sudo apt install -y postgresql postgresql-contrib
    
    if [ $? -eq 0 ]; then
        echo "✓ PostgreSQL instalado correctamente"
    else
        echo "✗ Error al instalar PostgreSQL"
        exit 1
    fi
fi

# Verificar que el servicio esté corriendo
echo ""
echo "Verificando estado del servicio PostgreSQL..."
sudo systemctl status postgresql --no-pager | head -3

# Iniciar el servicio si no está corriendo
if ! sudo systemctl is-active --quiet postgresql; then
    echo "Iniciando servicio PostgreSQL..."
    sudo systemctl start postgresql
    sudo systemctl enable postgresql
fi

echo ""
echo "=========================================="
echo "Configuración de la Base de Datos"
echo "=========================================="
echo ""

# Solicitar información para crear la base de datos
read -p "Nombre de la base de datos [nominaplus]: " db_name
db_name=${db_name:-nominaplus}

read -p "Usuario de PostgreSQL [nominaplus_user]: " db_user
db_user=${db_user:-nominaplus_user}

read -p "Contraseña para el usuario: " -s db_password
echo ""

# Crear usuario y base de datos
echo ""
echo "Creando usuario y base de datos..."

sudo -u postgres psql << EOF
-- Crear usuario si no existe
DO \$\$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_user WHERE usename = '$db_user') THEN
        CREATE USER $db_user WITH PASSWORD '$db_password';
    ELSE
        ALTER USER $db_user WITH PASSWORD '$db_password';
    END IF;
END
\$\$;

-- Crear base de datos si no existe
SELECT 'CREATE DATABASE $db_name OWNER $db_user'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '$db_name')\gexec

-- Otorgar privilegios
GRANT ALL PRIVILEGES ON DATABASE $db_name TO $db_user;
\q
EOF

if [ $? -eq 0 ]; then
    echo "✓ Base de datos '$db_name' creada correctamente"
    echo "✓ Usuario '$db_user' configurado"
else
    echo "✗ Error al crear la base de datos"
    exit 1
fi

# Crear archivo .env
echo ""
echo "Creando archivo .env..."

cat > .env << EOF
# Database Configuration - PostgreSQL
DATABASE_URL=postgresql://${db_user}:${db_password}@localhost:5432/${db_name}

# Flask Configuration
SECRET_KEY=$(openssl rand -hex 32)
FLASK_ENV=development
FLASK_DEBUG=True

# Application Configuration
APP_NAME=NominaPlus
APP_VERSION=1.0.0
EOF

echo "✓ Archivo .env creado con la configuración de PostgreSQL"
echo ""
echo "=========================================="
echo "¡Configuración completada!"
echo "=========================================="
echo ""
echo "Detalles de la conexión:"
echo "  Base de datos: $db_name"
echo "  Usuario: $db_user"
echo "  Host: localhost"
echo "  Puerto: 5432"
echo ""
echo "Ahora puedes ejecutar la aplicación:"
echo "  source venv/bin/activate"
echo "  python app.py"
echo ""

