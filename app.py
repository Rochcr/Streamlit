import streamlit as st
import requests

st.set_page_config(
    page_title="WebApp Gemini + Streamlit",
    layout="centered"
)

# --- CSS personalizado ---
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: white;
}
.block-container {
    padding-top: 2rem;
}
input, textarea {
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)


st.title("✨ WebApp con Gemini y Streamlit")
st.write("Escribe un prompt y envía una petición HTTP al modelo Gemini.")

# --- Input prompt ---
prompt = st.text_area("Tu prompt aquí:", height=150)

# Sliders (widgets extra)
temperature = st.slider("Creatividad (temperature)", 0.0, 1.5, 0.9)
max_tokens = st.slider("Máximo de tokens", 64, 1024, 256, step=64)

# --- Función para llamar a Gemini ---
def call_gemini(prompt):
    API_KEY = st.secrets["GEMINI_API_KEY"]

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

    headers = {"Content-Type": "application/json"}

    data = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": temperature,
            "maxOutputTokens": max_tokens
        }
    }

    response = requests.post(url + f"?key={API_KEY}", json=data, headers=headers)
    result = response.json()

    try:
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return " Error en la respuesta del modelo."


# --- Botón ---
if st.button("Enviar prompt"):
    if prompt.strip() == "":
        st.warning("Escribe un prompt primero.")
    else:
        st.subheader("Respuesta del modelo:")
        respuesta = call_gemini(prompt)
        st.write(respuesta)
