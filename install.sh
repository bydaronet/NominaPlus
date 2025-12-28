#!/bin/bash
# Script de instalación para NominaPlus
# Este script instala las dependencias necesarias

echo "=========================================="
echo "Instalación de NominaPlus"
echo "=========================================="
echo ""

# Verificar Python
echo "Verificando Python..."
python3 --version
if [ $? -ne 0 ]; then
    echo "Error: Python 3 no está instalado"
    exit 1
fi

# Intentar instalar python3-venv si no está disponible
echo ""
echo "Verificando python3-venv..."
if ! python3 -m venv --help > /dev/null 2>&1; then
    echo "python3-venv no está disponible. Intentando instalar..."
    echo "Por favor, ejecuta manualmente:"
    echo "  sudo apt install python3.12-venv python3.12-dev"
    echo ""
    echo "O si prefieres, puedes instalar pip directamente con:"
    echo "  python3 -m ensurepip --break-system-packages"
    echo ""
    read -p "¿Deseas intentar instalar pip directamente? (s/n): " respuesta
    if [ "$respuesta" = "s" ] || [ "$respuesta" = "S" ]; then
        python3 -m ensurepip --break-system-packages
    else
        echo "Por favor, instala python3-venv manualmente y vuelve a ejecutar este script"
        exit 1
    fi
fi

# Crear entorno virtual
echo ""
echo "Creando entorno virtual..."
if [ -d "venv" ]; then
    echo "El entorno virtual ya existe. Eliminando..."
    rm -rf venv
fi

python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "Error al crear el entorno virtual"
    exit 1
fi

# Activar entorno virtual e instalar dependencias
echo ""
echo "Activando entorno virtual e instalando dependencias..."
source venv/bin/activate

echo "Actualizando pip..."
pip install --upgrade pip

echo ""
echo "Instalando dependencias desde requirements.txt..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "¡Instalación completada exitosamente!"
    echo "=========================================="
    echo ""
    echo "Para activar el entorno virtual en el futuro, ejecuta:"
    echo "  source venv/bin/activate"
    echo ""
    echo "Para ejecutar la aplicación:"
    echo "  python app.py"
    echo ""
else
    echo ""
    echo "Error al instalar las dependencias"
    exit 1
fi

