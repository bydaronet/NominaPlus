"""
Script simple para agregar columnas country_code y cuil
Ejecutar: python add_columns.py
"""
import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from sqlalchemy import text

def migrate():
    """Agrega los campos country_code y cuil a la tabla employees"""
    app = create_app()
    
    with app.app_context():
        try:
            # Verificar si las columnas ya existen
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('employees')]
            
            print("Columnas existentes:", columns)
            
            if 'country_code' not in columns:
                print("Agregando columna country_code...")
                with db.engine.connect() as conn:
                    conn.execute(text("""
                        ALTER TABLE employees 
                        ADD COLUMN country_code VARCHAR(2) DEFAULT 'GT' NOT NULL
                    """))
                    conn.commit()
                print("✓ Columna country_code agregada")
            else:
                print("✓ Columna country_code ya existe")
            
            if 'cuil' not in columns:
                print("Agregando columna cuil...")
                with db.engine.connect() as conn:
                    conn.execute(text("""
                        ALTER TABLE employees 
                        ADD COLUMN cuil VARCHAR(15) NULL
                    """))
                    conn.commit()
                print("✓ Columna cuil agregada")
            else:
                print("✓ Columna cuil ya existe")
            
            # Verificar índices existentes
            indexes = [idx['name'] for idx in inspector.get_indexes('employees')]
            if 'ix_employees_cuil' not in indexes:
                print("Creando índice para cuil...")
                with db.engine.connect() as conn:
                    conn.execute(text("""
                        CREATE INDEX ix_employees_cuil ON employees(cuil)
                    """))
                    conn.commit()
                print("✓ Índice creado")
            else:
                print("✓ Índice ya existe")
            
            print("\n✅ Migración completada exitosamente")
            
        except Exception as e:
            print(f"❌ Error en la migración: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

if __name__ == '__main__':
    migrate()

