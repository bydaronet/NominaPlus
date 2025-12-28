# Guía de Instalación - NominaPlus

## Problema con dependencias del sistema

Si encuentras problemas al instalar `python3-pip` debido a dependencias rotas, aquí tienes varias soluciones:

## Solución 1: Instalar python3-venv (Recomendado)

```bash
sudo apt update
sudo apt install python3.12-venv python3.12-dev
```

Luego ejecuta el script de instalación:

```bash
./install.sh
```

## Solución 2: Usar el script de instalación automático

El script `install.sh` intentará configurar todo automáticamente:

```bash
chmod +x install.sh
./install.sh
```

## Solución 3: Instalación manual paso a paso

### Paso 1: Instalar python3-venv

```bash
sudo apt install python3.12-venv python3.12-dev
```

### Paso 2: Crear entorno virtual

```bash
python3 -m venv venv
```

### Paso 3: Activar entorno virtual

```bash
source venv/bin/activate
```

### Paso 4: Instalar dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Solución 4: Instalar pip directamente (si no puedes instalar python3-venv)

Si no puedes instalar `python3-venv`, puedes instalar pip directamente:

```bash
python3 -m ensurepip --break-system-packages
```

**Nota:** Esta opción modifica el sistema Python, úsala con precaución.

Luego instala las dependencias:

```bash
python3 -m pip install --user -r requirements.txt
```

## Solución 5: Usar pipx (si está disponible)

```bash
sudo apt install pipx
pipx install flask
# O instalar en un entorno virtual
```

## Verificar la instalación

Después de instalar, verifica que todo funciona:

```bash
# Activar entorno virtual (si usaste venv)
source venv/bin/activate

# Verificar Flask
python3 -c "import flask; print(flask.__version__)"

# Ejecutar la aplicación
python app.py
```

## Solución de problemas comunes

### Error: "externally-managed-environment"

Este error aparece en sistemas modernos de Ubuntu/Debian. La solución es usar un entorno virtual:

```bash
python3 -m venv venv
source venv/bin/activate
```

### Error: "ensurepip is not available"

Necesitas instalar `python3-venv`:

```bash
sudo apt install python3.12-venv
```

### Error: "Dependencias rotas" en apt

Intenta arreglar los repositorios:

```bash
sudo apt update
sudo apt --fix-broken install
sudo apt install python3.12-venv
```

### Si nada funciona

Como último recurso, puedes usar Docker o instalar Python desde fuentes, pero esto es más complejo.

## Próximos pasos

Una vez instaladas las dependencias:

1. Configura PostgreSQL y crea el archivo `.env`
2. Ejecuta `python app.py` para iniciar el servidor
3. (Opcional) Ejecuta `python init_sample_data.py` para cargar datos de ejemplo

