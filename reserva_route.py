from flask import Blueprint, request, jsonify
from reserva_model import Reserva
from database import db
import requests

routes = Blueprint("routes", __name__)

def validar_turma(turma_id):
    try:
        url = f"http://web:5000/turmas/turmas/{turma_id}"
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()
        print(data)
        return True if data.get('id') else False
    except requests.RequestException as e:
        print(f"Erro ao acessar a turma.service: {e}")
        return False

@routes.route("/reservas", methods=["POST"])
def criar_reserva():
    dados = request.json
    turma_id = dados.get("turma_id")
    print(turma_id)
    if not validar_turma(turma_id):
        return jsonify({"erro": f"Turma não encontrada aaaaaaaaaaa {validar_turma(turma_id)}"}), 400

    reserva = Reserva(
        turma_id=turma_id,
        sala=dados.get("sala"),
        data=dados.get("data"),
        hora_inicio=dados.get("hora_inicio"),
        hora_fim=dados.get("hora_fim")
    )

    db.session.add(reserva)
    db.session.commit()

    return jsonify({"mensagem": "Reserva criada com sucesso"}), 201

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

@routes.route("/reservas/<int:id>", methods=["GET"])
def obter_reserva(id):
    reserva = Reserva.query.get(id)
    if reserva:
        return jsonify({
            "id": reserva.id,
            "turma_id": reserva.turma_id,
            "sala": reserva.sala,
            "data": reserva.data,
            "hora_inicio": reserva.hora_inicio,
            "hora_fim": reserva.hora_fim
        })
    else:
        return jsonify({"erro": "Reserva nao encontrada"}), 404

@routes.route("/reservas/<int:id>", methods=["DELETE"])
def excluir_reserva(id):
    reserva = Reserva.query.get(id)
    if reserva:
        db.session.delete(reserva)
        db.session.commit()
        return jsonify({"mensagem": "Reserva excluida com sucesso"})
    else:
        return jsonify({"erro": "Reserva nao encontrada"}), 404

@routes.route("/reservas/<int:id>", methods=["PUT"])
def atualizar_reserva(id):
    reserva = Reserva.query.get(id)
    if reserva:
        dados = request.json
        reserva.turma_id = dados.get("turma_id")
        reserva.sala = dados.get("sala")
        reserva.data = dados.get("data")
        reserva.hora_inicio = dados.get("hora_inicio")
        reserva.hora_fim = dados.get("hora_fim")
        db.session.commit()
        return jsonify({"mensagem": "Reserva atualizada com sucesso"})
    else:
        return jsonify({"erro": "Reserva nao encontrada"}), 404