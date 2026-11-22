import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Configurações da aplicação."""


    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-inseguro")

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "guaipecare.db")

    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Recarrega templates
    TEMPLATES_AUTO_RELOAD = True
    SEND_FILE_MAX_AGE_DEFAULT = 0
