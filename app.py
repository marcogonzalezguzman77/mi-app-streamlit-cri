# app.py
import streamlit as st
import pandas as pd
import pickle

# --- CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Predicción de Diagnóstico Médico", layout="centered", page_icon="🧠")

# --- CARGAR MODELO Y FEATURES
modelo = pickle.load(open("modelo_grupo.pkl", "rb"))
features = pickle.load(open("features_grupo.pkl", "rb"))

# --- TÍTULO
st.title("🧠 Predicción de Diagnóstico Médico")
st.subheader("Ingresa los datos del paciente")

# --- FORMULARIO DE ENTRADA
edad = st.slider("Edad del paciente", 0, 100, 10)
genero = st.radio("Género", ["Femenino", "Masculino"])
pais = st.selectbox("Entidad (estado)", ["México", "CDMX", "Jalisco", "Otro"])
riesgo = st.radio("¿Tiene factores de riesgo?", ["Sí", "No"])
area = st.selectbox("Área afectada", ["Ortopedia", "Neurología", "Lenguaje", "Otro"])
parte = st.selectbox("Parte afectada", ["Extremidades", "Neurológico", "Auditivo", "Otro"])

# --- CODIFICAR VALORES COMO NÚMEROS
sexo_cod = 1 if genero == "Masculino" else 0
riesgo_cod = 1 if riesgo == "Sí" else 0
entidad_cod = hash(pais) % 100
area_cod = hash(area) % 100
parte_cod = hash(parte) % 100
topico = 0  # puedes usar un modelo de tópicos luego si deseas

# --- CONSTRUIR INPUT PARA EL MODELO
entrada = pd.DataFrame([{
    "edad": edad,
    "sexo_cod": sexo_cod,
    "cEntidad": entidad_cod,
    "cdscareaafectada": area_cod,
    "cdscparteafectada": parte_cod,
    "topico_cpadecimiento": topico
}])

entrada = entrada[features]  # asegurar el orden

# --- BOTÓN PARA HACER PREDICCIÓN
if st.button("Predecir diagnóstico"):
    resultado = modelo.predict(entrada)[0]
    grupos = ["conducta_lenguaje", "neurologico", "ortopedico_sensorial", "otro"]
    st.success(f"🔮 El grupo diagnóstico estimado es: **{grupos[resultado]}**")
