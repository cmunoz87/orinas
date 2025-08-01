import streamlit as st
from fpdf import FPDF

# =========================
# DICCIONARIO DE PARÁMETROS COMPLETO
# =========================
parametros = {
    "Color": {
        "resultados": ["Amarillo claro", "Ámbar", "Anaranjado", "Amarillo-verdoso", "Amarillo-marrón", "Azul-verde", "Rosa", "Rojo", "Marrón", "Negro"],
        "metodo": "Revisión visual"
    },
    "Aspecto (Turbidez)": {
        "resultados": ["Transparente", "Límpida", "Levemente turbia", "Turbia", "Lechosa"],
        "metodo": "Revisión visual"
    },
    "Eritrocitos (RBC)": {
        "resultados": ["0-3/campo", "3-5", "5-10", "10-25", "25-50", "50-100", ">100"],
        "metodo": "Citometría de flujo"
    },
    "Eritrocitos (RBC) morfología": {
        "resultados": ["Isomórficos", "Dismórficos"],
        "metodo": "Citometría de flujo"
    },
    "Eritrocitos Dismórficos": {
        "resultados": ["5%", "10%", "15%", "20%", "50%"],
        "metodo": "Citometría de flujo"
    },
    "Leucocitos (WBC)": {
        "resultados": ["0-5/campo", "5-10", "10-25", "25-50", "50-100", ">100"],
        "metodo": "Citometría de flujo"
    },
    "Piocitos": {
        "resultados": ["No se observan", "Muy escasas", "Escasas", "Regulares", "Abundantes"],
        "metodo": "Microscopía"
    },
    "Placas de pus": {
        "resultados": ["No se observan", "Muy escasas", "Escasas", "Regulares", "Abundantes"],
        "metodo": "Microscopía"
    },
    "Células epiteliales": {
        "resultados": ["No se observan", "Muy escasas", "Escasas", "Regulares", "Abundantes"],
        "metodo": "Microscopía"
    },
    "Mucus": {
        "resultados": ["No se observa", "Muy escaso", "Escaso", "Regular", "Abundante"],
        "metodo": "Microscopía"
    },
    "Bacterias": {
        "resultados": ["No se observan", "Muy escasas", "Escasas", "Regulares", "Abundantes"],
        "metodo": "Microscopía"
    },
    "Levaduras": {
        "resultados": ["No se observan", "Escasas", "Regulares", "Abundantes"],
        "metodo": "Microscopía"
    },
    "Cristales": {
        "resultados": ["No se observan", "Oxalato de calcio", "Ácido úrico", "Fosfato triple", "Otros"],
        "metodo": "Microscopía"
    },
    "Cilindros": {
        "resultados": ["No se observan", "Hialinos", "Granulosos", "Otros"],
        "metodo": "Microscopía"
    },
    "Filamento de moco": {
        "resultados": ["No se observan", "Muy escasos", "Escasos", "Regulares", "Abundantes"],
        "metodo": "Microscopía"
    },
    "Cilindros hialinos": {
        "resultados": ["No se observan", "Escasos", "Regulares", "Abundantes"],
        "metodo": "Microscopía"
    },
    "Cilindros granulosos": {
        "resultados": ["No se observan", "Escasos", "Regulares", "Abundantes"],
        "metodo": "Microscopía"
    },
    "Cilindros céreos": {
        "resultados": ["No se observan", "Escasos", "Regulares", "Abundantes"],
        "metodo": "Microscopía"
    },
    "Cilindros eritrocitarios": {
        "resultados": ["No se observan", "Escasos", "Regulares", "Abundantes"],
        "metodo": "Microscopía"
    },
    "Cilindros leucocitarios": {
        "resultados": ["No se observan", "Escasos", "Regulares", "Abundantes"],
        "metodo": "Microscopía"
    },
    "Cilindros grasos": {
        "resultados": ["No se observan", "Escasos", "Regulares", "Abundantes"],
        "metodo": "Microscopía"
    }
}

# =========================
# CONFIGURACIÓN DE LA APP
# =========================
st.set_page_config(page_title="Informe de Orina", page_icon="🧪", layout="centered")
st.title("🧾 Generador de Informe de Orina")

# Inicializar almacenamiento de resultados
if "resultados" not in st.session_state:
    st.session_state.resultados = {}

# =========================
# FORMULARIO DE SELECCIÓN
# =========================
st.subheader("Seleccione los resultados para cada parámetro:")

for parametro, datos in parametros.items():
    seleccion = st.selectbox(
        f"{parametro} ({datos['metodo']})",
        options=["Seleccione..."] + datos["resultados"],
        key=parametro
    )
    if seleccion != "Seleccione...":
        st.session_state.resultados[parametro] = seleccion

# =========================
# GENERAR PDF
# =========================
if st.button("📄 Generar PDF"):
    if not st.session_state.resultados:
        st.warning("Debe seleccionar al menos un resultado antes de generar el PDF.")
    else:
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="Informe de Orina", ln=True, align="C")
        pdf.ln(10)

        for parametro, resultado in st.session_state.resultados.items():
            metodo = parametros[parametro]["metodo"]
            pdf.multi_cell(0, 10, txt=f"{parametro}: {resultado}  (Método: {metodo})")

        pdf_output = "informe_orina.pdf"
        pdf.output(pdf_output)

        with open(pdf_output, "rb") as f:
            st.download_button(
                label="⬇️ Descargar PDF",
                data=f,
                file_name="informe_orina.pdf",
                mime="application/pdf"
            )

        st.success("PDF generado exitosamente.")
