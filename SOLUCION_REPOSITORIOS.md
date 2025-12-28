# Solución de Problemas con Repositorios

## Problema Detectado

El repositorio `mirrors.dc.uba.ar` no está disponible, lo que impide instalar PostgreSQL.

## Solución Rápida

Ejecuta el script que arregla los repositorios e instala PostgreSQL:

```bash
./fix_repos_and_install_postgresql.sh
```

## Solución Manual

### Paso 1: Hacer backup de repositorios

```bash
sudo cp /etc/apt/sources.list.d/ubuntu.sources /etc/apt/sources.list.d/ubuntu.sources.backup
```

### Paso 2: Editar repositorios

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

Reemplaza el contenido con:

```
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
```

### Paso 3: Actualizar e instalar

```bash
sudo apt update
sudo apt install -y postgresql postgresql-contrib
```

## Alternativa: Usar Repositorio Oficial de PostgreSQL

Si los repositorios de Ubuntu siguen fallando, puedes usar el repositorio oficial de PostgreSQL:

```bash
# Agregar repositorio oficial de PostgreSQL
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'

# Agregar clave GPG
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

# Actualizar e instalar
sudo apt update
sudo apt install -y postgresql postgresql-contrib
```

## Verificar Repositorios

Para ver qué repositorios están configurados:

```bash
cat /etc/apt/sources.list.d/ubuntu.sources
```

Para probar conectividad a un repositorio:

```bash
ping -c 1 archive.ubuntu.com
```

## Restaurar Backup

Si algo sale mal, puedes restaurar el backup:

```bash
sudo cp /etc/apt/sources.list.d/ubuntu.sources.backup /etc/apt/sources.list.d/ubuntu.sources
sudo apt update
```

## Alternativa Temporal: Usar SQLite

Si no puedes instalar PostgreSQL ahora, puedes usar SQLite temporalmente:

```bash
cat > .env << 'EOF'
DATABASE_URL=sqlite:///nominaplus.db
SECRET_KEY=dev-secret-key-cambiar-en-produccion
FLASK_ENV=development
FLASK_DEBUG=True
APP_NAME=NominaPlus
APP_VERSION=1.0.0
EOF
```

SQLite funciona perfectamente para desarrollo y pruebas. Puedes migrar a PostgreSQL más tarde.

