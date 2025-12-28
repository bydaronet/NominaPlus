# Guía de Instalación de PostgreSQL para NominaPlus

## Instalación Automática (Recomendado)

Ejecuta el script de instalación:

```bash
./install_postgresql.sh
```

Este script:
- Instala PostgreSQL y sus dependencias
- Inicia y habilita el servicio
- Crea la base de datos `nominaplus`
- Crea un usuario con permisos
- Configura el archivo `.env` automáticamente

## Instalación Manual

### Paso 1: Instalar PostgreSQL

```bash
sudo apt update
sudo apt install -y postgresql postgresql-contrib
```

### Paso 2: Iniciar el servicio

```bash
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### Paso 3: Verificar la instalación

```bash
sudo systemctl status postgresql
psql --version
```

### Paso 4: Crear la base de datos

Acceder a PostgreSQL como superusuario:

```bash
sudo -u postgres psql
```

Dentro de PostgreSQL, ejecutar:

```sql
-- Crear usuario
CREATE USER nominaplus_user WITH PASSWORD 'tu_contraseña_segura';

-- Crear base de datos
CREATE DATABASE nominaplus OWNER nominaplus_user;

-- Otorgar privilegios
GRANT ALL PRIVILEGES ON DATABASE nominaplus TO nominaplus_user;

-- Salir
\q
```

### Paso 5: Configurar el archivo .env

Crear o editar el archivo `.env`:

```bash
cat > .env << EOF
DATABASE_URL=postgresql://nominaplus_user:tu_contraseña_segura@localhost:5432/nominaplus
SECRET_KEY=tu-clave-secreta-aqui
FLASK_ENV=development
FLASK_DEBUG=True
APP_NAME=NominaPlus
APP_VERSION=1.0.0
EOF
```

## Verificar la Conexión

### Desde la línea de comandos:

```bash
psql -U nominaplus_user -d nominaplus -h localhost
```

### Desde Python (con la aplicación):

```bash
source venv/bin/activate
python app.py
```

Si no hay errores, la conexión está funcionando.

## Comandos Útiles de PostgreSQL

### Acceder a PostgreSQL:

```bash
# Como superusuario
sudo -u postgres psql

# Como usuario específico
psql -U nominaplus_user -d nominaplus
```

### Comandos dentro de psql:

```sql
-- Listar bases de datos
\l

-- Conectarse a una base de datos
\c nominaplus

-- Listar tablas
\dt

-- Ver estructura de una tabla
\d nombre_tabla

-- Listar usuarios
\du

-- Salir
\q
```

### Reiniciar el servicio:

```bash
sudo systemctl restart postgresql
```

### Ver logs:

```bash
sudo tail -f /var/log/postgresql/postgresql-*-main.log
```

## Solución de Problemas

### Error: "could not connect to server"

1. Verificar que el servicio esté corriendo:
```bash
sudo systemctl status postgresql
```

2. Si no está corriendo:
```bash
sudo systemctl start postgresql
```

### Error: "password authentication failed"

Verificar que la contraseña en `.env` sea correcta. Puedes cambiarla:

```sql
ALTER USER nominaplus_user WITH PASSWORD 'nueva_contraseña';
```

### Error: "database does not exist"

Crear la base de datos:

```sql
CREATE DATABASE nominaplus;
```

### Error: "permission denied"

Asegúrate de que el usuario tenga los permisos correctos:

```sql
GRANT ALL PRIVILEGES ON DATABASE nominaplus TO nominaplus_user;
```

### Cambiar la contraseña del usuario postgres

```bash
sudo -u postgres psql
ALTER USER postgres WITH PASSWORD 'nueva_contraseña';
```

## Configuración de Seguridad (Producción)

Para producción, considera:

1. **Cambiar el puerto** (si es necesario)
2. **Configurar firewall** para limitar acceso
3. **Usar SSL/TLS** para conexiones
4. **Limitar permisos** del usuario de la aplicación
5. **Hacer backups regulares**

### Backup de la base de datos:

```bash
pg_dump -U nominaplus_user nominaplus > backup_$(date +%Y%m%d).sql
```

### Restaurar backup:

```bash
psql -U nominaplus_user nominaplus < backup_20241228.sql
```

## Migraciones de Base de Datos

Con Flask-Migrate, puedes gestionar cambios en el esquema:

```bash
# Crear una migración
flask db migrate -m "Descripción del cambio"

# Aplicar migraciones
flask db upgrade

# Revertir última migración
flask db downgrade
```

## Recursos Adicionales

- [Documentación oficial de PostgreSQL](https://www.postgresql.org/docs/)
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
- [Flask-Migrate](https://flask-migrate.readthedocs.io/)

