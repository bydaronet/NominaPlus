#!/bin/bash
# Script para arreglar repositorios e instalar PostgreSQL

echo "=========================================="
echo "Arreglando repositorios e instalando PostgreSQL"
echo "=========================================="
echo ""

# Hacer backup del archivo de repositorios
echo "Haciendo backup de repositorios..."
sudo cp /etc/apt/sources.list.d/ubuntu.sources /etc/apt/sources.list.d/ubuntu.sources.backup

# Crear nuevo archivo de repositorios usando archive.ubuntu.com
echo "Configurando repositorios con archive.ubuntu.com..."
sudo tee /etc/apt/sources.list.d/ubuntu.sources > /dev/null << 'EOF'
Types: deb
URIs: http://archive.ubuntu.com/ubuntu
Suites: noble noble-updates noble-backports noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg

Types: deb
URIs: http://security.ubuntu.com/ubuntu
Suites: noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
EOF

echo "✓ Repositorios actualizados"
echo ""

# Actualizar lista de paquetes
echo "Actualizando lista de paquetes..."
sudo apt update

if [ $? -ne 0 ]; then
    echo "⚠ Advertencia: Algunos repositorios pueden tener problemas, pero continuamos..."
fi

echo ""

# Instalar PostgreSQL
echo "Instalando PostgreSQL..."
sudo apt install -y postgresql postgresql-contrib

if [ $? -eq 0 ]; then
    echo "✓ PostgreSQL instalado correctamente"
else
    echo "✗ Error al instalar PostgreSQL"
    echo ""
    echo "Intentando con repositorio específico de PostgreSQL..."
    # Intentar agregar repositorio oficial de PostgreSQL
    sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
    sudo apt update
    sudo apt install -y postgresql postgresql-contrib
fi

# Iniciar servicio
echo ""
echo "Iniciando servicio PostgreSQL..."
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Verificar instalación
echo ""
echo "Verificando instalación..."
if systemctl is-active --quiet postgresql; then
    echo "✓ Servicio PostgreSQL está corriendo"
    psql --version
else
    echo "⚠ El servicio PostgreSQL no está corriendo"
fi

echo ""
echo "=========================================="
echo "¡Instalación completada!"
echo "=========================================="
echo ""
echo "Ahora ejecuta ./install_postgresql.sh para configurar la base de datos"
echo "O configura manualmente siguiendo POSTGRESQL_SETUP.md"
echo ""

