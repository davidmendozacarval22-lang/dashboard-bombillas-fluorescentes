
import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px

st.set_page_config(page_title="Dashboard Encuestas", layout="wide")

DATA_FILE = Path("data/encuesta.xlsx")
ADMIN_PASSWORD = "cambia_esta_clave"

st.title("💡 Dashboard de Encuestas")

with st.sidebar:
    st.header("Administración")
    pwd = st.text_input("Contraseña", type="password")
    nuevo = st.file_uploader("Cargar nuevo Excel", type=["xlsx"])

    if st.button("Reemplazar archivo"):
        if pwd == ADMIN_PASSWORD and nuevo is not None:
            DATA_FILE.parent.mkdir(exist_ok=True)
            DATA_FILE.write_bytes(nuevo.getvalue())
            st.success("Archivo reemplazado correctamente.")
        else:
            st.error("Contraseña incorrecta o archivo no seleccionado.")

if not DATA_FILE.exists():
    st.warning("No existe archivo de datos. Cargue uno desde el panel de administración.")
    st.stop()

df = pd.read_excel(DATA_FILE)

preguntas = [c for c in df.columns if c != "Marca temporal"]

c1,c2 = st.columns(2)
c1.metric("Total encuestas", len(df))
c2.metric("Preguntas", len(preguntas))

pregunta = st.radio("Seleccione una pregunta", preguntas, horizontal=True)

conteo = df[pregunta].fillna("Sin respuesta").value_counts().reset_index()
conteo.columns = ["Respuesta","Cantidad"]
conteo["Porcentaje"] = round(conteo["Cantidad"]*100/conteo["Cantidad"].sum(),2)

col1,col2 = st.columns([2,1])

with col1:
    fig = px.bar(conteo, x="Cantidad", y="Respuesta", orientation="h",
                 text="Porcentaje", color="Cantidad")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig2 = px.pie(conteo, names="Respuesta", values="Cantidad", hole=0.6)
    st.plotly_chart(fig2, use_container_width=True)

st.dataframe(conteo, use_container_width=True)
