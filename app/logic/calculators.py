"""
Calculadoras de nómina por país usando Strategy Pattern
"""
from abc import ABC, abstractmethod
from decimal import Decimal
from datetime import date, datetime
from typing import Dict, List, Any
from app.models import Employee, Attendance
from app.locales.translations import get_country_config, get_currency_info


class BaseCalculator(ABC):
    """Clase base para calculadoras de nómina"""
    
    def __init__(self, employee: Employee):
        self.employee = employee
        self.country_code = employee.country_code or 'GT'
        self.config = get_country_config(self.country_code)
        self.currency_info = get_currency_info(self.country_code)
    
    @abstractmethod
    def calculate_payroll(self, attendances: List[Attendance], period: str, 
                         bonuses: Decimal = Decimal('0'), 
                         deductions: Decimal = Decimal('0')) -> Dict[str, Any]:
        """
        Calcula la nómina basándose en las asistencias
        """
        pass
    
    def calculate_overtime(self, hours: Decimal, is_weekend: bool = False) -> Decimal:
        """
        Calcula las horas extras según el tipo de día
        """
        multiplier = (self.config['overtime_weekend_multiplier'] 
                     if is_weekend 
                     else self.config['overtime_weekday_multiplier'])
        return hours * multiplier
    
    def get_regular_hours(self, total_hours: Decimal) -> Decimal:
        """
        Obtiene las horas regulares (hasta el límite legal)
        """
        legal_hours = Decimal(str(self.config['legal_workday_hours']))
        return min(total_hours, legal_hours)
    
    def get_overtime_hours(self, total_hours: Decimal) -> Decimal:
        """
        Obtiene las horas extras (por encima del límite legal)
        """
        legal_hours = Decimal(str(self.config['legal_workday_hours']))
        return max(Decimal('0'), total_hours - legal_hours)


class GuatemalaCalculator(BaseCalculator):
    """Calculadora para Guatemala (lógica original)"""
    
    def calculate_payroll(self, attendances: List[Attendance], period: str,
                         bonuses: Decimal = Decimal('0'),
                         deductions: Decimal = Decimal('0')) -> Dict[str, Any]:
        """
        Calcula la nómina para Guatemala
        """
        total_hours = Decimal('0')
        overtime_hours = Decimal('0')
        regular_hours = Decimal('0')
        
        for att in attendances:
            if att.hours_worked:
                hours = Decimal(str(att.hours_worked))
                total_hours += hours
                
                # Considerar horas extras (más de 8 horas por día)
                if hours > 8:
                    regular_hours += Decimal('8')
                    overtime_hours += (hours - Decimal('8'))
                else:
                    regular_hours += hours
        
        # Calcular salarios
        hourly_rate = Decimal(str(self.employee.hourly_rate))
        base_salary = regular_hours * hourly_rate
        overtime_rate = hourly_rate * Decimal('1.5')  # 50% extra
        overtime_pay = overtime_hours * overtime_rate
        
        total_amount = base_salary + overtime_pay + bonuses - deductions
        
        return {
            'base_salary': base_salary,
            'hours_worked': regular_hours,
            'overtime_hours': overtime_hours,
            'overtime_pay': overtime_pay,
            'bonuses': bonuses,
            'deductions': deductions,
            'total_amount': total_amount,
            'summary': {
                'total_hours': float(total_hours),
                'regular_hours': float(regular_hours),
                'overtime_hours': float(overtime_hours),
            }
        }


class ArgentinaCalculator(BaseCalculator):
    """Calculadora para Argentina con aportes de ley"""
    
    def calculate_payroll(self, attendances: List[Attendance], period: str,
                         bonuses: Decimal = Decimal('0'),
                         deductions: Decimal = Decimal('0')) -> Dict[str, Any]:
        """
        Calcula la liquidación de sueldos para Argentina
        Incluye aportes de ley: Jubilación (11%), Obra Social (3%), PAMI (3%)
        """
        total_hours = Decimal('0')
        overtime_hours_weekday = Decimal('0')
        overtime_hours_weekend = Decimal('0')
        regular_hours = Decimal('0')
        
        legal_hours = Decimal(str(self.config['legal_workday_hours']))
        
        for att in attendances:
            if att.hours_worked and not att.is_vacation:
                hours = Decimal(str(att.hours_worked))
                total_hours += hours
                
                # Determinar si es fin de semana o feriado
                is_weekend = att.date.weekday() >= 5 or att.is_holiday
                
                if hours > legal_hours:
                    regular_hours += legal_hours
                    overtime = hours - legal_hours
                    
                    if is_weekend:
                        overtime_hours_weekend += overtime
                    else:
                        overtime_hours_weekday += overtime
                else:
                    regular_hours += hours
        
        # Calcular salarios
        hourly_rate = Decimal(str(self.employee.hourly_rate))
        base_salary = regular_hours * hourly_rate
        
        # Horas extras: días hábiles 50%, fines de semana/feriados 100%
        overtime_rate_weekday = hourly_rate * Decimal(str(self.config['overtime_weekday_multiplier']))
        overtime_rate_weekend = hourly_rate * Decimal(str(self.config['overtime_weekend_multiplier']))
        
        overtime_pay = (overtime_hours_weekday * overtime_rate_weekday +
                        overtime_hours_weekend * overtime_rate_weekend)
        
        # Total bruto (antes de aportes)
        gross_salary = base_salary + overtime_pay + bonuses
        
        # Aportes de ley (del empleado)
        jubilacion = gross_salary * Decimal(str(self.config['jubilacion_rate']))
        obra_social = gross_salary * Decimal(str(self.config['obra_social_rate']))
        pami = gross_salary * Decimal(str(self.config['pami_rate']))
        total_aportes = jubilacion + obra_social + pami
        
        # Total neto (después de aportes y otros descuentos)
        total_amount = gross_salary - total_aportes - deductions
        
        return {
            'base_salary': base_salary,
            'hours_worked': regular_hours,
            'overtime_hours': overtime_hours_weekday + overtime_hours_weekend,
            'overtime_pay': overtime_pay,
            'bonuses': bonuses,
            'deductions': deductions,
            'gross_salary': gross_salary,
            'jubilacion': jubilacion,
            'obra_social': obra_social,
            'pami': pami,
            'total_aportes': total_aportes,
            'total_amount': total_amount,
            'summary': {
                'total_hours': float(total_hours),
                'regular_hours': float(regular_hours),
                'overtime_hours_weekday': float(overtime_hours_weekday),
                'overtime_hours_weekend': float(overtime_hours_weekend),
                'gross_salary': float(gross_salary),
                'total_aportes': float(total_aportes),
            }
        }


class SpainCalculator(BaseCalculator):
    """Calculadora para España"""
    
    def calculate_payroll(self, attendances: List[Attendance], period: str,
                         bonuses: Decimal = Decimal('0'),
                         deductions: Decimal = Decimal('0')) -> Dict[str, Any]:
        """
        Calcula la nómina para España
        (Similar a Guatemala por ahora, se puede personalizar)
        """
        calculator = GuatemalaCalculator(self.employee)
        return calculator.calculate_payroll(attendances, period, bonuses, deductions)


def get_calculator(employee: Employee) -> BaseCalculator:
    """
    Factory function para obtener la calculadora apropiada según el país del empleado
    """
    country_code = employee.country_code or 'GT'
    
    calculators = {
        'AR': ArgentinaCalculator,
        'GT': GuatemalaCalculator,
        'ES': SpainCalculator,
    }
    
    calculator_class = calculators.get(country_code.upper(), GuatemalaCalculator)
    return calculator_class(employee)

