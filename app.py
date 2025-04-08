import streamlit as st
import pandas as pd
import pickle

# --- Cargar modelo y columnas
modelo = pickle.load(open("modelo_grupo.pkl", "rb"))
features = pickle.load(open("features_grupo.pkl", "rb"))

st.set_page_config(page_title="Predicción de Diagnóstico Médico", layout="centered")
st.title("🧠 Diagnóstico Médico Automatizado")
st.subheader("Ingresa los datos del paciente:")

# --- Entradas del usuario
edad = st.slider("Edad", 0, 100, 10)
sexo = st.radio("Sexo", ["Femenino", "Masculino"])
entidad = st.selectbox("Entidad", ["CDMX", "México", "Jalisco", "Otro"])
area = st.selectbox("Área Afectada", ["Neurología", "Ortopedia", "Lenguaje", "Otro"])
parte = st.selectbox("Parte Afectada", ["Neurológico", "Extremidades", "Auditivo", "Otro"])

# Codificación (simulada)
sexo_cod = 1 if sexo == "Masculino" else 0
entidad_cod = hash(entidad) % 100
area_cod = hash(area) % 100
parte_cod = hash(parte) % 100
topico = 0  # puedes integrar LDA luego

# Construcción del input
entrada = pd.DataFrame([{
    "edad": edad,
    "sexo_cod": sexo_cod,
    "cEntidad": entidad_cod,
    "cdscareaafectada": area_cod,
    "cdscparteafectada": parte_cod,
    "topico_cpadecimiento": topico
}])
entrada = entrada[features]

# Predicción
if st.button("Predecir grupo diagnóstico"):
    resultado = modelo.predict(entrada)[0]
    etiquetas = ["conducta_lenguaje", "neurologico", "ortopedico_sensorial"]
    st.success(f"🔮 Grupo diagnóstico estimado: **{etiquetas[resultado]}**")
