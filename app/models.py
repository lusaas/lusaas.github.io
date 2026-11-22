import secrets
from datetime import datetime, timezone

from app import db


def gerar_tag():
    """Gera uma tag aleatória e segura para a URL da coleira NFC."""
    return secrets.token_urlsafe(8)


class Animal(db.Model):
    """Representa o animal atendido pela coleira inteligente."""

    __tablename__ = "animal"

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(32), unique=True, nullable=False, default=gerar_tag)
    nome = db.Column(db.String(100), nullable=False)
    especie = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    vacinas = db.Column(db.Text, nullable=True)
    foto_url = db.Column(db.Text, nullable=True)
    contato = db.Column(db.String(255), nullable=True)

    # Relacionamento com avistamentos (ordem decrescente de data)
    avistamentos = db.relationship(
        "Avistamento",
        backref="animal",
        cascade="all, delete-orphan",
        order_by="Avistamento.criado_em.desc()",
        lazy=True,
    )

    @property
    def lista_fotos(self):
        """Retorna uma lista com todas as URLs de fotos cadastradas (separadas por vírgula ou linha)."""
        if not self.foto_url:
            return []
        urls = [u.strip() for u in self.foto_url.replace("\r", "").replace("\n", ",").split(",")]
        return [u for u in urls if u]

    def __repr__(self):
        return f"<Animal {self.nome} ({self.tag})>"


class Avistamento(db.Model):
    """Registro de localização obtido quando a tag é escaneada."""

    __tablename__ = "avistamento"

    id = db.Column(db.Integer, primary_key=True)
    animal_id = db.Column(db.Integer, db.ForeignKey("animal.id"), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    criado_em = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self):
        return f"<Avistamento Animal {self.animal_id} em {self.criado_em}>"
