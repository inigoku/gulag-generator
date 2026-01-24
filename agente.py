# agente.py

import json
import requests
import itertools

from prompts import PROMPT_MAESTRO, CRITICO, REESCRITURA, ACABADO
from config import (
    GROQ_API_KEY, GROQ_MODEL, REWORK_RETRIES,
    GOOGLE_MODEL, GOOGLE_API_KEY
)

import unicodedata

def limpiar_prompt(texto):
    # Normaliza unicode (NFC) pero mantiene caracteres latinos como tildes y ñ
    texto = unicodedata.normalize("NFC", texto)
    return texto.strip()

# Configuración para Google AI Studio (Capa gratuita sin Vertex)
if GOOGLE_API_KEY:
    from google import genai
    client = genai.Client(api_key=GOOGLE_API_KEY)

def llamar_groq(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }

    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "Eres un asistente experto en poesía generativa."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.9,
        "max_tokens": 1600
    }

    print("=== DEBUG (GROQ) ===")
    print("MODEL:", GROQ_MODEL)
    print("API KEY:", "OK" if GROQ_API_KEY else "MISSING")
    print("PAYLOAD:", payload)


    import time
    max_retries = 5
    for intento in range(max_retries):
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 429:
            print("Rate limit alcanzado. Esperando 10 segundos antes de reintentar...")
            time.sleep(10)
            continue
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    raise Exception("Demasiados intentos fallidos por rate limit (429)")

def llamar_google(prompt):
    if GOOGLE_API_KEY:
        print("=== DEBUG (GOOGLE AI STUDIO) ===")
        
        print("MODEL:", GOOGLE_MODEL)
        try:
            response = client.models.generate_content(
                model=GOOGLE_MODEL,
                contents=prompt
            )
            return response.text
        except Exception as e:
            raise Exception(f"Error llamando a Google AI Studio: {e}")
    raise Exception("Google API Key no configurada")

_provider_cycle = {
    "creator": "google",
    "critic": "groq",
    "rework": "groq",
    "polish": "google"
}

def llamar_modelo(prompt, role):
    prompt = limpiar_prompt(prompt)
    provider = _provider_cycle[role]
    
    if provider == "google" and not GOOGLE_API_KEY:
        provider = "groq"
        
    print("=== DEBUG (SYSTEM) ===")
    print("PROVIDER", provider)

    if provider == "google":
        try:
            return llamar_google(prompt)
        except Exception as e:
            print(f"⚠️ Error en Google AI (fallback a Groq): {e}")
            return llamar_groq(prompt)
    else:
        return llamar_groq(prompt)

def construir_prompt_maestro(params):
    return PROMPT_MAESTRO.format(
        estilo=params.get("estilo", ""),
        mezcla=params.get("mezcla", ""),
        tema=params.get("tema", ""),
        tono_extra=params.get("tono_extra", ""),
        restricciones=params.get("restricciones", ""),
        extension=params.get("extension", 14),
    )

def genera_poema_master(params):
    prompt = construir_prompt_maestro(params)
    poema = llamar_modelo(prompt, "creator")
    return poema

def evaluar_poema(poema, params):
    prompt = CRITICO + f"\n\nPoema:\n{poema}\n\nEstilo: {params['estilo']}\nTema: {params['tema']}"
    evaluacion_raw = llamar_modelo(prompt, "critic")
    import re
    try:
        # Extrae el primer bloque JSON de la respuesta
        # Busca desde la primera llave hasta la última para soportar anidación
        start = evaluacion_raw.find('{')
        end = evaluacion_raw.rfind('}') + 1
        if start != -1 and end != 0:
            return json.loads(evaluacion_raw[start:end])
        else:
            raise ValueError("No se encontró bloque JSON en la respuesta")
    except Exception as e:
        print("ERROR: la respuesta no es JSON válido\n", evaluacion_raw)
        return {"ok": False, "problemas": ["Respuesta no es JSON válido"], "sugerencias": [str(e)]}


def corregir_poema(poema, evaluacion):
    prompt = REESCRITURA.format(
        poema=poema,
        problemas=", ".join(evaluacion["problemas"]),
        sugerencias=", ".join(evaluacion["sugerencias"])
    )
    return llamar_modelo(prompt, "rework")

def acabar_poema(poema, params):
    prompt = ACABADO + f"\n\nPoema:\n{poema}\n\nEstilo: {params['estilo']}\nTema: {params['tema']}\n\nRestricciones: {params['restricciones']}"
    return llamar_modelo(prompt, "polish")

def agente_generador(params):
    poema = genera_poema_master(params)

    evaluacion = evaluar_poema(poema, params)

    intentos = 0
    while not evaluacion["ok"] and intentos < REWORK_RETRIES:
        poema = corregir_poema(poema, evaluacion)
        evaluacion = evaluar_poema(poema, params)
        intentos += 1

    poema = acabar_poema(poema, params)

    return poema