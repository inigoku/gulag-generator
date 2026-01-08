# agente.py

import json
import requests
from prompts import PROMPT_MAESTRO, CRITICO, REESCRITURA
from config import GROQ_API_KEY, GROQ_MODEL

import unicodedata

def limpiar_prompt(texto):
    # Normaliza a ASCII eliminando caracteres no compatibles
    texto = unicodedata.normalize("NFKD", texto)
    texto = texto.encode("ascii", "ignore").decode("ascii")
    return texto

def llamar_modelo(prompt):
    from config import GROQ_MODEL, GROQ_API_KEY

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }

    prompt = limpiar_prompt(prompt)
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "Eres un asistente experto en poesía generativa."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.9,
        "max_tokens": 1600
    }

    print("=== DEBUG ===")
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


def construir_prompt_maestro(params):
    return PROMPT_MAESTRO.format(
        estilo=params.get("estilo", ""),
        mezcla=params.get("mezcla", ""),
        tema=params.get("tema", ""),
        tono_extra=params.get("tono_extra", ""),
        restricciones=params.get("restricciones", ""),
        extension=params.get("extension", 14),
    )


def evaluar_poema(poema, params):
    prompt = CRITICO + f"\n\nPoema:\n{poema}\n\nEstilo: {params['estilo']}\nTema: {params['tema']}"
    evaluacion_raw = llamar_modelo(prompt)
    import re
    try:
        # Extrae el primer bloque JSON de la respuesta
        match = re.search(r"\{[\s\S]*?\}", evaluacion_raw)
        if match:
            return json.loads(match.group(0))
        else:
            raise ValueError("No se encontró bloque JSON en la respuesta")
    except Exception as e:
        print("ERROR: la respuesta no es JSON válido\n", evaluacion_raw)
        return {"ok": False, "problemas": ["Respuesta no es JSON válido"], "sugerencias": [str(e)]}


def corregir_poema(poema, evaluacion):
    prompt = REESCRITURA.format(
        poema=poema,
        problemas=", ".join(evaluacion["problemas"])
    )
    return llamar_modelo(prompt)


def agente_generador(params):
    prompt = construir_prompt_maestro(params)
    poema = llamar_modelo(prompt)

    evaluacion = evaluar_poema(poema, params)

    intentos = 0
    while not evaluacion["ok"] and intentos < 3:
        poema = corregir_poema(poema, evaluacion)
        evaluacion = evaluar_poema(poema, params)
        intentos += 1

    return poema