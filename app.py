from app import create_app
from flask import render_template, send_from_directory
import os

# Obtener el entorno desde variables de entorno
config_name = os.environ.get('FLASK_ENV', 'development')

# Crear la aplicación
app = create_app(config_name)

@app.route('/')
def index():
    """Servir el frontend administrativo"""
    return render_template('index.html')

@app.route('/public')
def public_index():
    """Servir el frontend público para empleados"""
    public_dir = os.path.join(os.path.dirname(__file__), 'frontend_public')
    return send_from_directory(public_dir, 'index.html')

@app.route('/public/static/<path:filename>')
def public_static(filename):
    """Servir archivos estáticos del frontend público"""
    return send_from_directory(os.path.join(os.path.dirname(__file__), 'frontend_public', 'static'), filename)

@app.route('/api')
def api_info():
    """Endpoint raíz de la API"""
    return {
        'message': 'Bienvenido a NominaPlus API',
        'version': app.config.get('APP_VERSION', '1.0.0'),
        'status': 'running'
    }

@app.route('/health')
def health_check():
    """Endpoint para verificar el estado de la API"""
    return {
        'status': 'healthy',
        'service': 'NominaPlus API'
    }

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)

