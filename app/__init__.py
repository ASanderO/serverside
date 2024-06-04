from flask import Flask, jsonify
from flask_migrate import Migrate
from config import Config
from app.db import db
from app.auth import token_required, auth_bp

migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.config['SECRET_KEY'] = 'your_secret_key'  # Adicione sua chave secreta aqui

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    app.register_blueprint(auth_bp, url_prefix='/auth')

    # Tratadores de erros globais
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'message': 'Bad Request'}), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({'message': 'Unauthorized'}), 401

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'message': 'Not Found'}), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({'message': 'Internal Server Error'}), 500

    @app.errorhandler(503)
    def service_unavailable(error):
        return jsonify({'message': 'Service Unavailable'}), 503

    return app
