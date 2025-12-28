"""
Script de migración para agregar soporte multipaís
Ejecutar: python migrations/add_country_support.py
"""
from app import create_app, db
from app.models import Employee
from sqlalchemy import text

def migrate():
    """Agrega los campos country_code y cuil a la tabla employees"""
    app = create_app()
    
    with app.app_context():
        try:
            # Verificar si las columnas ya existen
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('employees')]
            
            if 'country_code' not in columns:
                print("Agregando columna country_code...")
                db.engine.execute(text("""
                    ALTER TABLE employees 
                    ADD COLUMN country_code VARCHAR(2) DEFAULT 'GT' NOT NULL
                """))
                print("✓ Columna country_code agregada")
            else:
                print("✓ Columna country_code ya existe")
            
            if 'cuil' not in columns:
                print("Agregando columna cuil...")
                db.engine.execute(text("""
                    ALTER TABLE employees 
                    ADD COLUMN cuil VARCHAR(15) NULL
                """))
                print("✓ Columna cuil agregada")
            else:
                print("✓ Columna cuil ya existe")
            
            # Crear índice para cuil si no existe
            indexes = [idx['name'] for idx in inspector.get_indexes('employees')]
            if 'ix_employees_cuil' not in indexes:
                print("Creando índice para cuil...")
                db.engine.execute(text("""
                    CREATE INDEX ix_employees_cuil ON employees(cuil)
                """))
                print("✓ Índice creado")
            else:
                print("✓ Índice ya existe")
            
            print("\n✅ Migración completada exitosamente")
            
        except Exception as e:
            print(f"❌ Error en la migración: {e}")
            raise

if __name__ == '__main__':
    migrate()

