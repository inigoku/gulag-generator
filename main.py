# main.py

from agente import agente_generador

params = {
    "estilo": "MIX",
    "mezcla": "50% Bé, 50% Gulag",
    "tema": "la vida en general",
    "tono_extra": "optimista",
    "restricciones": "lírico",
    "extension": 14
}

poema = agente_generador(params)
print("\n=== POEMA GENERADO ===\n")
print(poema)