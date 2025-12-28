from flask import Flask, send_from_directory
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import config

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name='default'):
    """Factory function para crear la aplicación Flask"""
    # Configurar rutas para archivos estáticos y templates
    base_dir = os.path.abspath(os.path.dirname(__file__))
    template_dir = os.path.join(base_dir, '..', 'frontend')
    static_dir = os.path.join(base_dir, '..', 'frontend', 'static')
    
    app = Flask(__name__, 
                template_folder=template_dir,
                static_folder=static_dir,
                static_url_path='/static')
    app.config.from_object(config[config_name])
    
    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Importar modelos para que SQLAlchemy los registre
    from app import models
    
    # Registrar blueprints
    from app.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Crear tablas en el contexto de la aplicación
    with app.app_context():
        db.create_all()
    
    return app

