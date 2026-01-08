# main.py

from agente import agente_generador

params = {
    "estilo": "MIX",
    "mezcla": "50% Bé, 50% Gulag",
    "tema": "la fragilidad de la memoria en la era digital",
    "tono_extra": "melancólico pero con toques de humor",
    "restricciones": "haiku (japonés tradicional: 3 versos de 5, 7 y 5 sílabas)",
    "extension": 3
}

poema = agente_generador(params)
print("\n=== POEMA GENERADO ===\n")
print(poema)