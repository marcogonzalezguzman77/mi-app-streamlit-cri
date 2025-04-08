import streamlit as st
import pandas as pd
import pickle

# --------------------
# CONFIGURACIÓN INICIAL
# --------------------

st.set_page_config(page_title="Predicción Diagnóstico Médico", layout="centered")
st.title("🧠 Sistema de Predicción de Diagnóstico Médico")
st.subheader("Ingresa los datos del paciente")

# --------------------
# CARGAR MODELOS Y VARIABLES
# --------------------

modelo_grupo = pickle.load(open("modelo_grupo.pkl", "rb"))
features_grupo = pickle.load(open("features_grupo.pkl", "rb"))

# Submodelo para grupo NEUROLÓGICO
try:
    modelo_neuro = pickle.load(open("modelo_neuro.pkl", "rb"))
    features_neuro = pickle.load(open("features_neuro.pkl", "rb"))
    subgrupos_neuro = pickle.load(open("labels_neuro.pkl", "rb"))
except:
    modelo_neuro = None
    features_neuro = []
    subgrupos_neuro = []

# --------------------
# ENTRADA DEL USUARIO
# --------------------

edad = st.slider("Edad del paciente", 0, 100, 10)
sexo = st.radio("Sexo", ["Femenino", "Masculino"])
entidad = st.selectbox("Entidad", ["CDMX", "México", "Jalisco", "Otro"])
area = st.selectbox("Área Afectada", ["Neurología", "Ortopedia", "Lenguaje", "Otro"])
parte = st.selectbox("Parte Afectada", ["Neurológico", "Extremidades", "Auditivo", "Otro"])

# Codificación básica
sexo_cod = 1 if sexo == "Masculino" else 0
entidad_cod = hash(entidad) % 100
area_cod = hash(area) % 100
parte_cod = hash(parte) % 100
topico = 0  # simplificado

# --------------------
# PREDICCIÓN DEL GRUPO
# --------------------

entrada_grupo = pd.DataFrame([{
    "edad": edad,
    "sexo_cod": sexo_cod,
    "cEntidad": entidad_cod,
    "cdscareaafectada": area_cod,
    "cdscparteafectada": parte_cod,
    "topico_cpadecimiento": topico
}])

entrada_grupo = entrada_grupo[features_grupo]

if st.button("🔮 Predecir grupo diagnóstico"):
    pred = modelo_grupo.predict(entrada_grupo)[0]
    grupos = ["conducta_lenguaje", "neurologico", "ortopedico_sensorial"]
    grupo_nombre = grupos[pred]
    st.success(f"El grupo diagnóstico estimado es: **{grupo_nombre.upper()}**")

    # -----------------------------
    # PREDICCIÓN DE SUBDIAGNÓSTICO
    # -----------------------------
    if grupo_nombre == "neurologico" and modelo_neuro:
        entrada_neuro = entrada_grupo[features_neuro]
        pred_sub = modelo_neuro.predict(entrada_neuro)[0]
        st.info(f"🧬 Subdiagnóstico estimado: **{subgrupos_neuro[pred_sub]}**")
