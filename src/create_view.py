import pandas as pd

from config import get_engine, run_sql_file

VIEWS = [
    "vw_resumo_dispositivo",
    "vw_anomalias",
    "vw_tendencia",
    "vw_leituras_por_hora",
]


def main() -> None:
    engine = get_engine()
    run_sql_file(engine, "view.sql")

    for view in VIEWS:
        total = pd.read_sql(f"SELECT COUNT(*) AS total FROM {view}", engine)
        print(f"  {view}: {int(total['total'][0])} linha(s)")

    print("Views criadas com sucesso! Agora execute: streamlit run src/app.py")


if __name__ == "__main__":
    main()
