import streamlit as st
from agente import agente_generador

def main():
    st.set_page_config(page_title="Generador de Poesía", page_icon="✒️", layout="centered")

    st.title("Generador de Poesía: NOLDO")
    st.markdown("Configura los parámetros y genera poemas con los estilos **Bé**, **Gulag** o una **Mezcla**.")

    # --- Configuración de Parámetros ---
    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            estilo = st.selectbox("Estilo", ["BÉ", "GULAG", "MIX"], index=0)
            
            mezcla = ""
            if estilo == "MIX":
                mezcla = st.text_input("Porcentajes de Mezcla", value="50% Bé, 50% Gulag")
            
            extension = st.number_input("Extensión (versos)", min_value=4, max_value=100, value=14, step=1)

        with col2:
            tema = st.text_input("Tema", value="el futuro digital")
            tono_extra = st.text_input("Tono Extra", placeholder="Ej: melancólico, agresivo...")
        
        restricciones = st.text_area("Restricciones", placeholder="Ej: sin rima, usar palabras técnicas, verso corto...")

    # --- Botón de Generación ---
    st.markdown("---")
    if st.button("Generar Poema", type="primary", use_container_width=True):
        if not tema:
            st.warning("⚠️ Por favor, escribe un tema para el poema.")
        else:
            params = {
                "estilo": estilo,
                "mezcla": mezcla,
                "tema": tema,
                "tono_extra": tono_extra,
                "restricciones": restricciones,
                "extension": extension
            }

            # --- Proceso de Generación ---
            with st.spinner("🤖 El agente está escribiendo, criticando y reescribiendo..."):
                try:
                    poema = agente_generador(params)
                    
                    st.success("¡Poema generado con éxito!")
                    st.text_area("Resultado", value=poema, height=500)
                    
                except Exception as e:
                    st.error(f"❌ Ocurrió un error: {e}")

if __name__ == "__main__":
    main()