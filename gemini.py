from google import genai
from google.genai import types
import streamlit as st


def get_gemini_client():
    api_key = st.secrets["GOOGLE_API_KEY"]
    client = genai.Client(api_key=api_key)
    return client


def generar_respuesta(
    prompt: str,
    model: str = "gemini-2.0-flash",
    temperature: float = 0.9,
    max_output_tokens: int = 512,
    system_instruction: str | None = None,
) -> str:


    client = get_gemini_client()

    # Configuración del modelo
    config = types.GenerateContentConfig(
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        system_instruction=system_instruction,
    )

    # Llamada a la API
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=config
    )

    # Extraer el texto de la respuesta
    try:
        first_part = response.candidates[0].content.parts[0]
        if hasattr(first_part, "text"):
            return first_part.text
        else:
            return "El modelo no devolvió texto en su respuesta."
    except Exception as e:
        return f"Error extrayendo texto: {e}"
