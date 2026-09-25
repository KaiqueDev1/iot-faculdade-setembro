import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

st.set_page_config(page_title="Iot Dashboard", layout="wide")
st.title("painel do dashboard IOT")

engine = create_engine("postgresql://postgres:admin@localhost:5432/iot_db")

df_resumo = pd.read_sql("SELECT * FROM vw_resumo_dispositivo", engine)

st.dataframe(df_resumo)

fig = px.bar(df_resumo, x="device_id", y="temp_media", title="Temperatura Média por Dispositivo")
st.plotly_chart(fig)

df_anomalias = pd.read_sql("SELECT * FROM vw_anomalias", engine)
df_tendencia = pd.read_sql("SELECT * FROM vw_tendencia", engine)

st.subheader("⚠️ Anomalias Detetadas (Temperaturas >= 40°C)")
if not df_anomalias.empty:
    fig2 = px.scatter(df_anomalias, x="noted_date", y="temp", color="ambiente", title="Dispersão de Anomalias")
    st.plotly_chart(fig2)
else:
    st.write("Nenhuma anomalia detectada.")

st.subheader("📈 Tendência Diária (Máximas e Mínimas)")
fig3 = px.line(df_tendencia, x="data_leitura", y=["temp_max", "temp_min"], title="Temperaturas Máx e Mín por Dia")
st.plotly_chart(fig3)