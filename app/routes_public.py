import math
from datetime import timezone
from zoneinfo import ZoneInfo

from flask import Blueprint, abort, jsonify, redirect, render_template, render_template_string, request, url_for

from app import db
from app.models import Animal, Avistamento

# Blueprint com as rotas públicas do sistema
public = Blueprint("public", __name__)

# Fuso horário oficial de Brasília
FUSO_BRASILIA = ZoneInfo("America/Sao_Paulo")


@public.route("/")
def index():
    """Redireciona para o animal ou exibe menu de demonstração se houver múltiplos."""
    todos_animais = Animal.query.all()
    if not todos_animais:
        return "Nenhum animal cadastrado. Execute 'python seed.py'.", 404

    # Filtra os animais principais da demo (Almofadinhas e Caramelo) e deixa Orelha como Easter Egg
    animais_principais = [a for a in todos_animais if a.nome != "Orelha"]
    orelha = next((a for a in todos_animais if a.nome == "Orelha"), None)

    template = """
    {% extends "base.html" %}
    {% block titulo %}Coleiras Disponíveis — GuaipeCare{% endblock %}
    {% block conteudo %}
    <article class="cartao">
        <header class="cabecalho-animal">
            <div class="titulo-linha">
                <h1>Amigos Cadastrados</h1>
                <span class="badge-especie">🐾 Demonstração</span>
            </div>
            <p class="descricao" style="margin-top: 0.25rem;">
                Toque em uma coleira para simular a aproximação da tag NFC:
            </p>
        </header>
        <ul style="list-style: none; padding: 0; display: flex; flex-direction: column; gap: 0.85rem; margin-top: 1rem;">
            {% for animal in animais_principais %}
            <li style="padding: 0.85rem 1rem; border: 1.5px solid #ebdcc8; border-radius: 12px; background: #fdfbf7; box-shadow: 2px 2px 0px #ded0bd; transition: transform 0.15s ease;">
                <a href="{{ url_for('public.pagina_animal', tag=animal.tag) }}" style="text-decoration: none; color: inherit; display: block;">
                    <div style="display: flex; align-items: center; justify-content: space-between;">
                        <strong style="font-family: Georgia, serif; font-size: 1.25rem; color: #362419;">
                            {% if animal.especie|lower in ["cão", "cao", "cadela", "cachorro", "cachorra"] %}🐕{% elif animal.especie|lower in ["gato", "gata"] %}🐈{% else %}🐾{% endif %}
                            {{ animal.nome }}
                        </strong>
                        <span style="font-size: 0.8rem; background: #f5ede1; border: 1px solid #e0d0bc; padding: 0.15rem 0.5rem; border-radius: 12px; color: #5a3e2b; font-weight: 600;">
                            {% if animal.nome == "Almofadinhas" %}Pet da Luísa (Equipe){% else %}{{ animal.especie }}{% endif %}
                        </span>
                    </div>
                    <div style="font-size: 0.82rem; color: #826c5c; margin-top: 0.4rem; display: flex; align-items: center; gap: 0.35rem;">
                        <span>🏷️ Coleira NFC:</span> <code style="background: #f1e6d6; border: 1px solid #decbb5; padding: 0.1rem 0.35rem; border-radius: 4px; font-family: monospace; font-size: 0.8rem; color: #442e20;">/a/{{ animal.tag }}</code>
                    </div>
                </a>
            </li>
            {% endfor %}
        </ul>

        {% if orelha %}
        <footer style="margin-top: 1.5rem; text-align: right; border-top: 1px dashed #e8dfd1; padding-top: 0.75rem;">
            <a href="{{ url_for('public.pagina_animal', tag=orelha.tag) }}" style="font-size: 0.75rem; color: #a89685; text-decoration: none;" title="Memorial do Cão Orelha">
                🕊️ <em>memorial / easter egg</em>
            </a>
        </footer>
        {% endif %}
    </article>
    {% endblock %}
    """
    return render_template_string(template, animais_principais=animais_principais, orelha=orelha)


@public.route("/a/<tag>")
def pagina_animal(tag):
    """Exibe o perfil público do animal identificado pela tag NFC."""
    animal = Animal.query.filter_by(tag=tag).first()
    if animal is None:
        abort(404)

    ultimo_avistamento = "Nenhum registro ainda."
    if animal.avistamentos:
        ultimo = animal.avistamentos[0]
        # Converte a data salva em UTC para o Horário de Brasília
        dt_utc = ultimo.criado_em.replace(tzinfo=timezone.utc)
        dt_bsb = dt_utc.astimezone(FUSO_BRASILIA)
        ultimo_avistamento = dt_bsb.strftime("%d/%m/%Y às %H:%M") + " (Horário de Brasília)"

    return render_template(
        "animal.html",
        animal=animal,
        ultimo_avistamento=ultimo_avistamento,
    )


@public.route("/avistamento/<tag>", methods=["POST"])
def registrar_avistamento(tag):
    """Recebe e registra a geolocalização do avistamento."""
    animal = Animal.query.filter_by(tag=tag).first()
    if animal is None:
        abort(404)

    dados = request.get_json(silent=True)
    if not dados or "latitude" not in dados or "longitude" not in dados:
        return jsonify({"erro": "Requisição inválida ou campos ausentes."}), 400

    lat = dados.get("latitude")
    lon = dados.get("longitude")

    # Valida se os valores são números
    if not isinstance(lat, (int, float)) or not isinstance(lon, (int, float)):
        return jsonify({"erro": "Latitude e longitude devem ser números."}), 400

    # Rejeita NaN e valores infinitos
    if math.isnan(lat) or math.isinf(lat) or math.isnan(lon) or math.isinf(lon):
        return jsonify({"erro": "Valores numéricos inválidos."}), 400

    # Valida intervalos geográficos
    if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
        return jsonify({"erro": "Coordenadas fora dos limites permitidos."}), 400

    # Grava apenas as coordenadas e o animal, sem IP ou dados de quem escaneou
    avistamento = Avistamento(
        animal_id=animal.id,
        latitude=lat,
        longitude=lon,
    )
    db.session.add(avistamento)
    db.session.commit()

    # Formata a nova data e hora em tempo real no Horário de Brasília
    dt_utc = avistamento.criado_em.replace(tzinfo=timezone.utc)
    dt_bsb = dt_utc.astimezone(FUSO_BRASILIA)
    horario_formatado = dt_bsb.strftime("%d/%m/%Y às %H:%M") + " (Horário de Brasília)"

    return jsonify({
        "mensagem": "Avistamento registrado com sucesso.",
        "ultimo_avistamento": horario_formatado
    }), 201
