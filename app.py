from app import create_app
import os

# Obtener el entorno desde variables de entorno
config_name = os.environ.get('FLASK_ENV', 'development')

# Crear la aplicación
app = create_app(config_name)

@app.route('/')
def home():
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

