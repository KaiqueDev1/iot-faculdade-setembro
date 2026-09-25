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