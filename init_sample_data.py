"""
Script para inicializar datos de ejemplo en la base de datos
Ejecutar solo una vez después de crear las tablas
"""
from app import create_app, db
from app.models import Employee, Attendance, Payroll
from datetime import date, time, timedelta
from decimal import Decimal

def init_sample_data():
    """Inicializa datos de ejemplo"""
    app = create_app()
    
    with app.app_context():
        # Verificar si ya hay datos
        if Employee.query.count() > 0:
            print("Ya existen datos en la base de datos. Saltando inicialización.")
            return
        
        print("Creando datos de ejemplo...")
        
        # Crear empleados de ejemplo
        employees_data = [
            {
                "name": "Juan Pérez",
                "dni": "1234567890123",
                "nit": "12345678-9",
                "position": "Desarrollador Senior",
                "hourly_rate": Decimal("50.00"),
                "address": "Ciudad de Guatemala",
                "phone": "12345678",
                "email": "juan.perez@example.com",
                "bank_account": "1234567890"
            },
            {
                "name": "María González",
                "dni": "9876543210987",
                "nit": "98765432-1",
                "position": "Gerente de Proyectos",
                "hourly_rate": Decimal("75.00"),
                "address": "Antigua Guatemala",
                "phone": "87654321",
                "email": "maria.gonzalez@example.com",
                "bank_account": "0987654321"
            },
            {
                "name": "Carlos Rodríguez",
                "dni": "5555555555555",
                "nit": "55555555-5",
                "position": "Desarrollador Junior",
                "hourly_rate": Decimal("35.00"),
                "address": "Quetzaltenango",
                "phone": "55555555",
                "email": "carlos.rodriguez@example.com",
                "bank_account": "5555555555"
            }
        ]
        
        employees = []
        for emp_data in employees_data:
            employee = Employee(**emp_data)
            db.session.add(employee)
            employees.append(employee)
        
        db.session.commit()
        print(f"✓ Creados {len(employees)} empleados")
        
        # Crear asistencias de ejemplo para el mes actual
        today = date.today()
        start_date = date(today.year, today.month, 1)
        
        # Crear asistencias para los primeros 10 días del mes
        for i, employee in enumerate(employees):
            for day in range(1, min(11, today.day + 1)):
                attendance_date = date(today.year, today.month, day)
                
                # Saltar fines de semana (sábado=5, domingo=6)
                if attendance_date.weekday() >= 5:
                    continue
                
                # Variar las horas de entrada y salida
                in_hour = 8 + (i % 2)  # 8 o 9
                out_hour = 17 + (i % 3)  # 17, 18 o 19
                
                attendance = Attendance(
                    employee_id=employee.id,
                    date=attendance_date,
                    in_time=time(in_hour, 0, 0),
                    out_time=time(out_hour, 0, 0),
                    is_holiday=False,
                    is_vacation=False
                )
                attendance.calculate_hours()
                db.session.add(attendance)
        
        db.session.commit()
        print(f"✓ Creadas asistencias de ejemplo")
        
        print("\n✓ Datos de ejemplo creados exitosamente!")
        print("\nPuedes probar la API con:")
        print("  - GET http://localhost:5000/api/employees")
        print("  - GET http://localhost:5000/api/attendances")
        print("  - POST http://localhost:5000/api/payrolls/calculate")

if __name__ == "__main__":
    init_sample_data()

