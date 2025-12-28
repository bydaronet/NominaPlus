# Sistema de Localización Multipaís - NominaPlus

## Resumen

NominaPlus ahora soporta múltiples países con terminología y cálculos específicos por país. El sistema está diseñado para ser extensible y fácil de mantener.

## Países Soportados

### 🇦🇷 Argentina (AR)
- **Terminología:**
  - Nómina → **Liquidación de Sueldos**
  - Asistencia → **Presentismo**
  - Recibo → **Recibo de Haberes**
  - DNI → **DNI** / **CUIL** (Código Único de Identificación Laboral)
  - Bonificaciones → **Adicionales**
  - Descuentos → **Retenciones**

- **Cálculos Específicos:**
  - **Aportes de Ley (17% total):**
    - Jubilación: 11%
    - Obra Social: 3%
    - PAMI (Ley 19.032): 3%
  - **Horas Extras:**
    - Días hábiles: 50% extra (1.5x)
    - Sábados (después de 13hs), domingos y feriados: 100% extra (2.0x)
  - **Jornada Legal:** 8 horas diarias / 48 horas semanales
  - **Moneda:** Peso Argentino ($) - ARS

### 🇬🇹 Guatemala (GT) - Original
- **Terminología:** Original del sistema
- **Cálculos:** Lógica original
- **Moneda:** Quetzal (Q) - GTQ

### 🇪🇸 España (ES)
- **Terminología:** Similar a Guatemala
- **Cálculos:** Similar a Guatemala (personalizable)
- **Moneda:** Euro (€) - EUR

## Arquitectura

### 1. Sistema de Localización (`app/locales/`)

```
app/locales/
├── __init__.py
└── translations.py  # Traducciones y configuraciones por país
```

**Funciones principales:**
- `get_translations(country_code)`: Obtiene traducciones
- `get_currency_info(country_code)`: Información de moneda
- `get_country_config(country_code)`: Configuración del país
- `translate(key, country_code)`: Traduce una clave

### 2. Calculadoras por País (`app/logic/calculators.py`)

**Strategy Pattern** para cálculos específicos por país:

```python
from app.logic.calculators import get_calculator

calculator = get_calculator(employee)
result = calculator.calculate_payroll(attendances, period, bonuses, deductions)
```

**Calculadoras disponibles:**
- `ArgentinaCalculator`: Con aportes de ley argentinos
- `GuatemalaCalculator`: Lógica original
- `SpainCalculator`: Similar a Guatemala

### 3. Modelo de Datos

**Employee** ahora incluye:
- `country_code` (String, 2): Código del país (AR, GT, ES)
- `cuil` (String, 15): CUIL para Argentina (formato: XX-XXXXXXXX-X)

## Uso

### Crear un Empleado Argentino

```python
employee = Employee(
    name="Juan Pérez",
    dni="12345678",
    cuil="20-12345678-9",  # CUIL argentino
    country_code="AR",     # Código de país
    position="Desarrollador",
    hourly_rate=Decimal("1500.00"),  # En pesos argentinos
    # ... otros campos
)
```

### Calcular Liquidación de Sueldos

El sistema automáticamente detecta el país del empleado y aplica la calculadora correcta:

```python
# La API detecta automáticamente el país y aplica los aportes
POST /api/payrolls/calculate
{
    "employee_id": 1,
    "period": "2024-12",
    "bonuses": 5000,
    "deductions": 0
}
```

**Respuesta para Argentina:**
```json
{
    "success": true,
    "data": {
        "base_salary": 240000.00,
        "overtime_pay": 15000.00,
        "bonuses": 5000.00,
        "gross_salary": 260000.00,
        "aportes": {
            "jubilacion": 28600.00,
            "obra_social": 7800.00,
            "pami": 7800.00,
            "total_aportes": 44200.00
        },
        "total_amount": 215800.00
    }
}
```

### Obtener Traducciones

```python
GET /api/locale/AR

{
    "success": true,
    "data": {
        "translations": {
            "payroll": "Liquidación de Sueldos",
            "attendance": "Presentismo",
            ...
        },
        "currency": {
            "code": "ARS",
            "symbol": "$",
            "locale": "es-AR"
        }
    }
}
```

## Migración de Base de Datos

Para agregar los nuevos campos a una base de datos existente:

```bash
python migrations/add_country_support.py
```

O manualmente con SQL:

```sql
ALTER TABLE employees 
ADD COLUMN country_code VARCHAR(2) DEFAULT 'GT' NOT NULL;

ALTER TABLE employees 
ADD COLUMN cuil VARCHAR(15) NULL;

CREATE INDEX ix_employees_cuil ON employees(cuil);
```

## Agregar un Nuevo País

### 1. Agregar Traducciones

En `app/locales/translations.py`:

```python
TRANSLATIONS['MX'] = {  # México
    'payroll': 'Nómina',
    'attendance': 'Asistencia',
    # ... más traducciones
}

CURRENCY_INFO['MX'] = {
    'code': 'MXN',
    'symbol': '$',
    'locale': 'es-MX',
    'name': 'Peso Mexicano',
}

COUNTRY_CONFIG['MX'] = {
    'legal_workday_hours': 8,
    'overtime_weekday_multiplier': 1.5,
    # ... configuración
}
```

### 2. Crear Calculadora (si es necesario)

En `app/logic/calculators.py`:

```python
class MexicoCalculator(BaseCalculator):
    def calculate_payroll(self, attendances, period, bonuses, deductions):
        # Lógica específica de México
        pass

# Agregar al factory
calculators['MX'] = MexicoCalculator
```

## Frontend

Los frontends pueden obtener traducciones dinámicamente:

```javascript
// Obtener traducciones
const locale = await fetch('/api/locale/AR').then(r => r.json());

// Usar traducciones
const payrollLabel = locale.data.translations.payroll; // "Liquidación de Sueldos"
```

## Validación de CUIL (Argentina)

Formato CUIL: `XX-XXXXXXXX-X`
- XX: Prefijo (20, 23, 24, 27, etc.)
- XXXXXXXXX: DNI (8 dígitos)
- X: Dígito verificador

Ejemplo: `20-12345678-9`

## Notas Importantes

1. **Compatibilidad:** Los empleados existentes mantienen `country_code='GT'` por defecto
2. **Moneda:** El formato de moneda se ajusta automáticamente según el país
3. **Cálculos:** Los aportes de Argentina se calculan sobre el salario bruto (base + extras + bonificaciones)
4. **Extensibilidad:** Fácil agregar nuevos países siguiendo el patrón establecido

## Próximas Mejoras

- [ ] Validación de formato CUIL
- [ ] Sueldo Anual Complementario (Aguinaldo) para Argentina
- [ ] Exportación de recibos en PDF con formato por país
- [ ] Soporte para múltiples monedas en el mismo sistema
- [ ] Configuración de aportes personalizables por empresa

## Ejemplos de Uso

Ver `example_requests.py` para ejemplos de uso de la API con diferentes países.

