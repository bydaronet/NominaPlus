"""
Traducciones y configuraciones por país
"""
from typing import Dict, Any

# Traducciones por país
TRANSLATIONS: Dict[str, Dict[str, str]] = {
    'AR': {  # Argentina
        'payroll': 'Liquidación de Sueldos',
        'payrolls': 'Liquidaciones de Sueldos',
        'payroll_detail': 'Detalle de Liquidación',
        'hourly_rate': 'Valor Hora',
        'base_salary': 'Sueldo Básico',
        'bonuses': 'Adicionales',
        'deductions': 'Retenciones',
        'overtime': 'Horas Extras',
        'overtime_pay': 'Pago por Horas Extras',
        'period': 'Mes de Devengamiento',
        'attendance': 'Presentismo',
        'attendances': 'Control de Presentismo',
        'employee': 'Empleado',
        'employees': 'Empleados',
        'dni': 'DNI',
        'cuil': 'CUIL',
        'total': 'Total a Cobrar',
        'status_pending': 'Pendiente',
        'status_confirmed': 'Confirmado',
        'status_paid': 'Pagado',
        'receipt': 'Recibo de Haberes',
        'receipts': 'Recibos de Haberes',
        'jubilacion': 'Jubilación (11%)',
        'obra_social': 'Obra Social (3%)',
        'pami': 'PAMI - Ley 19.032 (3%)',
        'total_aportes': 'Total Aportes (17%)',
    },
    'GT': {  # Guatemala (original)
        'payroll': 'Nómina',
        'payrolls': 'Nóminas',
        'payroll_detail': 'Detalle de Nómina',
        'hourly_rate': 'Tarifa por Hora',
        'base_salary': 'Salario Base',
        'bonuses': 'Bonificaciones',
        'deductions': 'Descuentos',
        'overtime': 'Horas Extras',
        'overtime_pay': 'Pago por Horas Extras',
        'period': 'Período',
        'attendance': 'Asistencia',
        'attendances': 'Asistencias',
        'employee': 'Empleado',
        'employees': 'Empleados',
        'dni': 'DNI',
        'cuil': 'NIT',
        'total': 'Total',
        'status_pending': 'Pendiente',
        'status_confirmed': 'Confirmado',
        'status_paid': 'Pagado',
        'receipt': 'Recibo',
        'receipts': 'Recibos',
    },
    'ES': {  # España
        'payroll': 'Nómina',
        'payrolls': 'Nóminas',
        'payroll_detail': 'Detalle de Nómina',
        'hourly_rate': 'Tarifa por Hora',
        'base_salary': 'Salario Base',
        'bonuses': 'Bonificaciones',
        'deductions': 'Descuentos',
        'overtime': 'Horas Extras',
        'overtime_pay': 'Pago por Horas Extras',
        'period': 'Período',
        'attendance': 'Asistencia',
        'attendances': 'Asistencias',
        'employee': 'Empleado',
        'employees': 'Empleados',
        'dni': 'DNI',
        'cuil': 'NIE',
        'total': 'Total',
        'status_pending': 'Pendiente',
        'status_confirmed': 'Confirmado',
        'status_paid': 'Pagado',
        'receipt': 'Recibo',
        'receipts': 'Recibos',
    },
}

# Información de moneda por país
CURRENCY_INFO: Dict[str, Dict[str, Any]] = {
    'AR': {
        'code': 'ARS',
        'symbol': '$',
        'locale': 'es-AR',
        'name': 'Peso Argentino',
    },
    'GT': {
        'code': 'GTQ',
        'symbol': 'Q',
        'locale': 'es-GT',
        'name': 'Quetzal',
    },
    'ES': {
        'code': 'EUR',
        'symbol': '€',
        'locale': 'es-ES',
        'name': 'Euro',
    },
}

# Configuraciones por país
COUNTRY_CONFIG: Dict[str, Dict[str, Any]] = {
    'AR': {
        'legal_workday_hours': 8,
        'legal_workweek_hours': 48,
        'overtime_weekday_multiplier': 1.5,  # 50% extra
        'overtime_weekend_multiplier': 2.0,  # 100% extra
        'jubilacion_rate': 0.11,  # 11%
        'obra_social_rate': 0.03,  # 3%
        'pami_rate': 0.03,  # 3%
        'total_aportes_rate': 0.17,  # 17% total
    },
    'GT': {
        'legal_workday_hours': 8,
        'legal_workweek_hours': 48,
        'overtime_weekday_multiplier': 1.5,
        'overtime_weekend_multiplier': 2.0,
    },
    'ES': {
        'legal_workday_hours': 8,
        'legal_workweek_hours': 40,
        'overtime_weekday_multiplier': 1.5,
        'overtime_weekend_multiplier': 2.0,
    },
}


def get_translations(country_code: str = 'GT') -> Dict[str, str]:
    """
    Obtiene las traducciones para un país específico
    """
    return TRANSLATIONS.get(country_code.upper(), TRANSLATIONS['GT'])


def get_currency_info(country_code: str = 'GT') -> Dict[str, Any]:
    """
    Obtiene la información de moneda para un país específico
    """
    return CURRENCY_INFO.get(country_code.upper(), CURRENCY_INFO['GT'])


def get_country_config(country_code: str = 'GT') -> Dict[str, Any]:
    """
    Obtiene la configuración de país
    """
    return COUNTRY_CONFIG.get(country_code.upper(), COUNTRY_CONFIG['GT'])


def translate(key: str, country_code: str = 'GT', default: str = None) -> str:
    """
    Traduce una clave según el país
    """
    translations = get_translations(country_code)
    return translations.get(key, default or key)

