from flask import Blueprint, request, jsonify, current_app
from reserva_model import Reserva
from database import db
from external_apis.client import SemesterAPIClient
import requests
import logging
from functools import wraps

logger = logging.getLogger(__name__)
routes = Blueprint("routes", __name__)

def handle_api_error(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"API request failed: {str(e)}")
            return jsonify({"erro": "Erro ao acessar serviço externo"}), 503
        except Exception as e:
            logger.exception(f"Erro inesperado: {str(e)}")
            return jsonify({"erro": "Erro interno do servidor"}), 500
    return wrapper

def validar_turma(turma_id):
    try:
        turma = SemesterAPIClient.get_turma(turma_id)
        return turma is not None
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return False
        current_app.logger.error(f"Erro ao validar turma: {str(e)}")
        raise
    except Exception as e:
        current_app.logger.error(f"Erro inesperado ao validar turma: {str(e)}")
        raise

# def validar_turma(turma_id):
#     resp = requests.get(f"http://localhost:5000/api/turmas/{turma_id}")
#     return resp.status_code == 200

@routes.route("/reservas", methods=["POST"])
@handle_api_error
def criar_reserva():
    dados = request.json
    # turma_id = dados.get("turma_id")

    required_fields = ["turma_id", "sala", "data", "hora_inicio", "hora_fim"]
    if not all(field in dados for field in required_fields):
        return jsonify({"erro": "Dados incompletos"}), 400
    
    dados.pop("id", None)

    if not validar_turma(dados["turma_id"]):
        return jsonify({"erro": "Turma não encontrada"}), 404

    reserva = Reserva(
        turma_id=dados["turma_id"],
        sala=dados("sala"),
        data=dados("data"),
        hora_inicio=dados("hora_inicio"),
        hora_fim=dados("hora_fim")
    )

    db.session.add(reserva)
    db.session.commit()

    return jsonify({
        "mensagem": "Reserva criada com sucesso",
        "id": reserva.id,
        }), 201

@routes.route("/reservas", methods=["GET"])
def listar_reservas():
    reservas = Reserva.query.all()
    return jsonify([
        {
            "id": r.id,
            "turma_id": r.turma_id,
            "sala": r.sala,
            "data": r.data,
            "hora_inicio": r.hora_inicio,
            "hora_fim": r.hora_fim
        } for r in reservas
    ])
