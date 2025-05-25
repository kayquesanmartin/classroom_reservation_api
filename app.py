import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from database import db
from reserva_route import routes
from external_apis.client import ActivitiesAPIClient, SemesterAPIClient

app = Flask(__name__)

# Configurações do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reservas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configurações das APIs externas
app.config['SEMESTER_API_URL'] = 'http://api_semester_project:5000/api'  # Usando nome do serviço Docker
app.config['ACTIVITIES_API_URL'] = 'http://activities_api:5001/api'  # Exemplo para outra API

# Configuração de logging
def configure_logging():
    """Configura o sistema de logging da aplicação"""
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, 'classroom_reservation.log'),
        maxBytes=10240,
        backupCount=10,
        encoding='utf-8'
    )
    
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    
    # Remove handlers existentes
    for handler in app.logger.handlers[:]:
        app.logger.removeHandler(handler)
    
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Classroom Reservation API iniciada')

# Inicializa extensões
db.init_app(app)
app.register_blueprint(routes)

# Configura logging
configure_logging()

# Cria tabelas do banco de dados
with app.app_context():
    db.create_all()
    app.logger.info('Tabelas do banco de dados verificadas/criadas')

if __name__ == "__main__":
    app.logger.info('Servidor iniciado em modo de desenvolvimento')
    app.run(host='0.0.0.0', port=5003, debug=True)