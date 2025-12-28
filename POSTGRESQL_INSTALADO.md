# PostgreSQL Instalado Correctamente ✅

PostgreSQL 16 se ha instalado exitosamente en tu sistema.

## Próximos Pasos

### 1. Iniciar el servicio PostgreSQL (si no está corriendo)

```bash
sudo systemctl start postgresql
sudo systemctl enable postgresql  # Para que inicie automáticamente
```

Verificar que está corriendo:
```bash
sudo systemctl status postgresql
```

### 2. Configurar la base de datos para NominaPlus

Ejecuta el script de configuración:

```bash
./setup_postgresql_db.sh
```

Este script te pedirá:
- Nombre de la base de datos (por defecto: `nominaplus`)
- Usuario de PostgreSQL (por defecto: `nominaplus_user`)
- Contraseña para el usuario

Y automáticamente:
- Creará el usuario y la base de datos
- Configurará permisos
- Creará el archivo `.env` con la configuración

### 3. Configuración Manual (Alternativa)

Si prefieres hacerlo manualmente:

#### Paso 1: Acceder a PostgreSQL

```bash
sudo -u postgres psql
```

#### Paso 2: Crear usuario y base de datos

Dentro de PostgreSQL:

```sql
-- Crear usuario
CREATE USER nominaplus_user WITH PASSWORD 'tu_contraseña_segura';

-- Crear base de datos
CREATE DATABASE nominaplus OWNER nominaplus_user;

-- Otorgar privilegios
GRANT ALL PRIVILEGES ON DATABASE nominaplus TO nominaplus_user;

-- Conectar a la base de datos
\c nominaplus

-- Otorgar privilegios en el esquema
GRANT ALL ON SCHEMA public TO nominaplus_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO nominaplus_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO nominaplus_user;

-- Salir
\q
```

#### Paso 3: Crear archivo .env

```bash
cat > .env << 'EOF'
DATABASE_URL=postgresql://nominaplus_user:tu_contraseña_segura@localhost:5432/nominaplus
SECRET_KEY=tu-clave-secreta-aqui
FLASK_ENV=development
FLASK_DEBUG=True
APP_NAME=NominaPlus
APP_VERSION=1.0.0
EOF
```

### 4. Ejecutar la aplicación

```bash
# Activar entorno virtual
source venv/bin/activate

# Ejecutar la aplicación (creará las tablas automáticamente)
python app.py
```

## Verificar la Instalación

### Verificar que PostgreSQL está corriendo:

```bash
sudo systemctl status postgresql
```

### Probar conexión:

```bash
# Como superusuario
sudo -u postgres psql

# Como usuario específico (después de crearlo)
psql -U nominaplus_user -d nominaplus -h localhost
```

### Ver versiones instaladas:

```bash
psql --version
sudo -u postgres psql -c "SELECT version();"
```

## Comandos Útiles

### Reiniciar PostgreSQL:

```bash
sudo systemctl restart postgresql
```

### Ver logs:

```bash
sudo tail -f /var/log/postgresql/postgresql-16-main.log
```

### Listar bases de datos:

```bash
sudo -u postgres psql -c "\l"
```

### Listar usuarios:

```bash
sudo -u postgres psql -c "\du"
```

## Solución de Problemas

### Error: "could not connect to server"

1. Verificar que el servicio esté corriendo:
```bash
sudo systemctl start postgresql
```

2. Verificar que PostgreSQL esté escuchando:
```bash
sudo netstat -tlnp | grep 5432
```

### Error: "password authentication failed"

Verificar la contraseña en el archivo `.env` o cambiarla:

```sql
ALTER USER nominaplus_user WITH PASSWORD 'nueva_contraseña';
```

### Error: "database does not exist"

Crear la base de datos siguiendo los pasos de configuración manual.

## Información del Sistema

- **Versión de PostgreSQL**: 16.11
- **Ubicación de datos**: `/var/lib/postgresql/16/main`
- **Archivo de configuración**: `/etc/postgresql/16/main/postgresql.conf`
- **Puerto por defecto**: 5432

## ¡Listo para Usar!

Una vez configurada la base de datos, tu aplicación NominaPlus estará lista para funcionar con PostgreSQL.

