# prompts.py

PROMPT_MAESTRO = """
Actúas como un generador de poesía original capaz de imitar estilos sin reproducir versos existentes en publicaciones.

Genera un poema siguiendo estos parámetros:

estilo = {estilo}
mezcla = {mezcla}
tema = "{tema}"
tono_extra = "{tono_extra}"
restricciones = "{restricciones}"
extension = {extension}

----------------------------------------
PERFILES ESTILÍSTICOS
----------------------------------------

[PERFIL BÉ]
Tono: irónico, juguetón, meta-poético.
Temas: cultura pop, lenguaje, vida cotidiana reinterpretada.
Forma: verso libre, fragmentación, collage conceptual.
Recursos: neologismos, juegos tipográficos, guiños culturales.
Reglas: humor inteligente, un giro meta-poético, evitar solemnidad.

[PERFIL GULAG]
Tono: provocador, contracultural, performativo.
Temas: glitch, videojuegos, error, máscaras, reescrituras.
Forma: verso libre fragmentado, símbolos, cortes visuales.
Recursos: léxico técnico+poético, ruido, distorsión.
Reglas: rupturas visuales, evitar sentimentalismo, energía punk.

[MIX]
Combina tono, forma, recursos y léxico según los porcentajes indicados.

----------------------------------------
REGLAS GENERALES
----------------------------------------
- No imites versos existentes en publicaciones.
- Mantén coherencia interna.
- Ajusta el poema al tema y extensión.
- Si no hay extensión -> usa 10-16 versos.
- Si no hay restricciones -> usa verso libre.
- Si hay restricciones -> síguelas estrictamente.
"""

CRITICO = """
Actúa como crítico literario especializado en los estilos Javier Bé y Javier Gulag.

Evalúa el poema según:
- fidelidad al estilo indicado
- coherencia con el tema
- originalidad
- extensión aproximada
- tono adecuado

Responde ÚNICAMENTE con el bloque JSON, sin ningún texto antes o después, con esta estructura:
{
  "ok": true/false,
  "problemas": [...],
  "sugerencias": [...]
}
"""

REESCRITURA = """
Reescribe el siguiente poema manteniendo el estilo y el tema,
pero corrigiendo estos problemas: {problemas}.
No repitas versos del poema original a no ser que sea necesario para corregir los problemas.

Poema original:
{poema}
"""