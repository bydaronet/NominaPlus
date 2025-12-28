import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuración base de la aplicación"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32)
    # Soporta tanto PostgreSQL como SQLite
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL:
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        # Fallback a SQLite si no se especifica DATABASE_URL
        SQLALCHEMY_DATABASE_URI = 'sqlite:///nominaplus.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Configuración de la aplicación
    APP_NAME = os.environ.get('APP_NAME', 'NominaPlus')
    APP_VERSION = os.environ.get('APP_VERSION', '1.0.0')
    
    # Configuración de CORS
    CORS_ORIGINS = ['*']  # En producción, especificar dominios permitidos


class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    FLASK_ENV = 'development'


class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    FLASK_ENV = 'production'
    SQLALCHEMY_ECHO = False


class TestingConfig(Config):
    """Configuración para testing"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


# Mapeo de configuraciones
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

