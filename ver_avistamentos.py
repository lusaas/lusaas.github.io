
from datetime import timezone
from zoneinfo import ZoneInfo

from app import create_app
from app.models import Avistamento

FUSO_BRASILIA = ZoneInfo("America/Sao_Paulo")


def listar_avistamentos():
    app = create_app()

    with app.app_context():
        # Busca os avistamentos ordenados pelo mais recente
        avistamentos = Avistamento.query.order_by(Avistamento.criado_em.desc()).all()

        if not avistamentos:
            print("Nenhum avistamento registrado até o momento.")
            return

        print(f"Total de avistamentos: {len(avistamentos)}\n")
        print(f"{'Data/Hora (Horário de Brasília)':<32} | {'Animal':<15} | {'Latitude':<10} | {'Longitude':<10} | Link Google Maps")
        print("-" * 115)

        for av in avistamentos:
            dt_utc = av.criado_em.replace(tzinfo=timezone.utc)
            dt_bsb = dt_utc.astimezone(FUSO_BRASILIA)
            data_formatada = dt_bsb.strftime("%d/%m/%Y %H:%M:%S")

            link_maps = f"https://www.google.com/maps?q={av.latitude},{av.longitude}"
            nome_animal = av.animal.nome if av.animal else "Desconhecido"

            print(
                f"{data_formatada:<32} | "
                f"{nome_animal:<15} | "
                f"{av.latitude:<10.5f} | "
                f"{av.longitude:<10.5f} | "
                f"{link_maps}"
            )


if __name__ == "__main__":
    listar_avistamentos()
