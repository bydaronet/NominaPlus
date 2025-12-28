#!/bin/bash
# Script para configurar la base de datos de NominaPlus en PostgreSQL

echo "=========================================="
echo "Configuración de Base de Datos NominaPlus"
echo "=========================================="
echo ""

# Verificar que PostgreSQL esté instalado
if ! command -v psql &> /dev/null; then
    echo "✗ PostgreSQL no está instalado"
    exit 1
fi

echo "✓ PostgreSQL está instalado: $(psql --version)"
echo ""

# Iniciar servicio si no está corriendo
echo "Verificando servicio PostgreSQL..."
if ! sudo systemctl is-active --quiet postgresql; then
    echo "Iniciando servicio PostgreSQL..."
    sudo systemctl start postgresql
    sudo systemctl enable postgresql
    sleep 2
fi

if sudo systemctl is-active --quiet postgresql; then
    echo "✓ Servicio PostgreSQL está corriendo"
else
    echo "⚠ Advertencia: No se pudo verificar el estado del servicio"
    echo "  Intenta manualmente: sudo systemctl start postgresql"
fi

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
        RAISE NOTICE 'Usuario $db_user creado';
    ELSE
        ALTER USER $db_user WITH PASSWORD '$db_password';
        RAISE NOTICE 'Contraseña del usuario $db_user actualizada';
    END IF;
END
\$\$;

-- Crear base de datos si no existe
SELECT 'CREATE DATABASE $db_name OWNER $db_user'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '$db_name')\gexec

-- Otorgar privilegios
GRANT ALL PRIVILEGES ON DATABASE $db_name TO $db_user;

-- Conectar a la base de datos y otorgar privilegios en el esquema público
\c $db_name
GRANT ALL ON SCHEMA public TO $db_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO $db_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO $db_user;

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

# Escapar la contraseña para URL
db_password_escaped=$(printf '%s' "$db_password" | sed 's/[[\.*^$()+?{|]/\\&/g')

cat > .env << EOF
# Database Configuration - PostgreSQL
DATABASE_URL=postgresql://${db_user}:${db_password_escaped}@localhost:5432/${db_name}

# Flask Configuration
SECRET_KEY=$(openssl rand -hex 32 2>/dev/null || python3 -c "import secrets; print(secrets.token_hex(32))")
FLASK_ENV=development
FLASK_DEBUG=True

# Application Configuration
APP_NAME=NominaPlus
APP_VERSION=1.0.0
EOF

echo "✓ Archivo .env creado con la configuración de PostgreSQL"
echo ""

# Verificar conexión
echo "Verificando conexión a la base de datos..."
PGPASSWORD="$db_password" psql -h localhost -U "$db_user" -d "$db_name" -c "SELECT version();" > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✓ Conexión a la base de datos exitosa"
else
    echo "⚠ Advertencia: No se pudo verificar la conexión automáticamente"
    echo "  Puedes probar manualmente con:"
    echo "  PGPASSWORD='$db_password' psql -h localhost -U $db_user -d $db_name"
fi

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
echo "La aplicación creará automáticamente las tablas al iniciar."
echo ""

