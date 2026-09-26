import pandas as pd
import plotly.express as px
import streamlit as st

from config import get_engine

st.set_page_config(page_title="IoT Dashboard", page_icon="🌡️", layout="wide")


@st.cache_resource
def engine():
    return get_engine()


@st.cache_data(ttl=300)
def load_data(view_name: str) -> pd.DataFrame:
    return pd.read_sql(f"SELECT * FROM {view_name}", engine())


st.title("🌡️ Dashboard de Temperaturas IoT")
st.caption(
    "Dados do dataset Kaggle *Temperature Readings: IoT Devices* "
    "processados por Python e armazenados em PostgreSQL (Docker)."
)

# Carrega as views
df_resumo = load_data("vw_resumo_dispositivo")
df_anomalias = load_data("vw_anomalias")
df_tendencia = load_data("vw_tendencia")
df_hora = load_data("vw_leituras_por_hora")

total_leituras = int(df_resumo["total_leituras"].sum())
media_geral = (df_resumo["temp_media"] * df_resumo["total_leituras"]).sum() / total_leituras

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de leituras", f"{total_leituras:,}".replace(",", "."))
col2.metric("Temperatura média", f"{media_geral:.1f} °C")
col3.metric("Dias monitorados", len(df_tendencia))
col4.metric("Anomalias", f"{len(df_anomalias):,}".replace(",", "."))

st.header("Média de Temperatura por Dispositivo")
fig1 = px.bar(
    df_resumo,
    x="device_id",
    y="temp_media",
    color="device_id",
    text="temp_media",
    labels={"device_id": "Dispositivo (In = interno, Out = externo)", "temp_media": "Temp. média (°C)"},
)
st.plotly_chart(fig1, width="stretch")
st.dataframe(df_resumo, width="stretch", hide_index=True)

st.header("📈 Temperaturas Máximas e Mínimas por Dia")
fig2 = px.line(
    df_tendencia,
    x="data_leitura",
    y=["temp_max", "temp_media", "temp_min"],
    labels={"data_leitura": "Data", "value": "Temperatura (°C)", "variable": "Série"},
    markers=True,
)
st.plotly_chart(fig2, width="stretch")

st.header("⚠️ Anomalias Detectadas (fora de ±2 desvios-padrão)")
if df_anomalias.empty:
    st.info("Nenhuma anomalia detectada.")
else:
    fig3 = px.scatter(
        df_anomalias,
        x="noted_date",
        y="temp",
        color="ambiente",
        hover_data=["z_score", "media_ambiente"],
        labels={"noted_date": "Data/hora", "temp": "Temperatura (°C)"},
    )
    st.plotly_chart(fig3, width="stretch")

st.header("🕒 Leituras por Hora do Dia")
fig4 = px.line(
    df_hora,
    x="hora",
    y="contagem",
    color="ambiente",
    markers=True,
    labels={"hora": "Hora do dia", "contagem": "Quantidade de leituras"},
)
st.plotly_chart(fig4, width="stretch")
