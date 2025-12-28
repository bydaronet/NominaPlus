from datetime import datetime, date, time
from app import db
from sqlalchemy.orm import relationship


class Employee(db.Model):
    """Modelo para empleados"""
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(20), unique=True, nullable=False, index=True)
    nit = db.Column(db.String(20), unique=True, nullable=True)
    address = db.Column(db.Text, nullable=True)
    position = db.Column(db.String(100), nullable=False)
    hourly_rate = db.Column(db.Numeric(10, 2), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    bank_account = db.Column(db.String(50), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relaciones
    attendances = relationship('Attendance', back_populates='employee', cascade='all, delete-orphan')
    payrolls = relationship('Payroll', back_populates='employee', cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'name': self.name,
            'dni': self.dni,
            'nit': self.nit,
            'address': self.address,
            'position': self.position,
            'hourly_rate': float(self.hourly_rate) if self.hourly_rate else None,
            'phone': self.phone,
            'email': self.email,
            'bank_account': self.bank_account,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Employee {self.name} - {self.dni}>'


class Attendance(db.Model):
    """Modelo para control de asistencias"""
    __tablename__ = 'attendances'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False, index=True)
    date = db.Column(db.Date, nullable=False, index=True)
    in_time = db.Column(db.Time, nullable=False)
    out_time = db.Column(db.Time, nullable=True)
    hours_worked = db.Column(db.Numeric(5, 2), nullable=True)
    is_holiday = db.Column(db.Boolean, default=False, nullable=False)
    is_vacation = db.Column(db.Boolean, default=False, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relaciones
    employee = relationship('Employee', back_populates='attendances')
    
    # Índice único para evitar registros duplicados
    __table_args__ = (db.UniqueConstraint('employee_id', 'date', name='unique_employee_date'),)
    
    def calculate_hours(self):
        """Calcula las horas trabajadas basándose en in_time y out_time"""
        if self.in_time and self.out_time:
            in_datetime = datetime.combine(self.date, self.in_time)
            out_datetime = datetime.combine(self.date, self.out_time)
            if out_datetime < in_datetime:
                # Si la salida es al día siguiente
                out_datetime = datetime.combine(
                    date.fromordinal(self.date.toordinal() + 1),
                    self.out_time
                )
            delta = out_datetime - in_datetime
            hours = delta.total_seconds() / 3600
            self.hours_worked = round(hours, 2)
        return self.hours_worked
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'employee_name': self.employee.name if self.employee else None,
            'date': self.date.isoformat() if self.date else None,
            'in_time': self.in_time.strftime('%H:%M:%S') if self.in_time else None,
            'out_time': self.out_time.strftime('%H:%M:%S') if self.out_time else None,
            'hours_worked': float(self.hours_worked) if self.hours_worked else None,
            'is_holiday': self.is_holiday,
            'is_vacation': self.is_vacation,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Attendance {self.employee_id} - {self.date}>'


class Payroll(db.Model):
    """Modelo para nóminas"""
    __tablename__ = 'payrolls'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False, index=True)
    period = db.Column(db.String(7), nullable=False, index=True)  # Formato: YYYY-MM
    base_salary = db.Column(db.Numeric(10, 2), nullable=False)
    hours_worked = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    overtime_hours = db.Column(db.Numeric(6, 2), nullable=False, default=0)
    overtime_pay = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    bonuses = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    deductions = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(20), default='pending', nullable=False)  # pending, confirmed, paid
    payment_date = db.Column(db.Date, nullable=True)
    bank_transfer_id = db.Column(db.String(100), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relaciones
    employee = relationship('Employee', back_populates='payrolls')
    
    # Índice único para evitar nóminas duplicadas
    __table_args__ = (db.UniqueConstraint('employee_id', 'period', name='unique_employee_period'),)
    
    def calculate_total(self):
        """Calcula el total de la nómina"""
        self.total_amount = (
            self.base_salary +
            self.overtime_pay +
            self.bonuses -
            self.deductions
        )
        return self.total_amount
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'employee_name': self.employee.name if self.employee else None,
            'period': self.period,
            'base_salary': float(self.base_salary) if self.base_salary else None,
            'hours_worked': float(self.hours_worked) if self.hours_worked else None,
            'overtime_hours': float(self.overtime_hours) if self.overtime_hours else None,
            'overtime_pay': float(self.overtime_pay) if self.overtime_pay else None,
            'bonuses': float(self.bonuses) if self.bonuses else None,
            'deductions': float(self.deductions) if self.deductions else None,
            'total_amount': float(self.total_amount) if self.total_amount else None,
            'status': self.status,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None,
            'bank_transfer_id': self.bank_transfer_id,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Payroll {self.employee_id} - {self.period}>'

