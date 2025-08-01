import streamlit as st
import pandas as pd
from fpdf import FPDF

# --- Función para generar PDF ---
def generar_pdf(selecciones):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Resultados de Parámetros de Orina - Sedimento", ln=True, align="C")
    pdf.ln(10)

    # Encabezado de tabla
    pdf.set_font("Arial", size=11)
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(80, 10, "Parámetro", 1, 0, "C", True)
    pdf.cell(60, 10, "Resultado", 1, 0, "C", True)
    pdf.cell(50, 10, "Método", 1, 1, "C", True)

    # Filas de la tabla
    for parametro, datos in selecciones.items():
        pdf.set_fill_color(255, 255, 255)
        pdf.multi_cell(80, 10, parametro, 1)
        pdf.set_xy(pdf.get_x() + 80, pdf.get_y() - 10)
        pdf.cell(60, 10, datos['resultado'], 1)
        pdf.cell(50, 10, datos['método'], 1)
        pdf.ln()

    pdf_output = "resultados_parametros.pdf"
    pdf.output(pdf_output)
    return pdf_output

# --- Interfaz Streamlit ---
st.title("Parámetros de Orina - Sedimento")

uploaded_file = st.file_uploader("Suba el archivo Excel con los parámetros", type=["xlsx"])

if uploaded_file:
    glosa_df = pd.read_excel(uploaded_file, sheet_name='glosa')

    st.subheader("Selección de resultados por parámetro")
    resultados_seleccionados = {}

    for _, row in glosa_df.iterrows():
        parametro = row["Parámetro"]
        resultados = [r.strip() for r in str(row["Resultados posibles"]).split(",")]
        metodo = row["Método"]

        with st.expander(f"⚙️ {parametro}"):
            resultado = st.selectbox(f"Seleccione resultado para {parametro}:", resultados, key=parametro)
            st.write(f"**Método:** {metodo}")
            resultados_seleccionados[parametro] = {
                "resultado": resultado,
                "método": metodo
            }

    # Botón para generar PDF
    if st.button("📄 Generar PDF"):
        pdf_path = generar_pdf(resultados_seleccionados)
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="⬇️ Descargar PDF",
                data=f,
                file_name="resultados_parametros.pdf",
                mime="application/pdf"
            )

else:
    st.info("Por favor, suba el archivo Excel para continuar.")
