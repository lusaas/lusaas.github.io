"""Script para popular o banco de dados com os animais da demonstração do GuaipeCare.

Garante que os dados da demo fiquem salvos de forma reproduzível:
- Tags NFC fixas e estáveis para a apresentação (não mudam ao rodar o seed)
- Suporte a múltiplas fotos por animal (separadas por vírgula)
- Histórico de avistamento inicial pré-configurado
"""

from datetime import datetime, timezone
from zoneinfo import ZoneInfo

# ==============================================================================
# DADOS DOS ANIMAIS DA DEMO — Edite ou adicione novos animais aqui
# ==============================================================================
ANIMAIS_DEMO = [
    {
        "nome": "Almofadinhas",
        "tag": "almofadinhas",
        "especie": "Cadela",
        "descricao": "Cachorrinha da Luísa Böhm, muito carinhosa, brincalhona, companheira e cheia de energia. Adora passear e receber carinho de todo mundo!",
        "vacinas": "Polivalente V10 (em dia)\nAntirrábica (em dia)\nVermifugada e castrada",
        "foto_url": "/static/img/001.jpeg, /static/img/002.jpeg, /static/img/003.jpeg, /static/img/004.jpeg, /static/img/005.jpeg, /static/img/006.jpeg",
        "contato": "Tutora: Luísa Böhm — (53) 96767-6767",
        "avistamento_inicial": {
            "latitude": -31.7719,
            "longitude": -52.3426,
            "data_sp": datetime(2026, 11, 22, 9, 30, tzinfo=ZoneInfo("America/Sao_Paulo")),
        },
        "destaque_demo": True,
    },
    {
        "nome": "Caramelo",
        "tag": "QI3u1Kd84hk",
        "especie": "Cão",
        "descricao": "Vira-lata comunitário muito dócil, brincalhão e castrado. Vive no campus e é cuidado com carinho pela comunidade acadêmica.",
        "vacinas": "Polivalente V10 (15/03/2026)\nAntirrábica (10/06/2026)",
        "foto_url": "https://images.unsplash.com/photo-1543466835-00a7907e9de1?auto=format&fit=crop&w=600&q=80, https://images.unsplash.com/photo-1587300003388-59208cc962cb?auto=format&fit=crop&w=600&q=80",
        "contato": "ONG Amigos dos Bichos: (53) 99999-8888 | contato@amigosdosbichos.org",
        "avistamento_inicial": {
            "latitude": -31.7654,
            "longitude": -52.3376,
            "data_sp": datetime(2026, 11, 21, 14, 0, tzinfo=ZoneInfo("America/Sao_Paulo")),
        },
        "destaque_demo": True,
    },
    {
        "nome": "Orelha",
        "tag": "tsLaXibfAwM",
        "especie": "Cão",
        "descricao": "Daniel Pontes deseja justiça pelo seu cachorro.",
        "vacinas": "Polivalente V10 (em dia)\nAntirrábica (em dia)\nCastrado e microchipado",
        "foto_url": "/static/img/cao-orelha-3.jpg, /static/img/orelha-daniel.jpg",
        "contato": "Coletivo de Cuidadores Comunitários: (48) 99888-0000 | memorial.orelha@guaipecare.org",
        "avistamento_inicial": {
            "latitude": -27.4011,
            "longitude": -48.4116,
            "data_sp": datetime(2026, 1, 4, 10, 0, tzinfo=ZoneInfo("America/Sao_Paulo")),
        },
        "destaque_demo": False,  # Easter Egg da demo
    },
]
# ==============================================================================

from app import db
from app.models import Animal, Avistamento


def cadastrar_animais(app=None):
    """Cadastra ou atualiza os animais da demo no banco de dados."""
    if app is None:
        from app import create_app
        app = create_app()

    with app.app_context():
        print("Sincronizando animais de demonstração do GuaipeCare:\n")

        for dados in ANIMAIS_DEMO:
            animal = Animal.query.filter_by(nome=dados["nome"]).first()

            if animal is None:
                animal = Animal(
                    nome=dados["nome"],
                    tag=dados["tag"],
                    especie=dados["especie"],
                    descricao=dados["descricao"],
                    vacinas=dados["vacinas"],
                    foto_url=dados["foto_url"],
                    contato=dados["contato"],
                )
                db.session.add(animal)
                db.session.flush()
                print(f"+ '{animal.nome}' criado -> /a/{animal.tag}")
            else:
                animal.tag = dados["tag"]
                animal.descricao = dados["descricao"]
                animal.vacinas = dados["vacinas"]
                animal.foto_url = dados["foto_url"]
                animal.contato = dados["contato"]
                print(f"✓ '{animal.nome}' atualizado -> /a/{animal.tag}")

            if not animal.avistamentos and "avistamento_inicial" in dados:
                av_info = dados["avistamento_inicial"]
                dt_utc = av_info["data_sp"].astimezone(timezone.utc).replace(tzinfo=None)
                avistamento = Avistamento(
                    animal_id=animal.id,
                    latitude=av_info["latitude"],
                    longitude=av_info["longitude"],
                    criado_em=dt_utc,
                )
                db.session.add(avistamento)

        db.session.commit()
        print("\nTodos os dados da demo foram salvos com sucesso!")


if __name__ == "__main__":
    cadastrar_animais()
