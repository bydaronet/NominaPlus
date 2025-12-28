"""
Utilidades y funciones auxiliares para NominaPlus
"""
from datetime import datetime, date
from decimal import Decimal
from typing import Optional, Tuple


def validate_dni(dni: str) -> bool:
    """
    Valida el formato del DNI
    """
    if not dni:
        return False
    # Validación básica: debe tener entre 8 y 20 caracteres alfanuméricos
    return dni.isalnum() and 8 <= len(dni) <= 20


def validate_email(email: str) -> bool:
    """
    Valida el formato del email
    """
    if not email:
        return False
    return '@' in email and '.' in email.split('@')[1]


def parse_date(date_string: str) -> Optional[date]:
    """
    Convierte una cadena de fecha a objeto date
    """
    try:
        return datetime.strptime(date_string, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return None


def parse_time(time_string: str) -> Optional[datetime.time]:
    """
    Convierte una cadena de hora a objeto time
    """
    try:
        return datetime.strptime(time_string, '%H:%M:%S').time()
    except (ValueError, TypeError):
        try:
            # Intentar con formato HH:MM
            return datetime.strptime(time_string, '%H:%M').time()
        except (ValueError, TypeError):
            return None


def format_currency(amount: Decimal, country_code: str = 'GT') -> str:
    """
    Formatea un monto como moneda según el país
    """
    from app.locales.translations import get_currency_info
    
    currency_info = get_currency_info(country_code)
    symbol = currency_info['symbol']
    
    # Formatear con separadores de miles y decimales
    formatted = f"{amount:,.2f}"
    
    # Ajustar formato según el país
    if country_code == 'AR':
        # Argentina usa punto para miles y coma para decimales
        formatted = formatted.replace(',', 'X').replace('.', ',').replace('X', '.')
    elif country_code == 'ES':
        # España usa punto para miles y coma para decimales
        formatted = formatted.replace(',', 'X').replace('.', ',').replace('X', '.')
    
    return f"{symbol}{formatted}"


def calculate_overtime_rate(base_rate: Decimal, multiplier: Decimal = Decimal('1.5')) -> Decimal:
    """
    Calcula la tasa de horas extras
    """
    return base_rate * multiplier


def get_month_period(year: int, month: int) -> str:
    """
    Obtiene el período en formato YYYY-MM
    """
    return f"{year}-{month:02d}"


def get_current_period() -> str:
    """
    Obtiene el período actual en formato YYYY-MM
    """
    today = date.today()
    return get_month_period(today.year, today.month)


def get_period_dates(period: str) -> Tuple[date, date]:
    """
    Obtiene las fechas de inicio y fin de un período
    """
    year, month = map(int, period.split('-'))
    start_date = date(year, month, 1)
    
    if month == 12:
        end_date = date(year + 1, 1, 1)
    else:
        end_date = date(year, month + 1, 1)
    
    end_date = end_date - date.resolution  # Restar un día para obtener el último día del mes
    
    return start_date, end_date

