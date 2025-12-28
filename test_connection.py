#!/usr/bin/env python3
"""
Script para probar la conexión a PostgreSQL
"""
import os
from dotenv import load_dotenv

load_dotenv()

database_url = os.getenv('DATABASE_URL', '')

if not database_url:
    print("✗ DATABASE_URL no encontrado en .env")
    exit(1)

print(f"✓ DATABASE_URL encontrado: {database_url[:50]}...")

# Intentar importar y crear la app
try:
    from app import create_app, db
    from app.models import Employee, Attendance, Payroll
    
    app = create_app()
    
    with app.app_context():
        # Intentar conectar
        try:
            db.engine.connect()
            print("✓ Conexión a PostgreSQL exitosa")
            
            # Verificar si las tablas existen
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            if tables:
                print(f"✓ Tablas encontradas: {', '.join(tables)}")
            else:
                print("⚠ No hay tablas. La aplicación las creará al iniciar.")
                print("  Ejecuta: python app.py")
        except Exception as e:
            print(f"✗ Error al conectar: {e}")
            print("\nPosibles soluciones:")
            print("  1. Verifica que PostgreSQL esté corriendo: sudo systemctl status postgresql")
            print("  2. Verifica que la base de datos exista")
            print("  3. Ejecuta: ./setup_postgresql_db.sh para crear la base de datos")
            
except Exception as e:
    print(f"✗ Error al cargar la aplicación: {e}")
    import traceback
    traceback.print_exc()

