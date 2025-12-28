#!/bin/bash
# Script rápido para configurar la base de datos (sin interacción)

echo "=========================================="
echo "Configuración Rápida de Base de Datos"
echo "=========================================="
echo ""

# Valores por defecto
DB_NAME=${1:-nominaplus}
DB_USER=${2:-nominaplus_user}
DB_PASSWORD=${3:-nominaplus123}

echo "Usando configuración:"
echo "  Base de datos: $DB_NAME"
echo "  Usuario: $DB_USER"
echo "  (Para cambiar: ./quick_setup_db.sh [db_name] [user] [password])"
echo ""

# Crear usuario y base de datos
echo "Creando usuario y base de datos..."
sudo -u postgres psql << EOF
-- Crear usuario si no existe
DO \$\$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_user WHERE usename = '$DB_USER') THEN
        CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
        RAISE NOTICE 'Usuario $DB_USER creado';
    ELSE
        ALTER USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
        RAISE NOTICE 'Contraseña del usuario $DB_USER actualizada';
    END IF;
END
\$\$;

-- Crear base de datos si no existe
SELECT 'CREATE DATABASE $DB_NAME OWNER $DB_USER'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '$DB_NAME')\gexec

-- Otorgar privilegios
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;

-- Conectar y configurar esquema
\c $DB_NAME
GRANT ALL ON SCHEMA public TO $DB_USER;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO $DB_USER;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO $DB_USER;

\q
EOF

if [ $? -eq 0 ]; then
    echo "✓ Base de datos configurada correctamente"
else
    echo "✗ Error al configurar la base de datos"
    exit 1
fi

# Actualizar .env
echo ""
echo "Actualizando archivo .env..."

# Escapar la contraseña para URL
DB_PASSWORD_ESC=$(printf '%s' "$DB_PASSWORD" | sed 's/[[\.*^$()+?{|]/\\&/g')

# Generar SECRET_KEY si no existe
if [ -f .env ] && grep -q "SECRET_KEY=" .env; then
    # Mantener SECRET_KEY existente
    SECRET_KEY=$(grep "^SECRET_KEY=" .env | cut -d'=' -f2-)
else
    SECRET_KEY=$(openssl rand -hex 32 2>/dev/null || python3 -c "import secrets; print(secrets.token_hex(32))")
fi

cat > .env << EOF
# Database Configuration - PostgreSQL
DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD_ESC}@localhost:5432/${DB_NAME}

# Flask Configuration
SECRET_KEY=${SECRET_KEY}
FLASK_ENV=development
FLASK_DEBUG=True

# Application Configuration
APP_NAME=NominaPlus
APP_VERSION=1.0.0
EOF

echo "✓ Archivo .env actualizado"
echo ""
echo "=========================================="
echo "¡Configuración completada!"
echo "=========================================="
echo ""
echo "Detalles de conexión:"
echo "  Base de datos: $DB_NAME"
echo "  Usuario: $DB_USER"
echo "  Host: localhost:5432"
echo ""
echo "Ahora puedes ejecutar:"
echo "  python app.py"
echo ""

