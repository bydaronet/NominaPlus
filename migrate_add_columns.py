"""
Script de migración simple para agregar columnas country_code y cuil
Ejecutar: python migrate_add_columns.py
"""
import os
import sys
import psycopg2
from psycopg2 import sql

# Obtener configuración de base de datos desde variables de entorno o config
def get_db_config():
    """Obtiene la configuración de la base de datos"""
    # Intentar desde variables de entorno
    db_url = os.environ.get('DATABASE_URL')
    if db_url:
        # Parsear DATABASE_URL (formato: postgresql://user:pass@host:port/dbname)
        from urllib.parse import urlparse
        result = urlparse(db_url)
        return {
            'host': result.hostname,
            'port': result.port or 5432,
            'database': result.path[1:],  # Remover el '/' inicial
            'user': result.username,
            'password': result.password
        }
    
    # Valores por defecto
    return {
        'host': os.environ.get('DB_HOST', 'localhost'),
        'port': os.environ.get('DB_PORT', '5432'),
        'database': os.environ.get('DB_NAME', 'nominplus'),
        'user': os.environ.get('DB_USER', 'postgres'),
        'password': os.environ.get('DB_PASSWORD', '')
    }

def migrate():
    """Agrega los campos country_code y cuil a la tabla employees"""
    try:
        config = get_db_config()
        print(f"Conectando a la base de datos: {config['database']}@{config['host']}")
        
        conn = psycopg2.connect(**config)
        cur = conn.cursor()
        
        # Verificar si las columnas ya existen
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'employees'
        """)
        existing_columns = [row[0] for row in cur.fetchall()]
        
        # Agregar country_code si no existe
        if 'country_code' not in existing_columns:
            print("Agregando columna country_code...")
            cur.execute("""
                ALTER TABLE employees 
                ADD COLUMN country_code VARCHAR(2) DEFAULT 'GT' NOT NULL
            """)
            print("✓ Columna country_code agregada")
        else:
            print("✓ Columna country_code ya existe")
        
        # Agregar cuil si no existe
        if 'cuil' not in existing_columns:
            print("Agregando columna cuil...")
            cur.execute("""
                ALTER TABLE employees 
                ADD COLUMN cuil VARCHAR(15) NULL
            """)
            print("✓ Columna cuil agregada")
        else:
            print("✓ Columna cuil ya existe")
        
        # Verificar índices existentes
        cur.execute("""
            SELECT indexname 
            FROM pg_indexes 
            WHERE tablename = 'employees' AND indexname = 'ix_employees_cuil'
        """)
        index_exists = cur.fetchone() is not None
        
        if not index_exists:
            print("Creando índice para cuil...")
            cur.execute("""
                CREATE INDEX ix_employees_cuil ON employees(cuil)
            """)
            print("✓ Índice creado")
        else:
            print("✓ Índice ya existe")
        
        conn.commit()
        print("\n✅ Migración completada exitosamente")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error en la migración: {e}")
        if 'conn' in locals():
            conn.rollback()
        sys.exit(1)

if __name__ == '__main__':
    migrate()

