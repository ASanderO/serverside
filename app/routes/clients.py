from flask import jsonify, request, abort
from app import db
from app.models import Client
from app.routes import bp
from app.auth import token_required

@bp.route('/clients', methods=['GET'])
@token_required
def get_clients(current_user):
    client_id = request.args.get('clientId')
    if client_id:
        try:
            client = Client.query.get_or_404(client_id)
            return jsonify(client.to_dict()), 200  # HTTP 200 OK
        except Exception as e:
            return jsonify({'message': str(e)}), 500  # HTTP 500 Internal Server Error
    else:
        try:
            clients = Client.query.all()
            return jsonify([client.to_dict() for client in clients]), 200  # HTTP 200 OK
        except Exception as e:
            return jsonify({'message': str(e)}), 500  # HTTP 500 Internal Server Error

@bp.route('/clients/<int:id>', methods=['GET'])
@token_required
def get_client(current_user, id):
    try:
        client = Client.query.get_or_404(id)
        return jsonify(client.to_dict()), 200  # HTTP 200 OK
    except Exception as e:
        return jsonify({'message': str(e)}), 500  # HTTP 500 Internal Server Error

@bp.route('/clients', methods=['POST'])
@token_required
def create_client(current_user):
    try:
        data = request.get_json() or {}
        if 'name' not in data or 'email' not in data:
            return jsonify({'message': 'Name and email are required'}), 400  # HTTP 400 Bad Request
        if Client.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'Email already exists'}), 400  # HTTP 400 Bad Request
        client = Client(name=data['name'], email=data['email'])
        db.session.add(client)
        db.session.commit()
        return jsonify(client.to_dict()), 201  # HTTP 201 Created
    except Exception as e:
        return jsonify({'message': str(e)}), 500  # HTTP 500 Internal Server Error

@bp.route('/clients/<int:id>', methods=['PUT'])
@token_required
def update_client(current_user, id):
    try:
        client = Client.query.get_or_404(id)
        data = request.get_json() or {}
        if 'name' not in data and 'email' not in data:
            return jsonify({'message': 'At least one of name or email is required'}), 400  # HTTP 400 Bad Request
        if 'name' in data:
            client.name = data['name']
        if 'email' in data:
            client.email = data['email']
        db.session.commit()
        return jsonify(client.to_dict()), 200  # HTTP 200 OK
    except Exception as e:
        return jsonify({'message': str(e)}), 500  # HTTP 500 Internal Server Error

@bp.route('/clients/<int:id>', methods=['DELETE'])
@token_required
def delete_client(current_user, id):
    try:
        client = Client.query.get_or_404(id)
        db.session.delete(client)
        db.session.commit()
        return jsonify({'message': 'Client deleted successfully'}), 204  # HTTP 204 No Content
    except Exception as e:
        return jsonify({'message': str(e)}), 500  # HTTP 500 Internal Server Error
