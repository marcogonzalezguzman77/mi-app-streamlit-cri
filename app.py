# app.py

import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Predicción Médica", layout="centered")
st.title("🩺 Predicción de Diagnóstico Médico")

# Cargar el modelo guardado
modelo = joblib.load("modelo.pkl")

# Interfaz de usuario
st.subheader("Ingresa los datos del paciente")

col1, col2 = st.columns(2)

with col1:
    edad = st.slider("Edad", 0, 100, 30)
    genero = st.selectbox("Género", ["Masculino", "Femenino"])
    
with col2:
    pais = st.selectbox("País", ["México", "Colombia", "Argentina"])
    riesgo = st.radio("¿Tiene factores de riesgo?", ["Sí", "No"])

# Botón para predecir
if st.button("Predecir diagnóstico"):
    entrada = pd.DataFrame({
        "edad": [edad],
        "genero": [genero],
        "pais": [pais],
        "riesgo": [riesgo]
    })

    prediccion = modelo.predict(entrada)

    st.success(f"✅ Diagnóstico predicho: {prediccion[0]}")
