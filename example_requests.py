"""
Ejemplos de uso de la API de NominaPlus
Este archivo contiene ejemplos de cómo hacer peticiones a la API
"""
import requests
import json

BASE_URL = "http://localhost:5000/api"

# Ejemplo 1: Crear un empleado
def create_employee_example():
    """Ejemplo de creación de empleado"""
    url = f"{BASE_URL}/employees"
    data = {
        "name": "Juan Pérez",
        "dni": "1234567890123",
        "nit": "12345678-9",
        "position": "Desarrollador Senior",
        "hourly_rate": 50.00,
        "address": "Ciudad de Guatemala",
        "phone": "12345678",
        "email": "juan.perez@example.com",
        "bank_account": "1234567890",
        "is_active": True
    }
    
    response = requests.post(url, json=data)
    print("Crear empleado:")
    print(json.dumps(response.json(), indent=2))
    return response.json().get('data', {}).get('id')


# Ejemplo 2: Obtener todos los empleados
def get_employees_example():
    """Ejemplo de obtener lista de empleados"""
    url = f"{BASE_URL}/employees"
    response = requests.get(url)
    print("\nObtener empleados:")
    print(json.dumps(response.json(), indent=2))


# Ejemplo 3: Registrar asistencia
def create_attendance_example(employee_id):
    """Ejemplo de registro de asistencia"""
    url = f"{BASE_URL}/attendances"
    data = {
        "employee_id": employee_id,
        "date": "2024-01-15",
        "in_time": "08:00:00",
        "out_time": "17:00:00",
        "is_holiday": False,
        "is_vacation": False,
        "notes": "Asistencia normal"
    }
    
    response = requests.post(url, json=data)
    print("\nRegistrar asistencia:")
    print(json.dumps(response.json(), indent=2))


# Ejemplo 4: Calcular nómina automáticamente
def calculate_payroll_example(employee_id):
    """Ejemplo de cálculo automático de nómina"""
    url = f"{BASE_URL}/payrolls/calculate"
    data = {
        "employee_id": employee_id,
        "period": "2024-01",
        "bonuses": 500.00,
        "deductions": 200.00
    }
    
    response = requests.post(url, json=data)
    print("\nCalcular nómina:")
    print(json.dumps(response.json(), indent=2))


# Ejemplo 5: Obtener resumen de reportes
def get_summary_example():
    """Ejemplo de obtener resumen"""
    url = f"{BASE_URL}/reports/summary"
    params = {"period": "2024-01"}
    response = requests.get(url, params=params)
    print("\nResumen de reportes:")
    print(json.dumps(response.json(), indent=2))


if __name__ == "__main__":
    print("=" * 50)
    print("Ejemplos de uso de la API NominaPlus")
    print("=" * 50)
    print("\nAsegúrate de que el servidor esté corriendo en http://localhost:5000")
    print("\nDescomenta las funciones que quieras probar:\n")
    
    # Descomentar para probar:
    # employee_id = create_employee_example()
    # get_employees_example()
    # create_attendance_example(employee_id)
    # calculate_payroll_example(employee_id)
    # get_summary_example()

