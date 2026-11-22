from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    
    app = Flask(__name__)


    from config import Config
    app.config.from_object(Config)

    
    db.init_app(app)

    
    from app import models  # noqa: F401
    from app.routes_public import public
    app.register_blueprint(public)

    # Criar as tabelas no banco de dados e dados da demo caso vazio
    with app.app_context():
        db.create_all()

        from app.models import Animal
        if Animal.query.first() is None:
            from seed import cadastrar_animais
            cadastrar_animais(app)

    return app
