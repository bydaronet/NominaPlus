from flask import Blueprint, request, jsonify
from datetime import datetime, date, timedelta
from decimal import Decimal
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, and_, or_

from app import db
from app.models import Employee, Attendance, Payroll

api_bp = Blueprint('api', __name__)


# ==================== EMPLEADOS ====================

@api_bp.route('/employees', methods=['GET'])
def get_employees():
    """Obtener lista de empleados"""
    try:
        is_active = request.args.get('is_active', type=str)
        query = Employee.query
        
        if is_active is not None:
            query = query.filter(Employee.is_active == (is_active.lower() == 'true'))
        
        employees = query.order_by(Employee.name).all()
        return jsonify({
            'success': True,
            'data': [employee.to_dict() for employee in employees],
            'count': len(employees)
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@api_bp.route('/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    """Obtener un empleado por ID"""
    try:
        employee = Employee.query.get_or_404(employee_id)
        return jsonify({
            'success': True,
            'data': employee.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 404


@api_bp.route('/employees', methods=['POST'])
def create_employee():
    """Crear un nuevo empleado"""
    try:
        data = request.json
        
        # Validaciones básicas
        if not data.get('name') or not data.get('dni') or not data.get('position'):
            return jsonify({
                'success': False,
                'error': 'Faltan campos requeridos: name, dni, position'
            }), 400
        
        if not data.get('hourly_rate'):
            return jsonify({
                'success': False,
                'error': 'hourly_rate es requerido'
            }), 400
        
        employee = Employee(
            name=data['name'],
            dni=data['dni'],
            nit=data.get('nit'),
            address=data.get('address'),
            position=data['position'],
            hourly_rate=Decimal(str(data['hourly_rate'])),
            phone=data.get('phone'),
            email=data.get('email'),
            bank_account=data.get('bank_account'),
            is_active=data.get('is_active', True)
        )
        
        db.session.add(employee)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': employee.to_dict(),
            'message': 'Empleado creado exitosamente'
        }), 201
        
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'El DNI o NIT ya existe en el sistema'
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@api_bp.route('/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    """Actualizar un empleado"""
    try:
        employee = Employee.query.get_or_404(employee_id)
        data = request.json
        
        if 'name' in data:
            employee.name = data['name']
        if 'dni' in data:
            employee.dni = data['dni']
        if 'nit' in data:
            employee.nit = data['nit']
        if 'address' in data:
            employee.address = data['address']
        if 'position' in data:
            employee.position = data['position']
        if 'hourly_rate' in data:
            employee.hourly_rate = Decimal(str(data['hourly_rate']))
        if 'phone' in data:
            employee.phone = data['phone']
        if 'email' in data:
            employee.email = data['email']
        if 'bank_account' in data:
            employee.bank_account = data['bank_account']
        if 'is_active' in data:
            employee.is_active = data['is_active']
        
        employee.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': employee.to_dict(),
            'message': 'Empleado actualizado exitosamente'
        }), 200
        
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'El DNI o NIT ya existe en el sistema'
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@api_bp.route('/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    """Eliminar un empleado (soft delete)"""
    try:
        employee = Employee.query.get_or_404(employee_id)
        employee.is_active = False
        employee.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Empleado desactivado exitosamente'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== ASISTENCIAS ====================

@api_bp.route('/attendances', methods=['GET'])
def get_attendances():
    """Obtener lista de asistencias"""
    try:
        employee_id = request.args.get('employee_id', type=int)
        start_date = request.args.get('start_date', type=str)
        end_date = request.args.get('end_date', type=str)
        
        query = Attendance.query
        
        if employee_id:
            query = query.filter(Attendance.employee_id == employee_id)
        
        if start_date:
            query = query.filter(Attendance.date >= datetime.strptime(start_date, '%Y-%m-%d').date())
        
        if end_date:
            query = query.filter(Attendance.date <= datetime.strptime(end_date, '%Y-%m-%d').date())
        
        attendances = query.order_by(Attendance.date.desc(), Attendance.in_time.desc()).all()
        
        return jsonify({
            'success': True,
            'data': [attendance.to_dict() for attendance in attendances],
            'count': len(attendances)
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@api_bp.route('/attendances/<int:attendance_id>', methods=['GET'])
def get_attendance(attendance_id):
    """Obtener una asistencia por ID"""
    try:
        attendance = Attendance.query.get_or_404(attendance_id)
        return jsonify({
            'success': True,
            'data': attendance.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 404


@api_bp.route('/attendances', methods=['POST'])
def create_attendance():
    """Registrar una nueva asistencia"""
    try:
        data = request.json
        
        if not data.get('employee_id') or not data.get('date') or not data.get('in_time'):
            return jsonify({
                'success': False,
                'error': 'Faltan campos requeridos: employee_id, date, in_time'
            }), 400
        
        # Verificar que el empleado existe
        employee = Employee.query.get_or_404(data['employee_id'])
        
        attendance_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        in_time = datetime.strptime(data['in_time'], '%H:%M:%S').time()
        out_time = None
        if data.get('out_time'):
            out_time = datetime.strptime(data['out_time'], '%H:%M:%S').time()
        
        attendance = Attendance(
            employee_id=data['employee_id'],
            date=attendance_date,
            in_time=in_time,
            out_time=out_time,
            is_holiday=data.get('is_holiday', False),
            is_vacation=data.get('is_vacation', False),
            notes=data.get('notes')
        )
        
        # Calcular horas trabajadas si hay hora de salida
        if out_time:
            attendance.calculate_hours()
        
        db.session.add(attendance)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': attendance.to_dict(),
            'message': 'Asistencia registrada exitosamente'
        }), 201
        
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Ya existe un registro de asistencia para este empleado en esta fecha'
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@api_bp.route('/attendances/<int:attendance_id>', methods=['PUT'])
def update_attendance(attendance_id):
    """Actualizar una asistencia"""
    try:
        attendance = Attendance.query.get_or_404(attendance_id)
        data = request.json
        
        if 'date' in data:
            attendance.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        if 'in_time' in data:
            attendance.in_time = datetime.strptime(data['in_time'], '%H:%M:%S').time()
        if 'out_time' in data:
            attendance.out_time = datetime.strptime(data['out_time'], '%H:%M:%S').time()
        if 'is_holiday' in data:
            attendance.is_holiday = data['is_holiday']
        if 'is_vacation' in data:
            attendance.is_vacation = data['is_vacation']
        if 'notes' in data:
            attendance.notes = data['notes']
        
        # Recalcular horas si hay cambios en las horas
        if 'in_time' in data or 'out_time' in data:
            if attendance.out_time:
                attendance.calculate_hours()
        
        attendance.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': attendance.to_dict(),
            'message': 'Asistencia actualizada exitosamente'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@api_bp.route('/attendances/<int:attendance_id>', methods=['DELETE'])
def delete_attendance(attendance_id):
    """Eliminar una asistencia"""
    try:
        attendance = Attendance.query.get_or_404(attendance_id)
        db.session.delete(attendance)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Asistencia eliminada exitosamente'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== NÓMINAS ====================

@api_bp.route('/payrolls', methods=['GET'])
def get_payrolls():
    """Obtener lista de nóminas"""
    try:
        employee_id = request.args.get('employee_id', type=int)
        period = request.args.get('period', type=str)
        status = request.args.get('status', type=str)
        
        query = Payroll.query
        
        if employee_id:
            query = query.filter(Payroll.employee_id == employee_id)
        if period:
            query = query.filter(Payroll.period == period)
        if status:
            query = query.filter(Payroll.status == status)
        
        payrolls = query.order_by(Payroll.period.desc(), Payroll.created_at.desc()).all()
        
        return jsonify({
            'success': True,
            'data': [payroll.to_dict() for payroll in payrolls],
            'count': len(payrolls)
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@api_bp.route('/payrolls/<int:payroll_id>', methods=['GET'])
def get_payroll(payroll_id):
    """Obtener una nómina por ID"""
    try:
        payroll = Payroll.query.get_or_404(payroll_id)
        return jsonify({
            'success': True,
            'data': payroll.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 404


@api_bp.route('/payrolls', methods=['POST'])
def create_payroll():
    """Crear una nueva nómina"""
    try:
        data = request.json
        
        if not data.get('employee_id') or not data.get('period'):
            return jsonify({
                'success': False,
                'error': 'Faltan campos requeridos: employee_id, period'
            }), 400
        
        # Verificar que el empleado existe
        employee = Employee.query.get_or_404(data['employee_id'])
        
        payroll = Payroll(
            employee_id=data['employee_id'],
            period=data['period'],
            base_salary=Decimal(str(data.get('base_salary', 0))),
            hours_worked=Decimal(str(data.get('hours_worked', 0))),
            overtime_hours=Decimal(str(data.get('overtime_hours', 0))),
            overtime_pay=Decimal(str(data.get('overtime_pay', 0))),
            bonuses=Decimal(str(data.get('bonuses', 0))),
            deductions=Decimal(str(data.get('deductions', 0))),
            status=data.get('status', 'pending'),
            notes=data.get('notes')
        )
        
        payroll.calculate_total()
        
        db.session.add(payroll)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': payroll.to_dict(),
            'message': 'Nómina creada exitosamente'
        }), 201
        
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Ya existe una nómina para este empleado en este período'
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@api_bp.route('/payrolls/<int:payroll_id>', methods=['PUT'])
def update_payroll(payroll_id):
    """Actualizar una nómina"""
    try:
        payroll = Payroll.query.get_or_404(payroll_id)
        data = request.json
        
        if 'period' in data:
            payroll.period = data['period']
        if 'base_salary' in data:
            payroll.base_salary = Decimal(str(data['base_salary']))
        if 'hours_worked' in data:
            payroll.hours_worked = Decimal(str(data['hours_worked']))
        if 'overtime_hours' in data:
            payroll.overtime_hours = Decimal(str(data['overtime_hours']))
        if 'overtime_pay' in data:
            payroll.overtime_pay = Decimal(str(data['overtime_pay']))
        if 'bonuses' in data:
            payroll.bonuses = Decimal(str(data['bonuses']))
        if 'deductions' in data:
            payroll.deductions = Decimal(str(data['deductions']))
        if 'status' in data:
            payroll.status = data['status']
        if 'payment_date' in data:
            payroll.payment_date = datetime.strptime(data['payment_date'], '%Y-%m-%d').date()
        if 'bank_transfer_id' in data:
            payroll.bank_transfer_id = data['bank_transfer_id']
        if 'notes' in data:
            payroll.notes = data['notes']
        
        payroll.calculate_total()
        payroll.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': payroll.to_dict(),
            'message': 'Nómina actualizada exitosamente'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@api_bp.route('/payrolls/<int:payroll_id>', methods=['DELETE'])
def delete_payroll(payroll_id):
    """Eliminar una nómina"""
    try:
        payroll = Payroll.query.get_or_404(payroll_id)
        db.session.delete(payroll)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Nómina eliminada exitosamente'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== CÁLCULO AUTOMÁTICO DE NÓMINA ====================

@api_bp.route('/payrolls/calculate', methods=['POST'])
def calculate_payroll():
    """Calcular nómina automáticamente basándose en asistencias"""
    try:
        data = request.json
        
        if not data.get('employee_id') or not data.get('period'):
            return jsonify({
                'success': False,
                'error': 'Faltan campos requeridos: employee_id, period'
            }), 400
        
        employee = Employee.query.get_or_404(data['employee_id'])
        
        # Obtener año y mes del período
        year, month = map(int, data['period'].split('-'))
        start_date = date(year, month, 1)
        
        # Calcular último día del mes
        if month == 12:
            end_date = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = date(year, month + 1, 1) - timedelta(days=1)
        
        # Obtener asistencias del período
        attendances = Attendance.query.filter(
            and_(
                Attendance.employee_id == data['employee_id'],
                Attendance.date >= start_date,
                Attendance.date <= end_date,
                ~Attendance.is_vacation  # Excluir vacaciones
            )
        ).all()
        
        # Calcular horas trabajadas
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
        hourly_rate = Decimal(str(employee.hourly_rate))
        base_salary = regular_hours * hourly_rate
        overtime_rate = hourly_rate * Decimal('1.5')  # 50% extra para horas extras
        overtime_pay = overtime_hours * overtime_rate
        
        # Bonificaciones y descuentos (pueden venir en el request)
        bonuses = Decimal(str(data.get('bonuses', 0)))
        deductions = Decimal(str(data.get('deductions', 0)))
        
        total_amount = base_salary + overtime_pay + bonuses - deductions
        
        # Crear o actualizar nómina
        payroll = Payroll.query.filter_by(
            employee_id=data['employee_id'],
            period=data['period']
        ).first()
        
        if payroll:
            # Actualizar nómina existente
            payroll.base_salary = base_salary
            payroll.hours_worked = regular_hours
            payroll.overtime_hours = overtime_hours
            payroll.overtime_pay = overtime_pay
            payroll.bonuses = bonuses
            payroll.deductions = deductions
            payroll.calculate_total()
        else:
            # Crear nueva nómina
            payroll = Payroll(
                employee_id=data['employee_id'],
                period=data['period'],
                base_salary=base_salary,
                hours_worked=regular_hours,
                overtime_hours=overtime_hours,
                overtime_pay=overtime_pay,
                bonuses=bonuses,
                deductions=deductions,
                status='pending'
            )
            payroll.calculate_total()
            db.session.add(payroll)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': payroll.to_dict(),
            'message': 'Nómina calculada exitosamente',
            'summary': {
                'total_hours': float(total_hours),
                'regular_hours': float(regular_hours),
                'overtime_hours': float(overtime_hours),
                'base_salary': float(base_salary),
                'overtime_pay': float(overtime_pay)
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== REPORTES ====================

@api_bp.route('/reports/summary', methods=['GET'])
def get_summary_report():
    """Obtener resumen general de la empresa"""
    try:
        period = request.args.get('period', type=str)
        
        # Si no se especifica período, usar el mes actual
        if not period:
            today = date.today()
            period = f"{today.year}-{today.month:02d}"
        
        # Estadísticas de empleados
        total_employees = Employee.query.filter_by(is_active=True).count()
        
        # Estadísticas de nóminas
        payrolls_query = Payroll.query.filter_by(period=period)
        total_payrolls = payrolls_query.count()
        total_paid = db.session.query(func.sum(Payroll.total_amount)).filter(
            and_(Payroll.period == period, Payroll.status == 'paid')
        ).scalar() or Decimal('0')
        
        # Estadísticas de asistencias
        year, month = map(int, period.split('-'))
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = date(year, month + 1, 1) - timedelta(days=1)
        
        total_attendances = Attendance.query.filter(
            and_(
                Attendance.date >= start_date,
                Attendance.date <= end_date
            )
        ).count()
        
        return jsonify({
            'success': True,
            'data': {
                'period': period,
                'employees': {
                    'total_active': total_employees
                },
                'payrolls': {
                    'total': total_payrolls,
                    'total_paid': float(total_paid)
                },
                'attendances': {
                    'total': total_attendances
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

