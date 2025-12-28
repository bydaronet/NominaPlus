# NominaPlus

Sistema de gestión de nóminas y control de pagos de empleados desarrollado con Flask y PostgreSQL.

## 🚀 Características

- **Gestión de Empleados**: Registro completo de información personal y laboral
- **Control de Asistencias**: Registro de entradas, salidas, horas trabajadas, días festivos y vacaciones
- **Cálculo de Nóminas**: Generación automática de nóminas con cálculo de horas extras, bonificaciones y descuentos
- **Reportes**: Resúmenes y estadísticas del estado financiero de la empresa
- **API RESTful**: Endpoints completos para todas las operaciones

## 📋 Requisitos Previos

- Python 3.8 o superior
- PostgreSQL 12 o superior
- pip (gestor de paquetes de Python)

## 🔧 Instalación

### 1. Clonar el repositorio

```bash
cd NominaPlus
```

### 2. Crear un entorno virtual (recomendado)

```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar PostgreSQL

1. Crear una base de datos en PostgreSQL:

```sql
CREATE DATABASE nominaplus;
```

2. Crear un archivo `.env` en la raíz del proyecto (puedes usar `.env.example` como referencia):

```bash
cp .env.example .env
```

3. Editar el archivo `.env` con tus credenciales:

```env
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/nominaplus
SECRET_KEY=tu-clave-secreta-aqui
FLASK_ENV=development
FLASK_DEBUG=True
```

### 5. Inicializar la base de datos

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

O si prefieres crear las tablas directamente:

```bash
python app.py
```

La aplicación creará automáticamente las tablas al iniciar.

## 🏃 Ejecución

### Modo Desarrollo

```bash
python app.py
```

O usando Flask directamente:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

La API estará disponible en `http://localhost:5000`

### 6. (Opcional) Cargar datos de ejemplo

Si deseas probar la API con datos de ejemplo:

```bash
python init_sample_data.py
```

Esto creará 3 empleados de ejemplo con algunas asistencias registradas.

## 📚 Documentación de la API

### Endpoints de Empleados

#### Obtener todos los empleados
```
GET /api/employees
Query params: ?is_active=true
```

#### Obtener un empleado
```
GET /api/employees/<id>
```

#### Crear empleado
```
POST /api/employees
Body:
{
  "name": "Juan Pérez",
  "dni": "1234567890",
  "nit": "12345678-9",
  "position": "Desarrollador",
  "hourly_rate": 50.00,
  "address": "Ciudad",
  "phone": "12345678",
  "email": "juan@example.com",
  "bank_account": "1234567890"
}
```

#### Actualizar empleado
```
PUT /api/employees/<id>
Body: (campos a actualizar)
```

#### Desactivar empleado
```
DELETE /api/employees/<id>
```

### Endpoints de Asistencias

#### Obtener asistencias
```
GET /api/attendances
Query params: ?employee_id=1&start_date=2024-01-01&end_date=2024-01-31
```

#### Registrar asistencia
```
POST /api/attendances
Body:
{
  "employee_id": 1,
  "date": "2024-01-15",
  "in_time": "08:00:00",
  "out_time": "17:00:00",
  "is_holiday": false,
  "is_vacation": false,
  "notes": "Asistencia normal"
}
```

#### Actualizar asistencia
```
PUT /api/attendances/<id>
```

#### Eliminar asistencia
```
DELETE /api/attendances/<id>
```

### Endpoints de Nóminas

#### Obtener nóminas
```
GET /api/payrolls
Query params: ?employee_id=1&period=2024-01&status=pending
```

#### Crear nómina manualmente
```
POST /api/payrolls
Body:
{
  "employee_id": 1,
  "period": "2024-01",
  "base_salary": 8000.00,
  "hours_worked": 160,
  "overtime_hours": 10,
  "overtime_pay": 750.00,
  "bonuses": 500.00,
  "deductions": 200.00
}
```

#### Calcular nómina automáticamente
```
POST /api/payrolls/calculate
Body:
{
  "employee_id": 1,
  "period": "2024-01",
  "bonuses": 500.00,
  "deductions": 200.00
}
```

Este endpoint calcula automáticamente la nómina basándose en las asistencias registradas del período.

#### Actualizar nómina
```
PUT /api/payrolls/<id>
Body: (campos a actualizar)
```

### Endpoints de Reportes

#### Resumen general
```
GET /api/reports/summary
Query params: ?period=2024-01
```

## 🗄️ Estructura de la Base de Datos

### Tabla: employees
- `id`: ID único del empleado
- `name`: Nombre completo
- `dni`: Documento de identidad (único)
- `nit`: Número de identificación tributaria
- `address`: Dirección
- `position`: Cargo
- `hourly_rate`: Tasa horaria
- `phone`: Teléfono
- `email`: Correo electrónico
- `bank_account`: Cuenta bancaria
- `is_active`: Estado activo/inactivo

### Tabla: attendances
- `id`: ID único de la asistencia
- `employee_id`: Referencia al empleado
- `date`: Fecha de asistencia
- `in_time`: Hora de entrada
- `out_time`: Hora de salida
- `hours_worked`: Horas trabajadas (calculado)
- `is_holiday`: Es día festivo
- `is_vacation`: Es vacación
- `notes`: Notas adicionales

### Tabla: payrolls
- `id`: ID único de la nómina
- `employee_id`: Referencia al empleado
- `period`: Período (YYYY-MM)
- `base_salary`: Salario base
- `hours_worked`: Horas trabajadas regulares
- `overtime_hours`: Horas extras
- `overtime_pay`: Pago por horas extras
- `bonuses`: Bonificaciones
- `deductions`: Descuentos
- `total_amount`: Monto total (calculado)
- `status`: Estado (pending, confirmed, paid)
- `payment_date`: Fecha de pago
- `bank_transfer_id`: ID de transferencia bancaria

## 🔒 Seguridad

- Las contraseñas y datos sensibles deben almacenarse de forma segura
- Usa HTTPS en producción
- Configura CORS adecuadamente para producción
- Implementa autenticación y autorización según tus necesidades

## 🧪 Testing

Para ejecutar tests (cuando estén implementados):

```bash
pytest
```

## 📝 Notas

- El cálculo de horas extras considera 1.5x la tasa horaria normal
- Las horas extras se calculan cuando se trabajan más de 8 horas por día
- Las vacaciones no se incluyen en el cálculo de horas trabajadas

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

## 👥 Autores

- **Tu Nombre** - *Desarrollo inicial*

## 🙏 Agradecimientos

- Flask y la comunidad de Python
- PostgreSQL

# NominaPlus
