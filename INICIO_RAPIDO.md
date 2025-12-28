# Inicio Rápido - NominaPlus

## ✅ Estado Actual

- ✅ PostgreSQL 16 instalado y corriendo
- ✅ Entorno virtual configurado
- ✅ Dependencias instaladas
- ✅ Archivo .env existe

## 🚀 Configurar Base de Datos (Elige una opción)

### Opción 1: Configuración Interactiva (Recomendada)

```bash
./setup_postgresql_db.sh
```

Te pedirá:
- Nombre de la base de datos
- Usuario
- Contraseña

### Opción 2: Configuración Rápida (Con valores por defecto)

```bash
./quick_setup_db.sh
```

Usa valores por defecto:
- Base de datos: `nominaplus`
- Usuario: `nominaplus_user`
- Contraseña: `nominaplus123`

O personaliza:
```bash
./quick_setup_db.sh mi_base_de_datos mi_usuario mi_contraseña
```

### Opción 3: Configuración Manual

Si ya tienes el archivo `.env` configurado, puedes saltar este paso.

## 🏃 Ejecutar la Aplicación

Una vez configurada la base de datos:

```bash
# Asegúrate de que el entorno virtual esté activado
source venv/bin/activate

# Ejecutar la aplicación
python app.py
```

La aplicación:
- Se conectará a PostgreSQL
- Creará automáticamente las tablas (Employee, Attendance, Payroll)
- Estará disponible en: `http://localhost:5000`

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
# Ver empleados
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

## 📝 Verificar Configuración

### Ver contenido del archivo .env:

```bash
cat .env
```

### Probar conexión a PostgreSQL:

```bash
# Ver las bases de datos
sudo -u postgres psql -c "\l"

# Conectar a tu base de datos (después de crearla)
psql -U nominaplus_user -d nominaplus -h localhost
```

## 🔧 Solución de Problemas

### Error: "could not connect to server"

1. Verificar que PostgreSQL esté corriendo:
```bash
sudo systemctl status postgresql
```

2. Si no está corriendo:
```bash
sudo systemctl start postgresql
```

### Error: "password authentication failed"

Verifica que la contraseña en `.env` sea correcta. Puedes cambiarla:

```bash
sudo -u postgres psql
ALTER USER nominaplus_user WITH PASSWORD 'nueva_contraseña';
```

### Error: "database does not exist"

Ejecuta el script de configuración:
```bash
./setup_postgresql_db.sh
```

### Error al crear tablas

Verifica que el usuario tenga permisos:
```bash
sudo -u postgres psql -d nominaplus -c "GRANT ALL ON SCHEMA public TO nominaplus_user;"
```

## 📚 Próximos Pasos

1. ✅ Configurar base de datos
2. ✅ Ejecutar aplicación
3. 📖 Leer `README.md` para documentación completa de la API
4. 🧪 Probar endpoints con `example_requests.py`

## 🎉 ¡Listo!

Tu aplicación NominaPlus está lista para usar con PostgreSQL.

