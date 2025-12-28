# Guía de Inicio Rápido - NominaPlus

## ✅ Instalación Completada

¡Las dependencias de Python ya están instaladas! Ahora solo necesitas configurar la base de datos.

## 🚀 Inicio Rápido (3 pasos)

### Paso 1: Activar el entorno virtual

```bash
source venv/bin/activate
```

### Paso 2: Configurar la base de datos

Tienes dos opciones:

#### Opción A: SQLite (Más fácil, para empezar)

SQLite no requiere instalación adicional. Solo ejecuta:

```bash
# Crear archivo .env con SQLite
cat > .env << EOF
DATABASE_URL=sqlite:///nominaplus.db
SECRET_KEY=dev-secret-key-cambiar-en-produccion
FLASK_ENV=development
FLASK_DEBUG=True
APP_NAME=NominaPlus
APP_VERSION=1.0.0
EOF
```

#### Opción B: PostgreSQL (Recomendado para producción)

1. Instalar PostgreSQL:
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

2. Crear la base de datos:
```bash
sudo -u postgres psql
```

Dentro de PostgreSQL:
```sql
CREATE DATABASE nominaplus;
CREATE USER nominaplus_user WITH PASSWORD 'tu_contraseña';
GRANT ALL PRIVILEGES ON DATABASE nominaplus TO nominaplus_user;
\q
```

3. Configurar .env:
```bash
./setup_db.sh
# O manualmente, edita .env y configura:
# DATABASE_URL=postgresql://nominaplus_user:tu_contraseña@localhost:5432/nominaplus
```

### Paso 3: Ejecutar la aplicación

```bash
python app.py
```

La API estará disponible en: `http://localhost:5000`

## 🧪 Probar la API

### Verificar que funciona:

```bash
curl http://localhost:5000/
```

### Cargar datos de ejemplo (opcional):

En otra terminal:
```bash
source venv/bin/activate
python init_sample_data.py
```

### Probar endpoints:

```bash
# Obtener empleados
curl http://localhost:5000/api/employees

# Crear un empleado
curl -X POST http://localhost:5000/api/employees \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Juan Pérez",
    "dni": "1234567890123",
    "position": "Desarrollador",
    "hourly_rate": 50.00
  }'
```

## 📝 Notas Importantes

1. **SQLite vs PostgreSQL:**
   - SQLite es perfecto para desarrollo y pruebas
   - PostgreSQL es necesario para producción (mejor rendimiento, concurrencia)

2. **Archivo .env:**
   - No subas el archivo `.env` a Git (ya está en .gitignore)
   - Cambia `SECRET_KEY` en producción

3. **Activar entorno virtual:**
   - Cada vez que abras una nueva terminal, ejecuta: `source venv/bin/activate`
   - Verás `(venv)` en tu prompt cuando esté activo

## 🔧 Solución de Problemas

### Error: "No module named 'flask'"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Error de conexión a base de datos
- Verifica que el archivo `.env` existe y tiene la configuración correcta
- Para PostgreSQL: verifica que el servicio esté corriendo: `sudo systemctl status postgresql`

### Puerto 5000 ya en uso
```bash
# Cambiar el puerto en app.py o usar:
PORT=5001 python app.py
```

## 📚 Documentación Completa

Ver `README.md` para documentación completa de la API.

## 🎉 ¡Listo!

Tu aplicación NominaPlus está lista para usar. ¡Feliz desarrollo!

