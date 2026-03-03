import streamlit as st
import pandas as pd

# 1. Configuración de la pestaña
st.set_page_config(page_title="PCAR - Stock", layout="wide", page_icon="🚗")

# --- ESTILO CSS PARA PESTAÑAS 50/50 Y CENTRADAS ---
st.markdown("""
    <style>
    /* Estira las pestañas para que ocupen el 50% cada una */
    div[data-baseweb="tab-list"] {
        width: 100% !important;
        display: flex !important;
        justify-content: center !important;
        gap: 0px !important;
    }
    button[data-baseweb="tab"] {
        width: 50% !important;
        flex-grow: 1 !important;
        text-align: center !important;
        height: 50px !important;
    }
    /* Tamaño de letra y estilo del texto en pestañas */
    div[data-testid="stMarkdownContainer"] p {
        font-size: 18px !important;
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)

# 2. LOGO DE LA AGENCIA
URL_DE_TU_LOGO = 'https://i.postimg.cc/Cx1wcv1f/PCARA-Mesa-de-trabajo-1.png' 

st.markdown(f"""
    <div style='text-align: center;'>
        <img src='{URL_DE_TU_LOGO}' width='400' style='margin-bottom: 20px;'>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# 3. UBICACIÓN
st.markdown(f"""
    <div style='text-align: center; margin-top: -10px; margin-bottom: 25px;'>
        <a href='https://maps.google.com/?cid=1158533433268707757&g_mp=CiVnb29nbGUubWFwcy5wbGFjZXMudjEuUGxhY2VzLkdldFBsYWNl' target='_blank' style='text-decoration: none;'>
            <div style='display: inline-block; background-color: #f0f2f6; padding: 10px 20px; border-radius: 10px; border: 1px solid #004080;'>
                <span style='color: #004080; font-weight: bold; font-size: 16px;'>📍 PCAR AUTOS</span><br>
                <span style='color: #555; font-size: 14px;'>VISITANOS!!</span>
            </div>
        </a>
    </div>
""", unsafe_allow_html=True)

# 4. Conexión con Google Sheets
SHEET_ID = '1TnIRP4doFAJk5u2lB6qGwqNJHPY4LNXWdx8KQaHWrSc'
url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv'

try:
    df = pd.read_csv(url)

    # Filtro de Estado: Solo "Disponible"
    if 'Estado' in df.columns:
        df_mostrar = df[df['Estado'] == 'Disponible']
    else:
        df_mostrar = df

    # 5. Buscador
    st.markdown(f"<h2 style='color: #004080; margin-bottom: -10px;'>STOCK DISPONIBLE</h2>", unsafe_allow_html=True)
    busqueda = st.text_input("", placeholder="🔍 Escribí Marca o Modelo...").strip().lower()

    # --- FUNCIÓN PARA RENDERIZAR GRILLA ---
    def mostrar_unidades(datos):
        if not datos.empty:
            # Filtro de buscador dentro de la categoría
            if busqueda:
                mask = (datos['Marca'].astype(str).str.lower().str.contains(busqueda, na=False) | 
                        datos['Modelo'].astype(str).str.lower().str.contains(busqueda, na=False))
                datos = datos[mask]

            if datos.empty:
                st.info("No hay unidades que coincidan con la búsqueda.")
                return

            cols = st.columns(3)
            for i, (index, row) in enumerate(datos.iterrows()):
                with cols[i % 3]:
                    st.image(row['Foto_URL'], use_container_width=True)
                    
                    # Galería
                    fotos_extra = [row[c] for c in row.index if c.startswith('Foto') and c != 'Foto_URL' and pd.notna(row[c]) and str(row[c]).strip() != ""]
                    if fotos_extra:
                        with st.expander("📸 Ver más fotos"):
                            for f in fotos_extra:
                                st.image(f, use_container_width=True)
                    
                    st.subheader(f"{row['Marca']} {row['Modelo']}")
                    km_texto = str(row['KM']).replace('.0', '')
                    st.write(f"Año: {row['Año']} | KM: {km_texto}")
                    
                    if 'Motor' in row and pd.notna(row['Motor']) and str(row['Motor']).strip() != "":
                        st.write(str(row['Motor']))
                    
                    precio_mostrar = str(row['Precio']) if pd.notna(row['Precio']) else "Consultar"
                    st.markdown(f"<h3 style='color: #004080;'>{precio_mostrar}</h3>", unsafe_allow_html=True)
                    st.markdown("---")
        else:
            st.info("No hay unidades en esta categoría.")

    # --- PESTAÑAS 50/50 SIN ICONOS ---
    tab_autos, tab_motos = st.tabs(["AUTOS", "MOTOS"])

    with tab_autos:
        # Filtra la columna 1 (Categoría) buscando "Auto"
        df_autos = df_mostrar[df_mostrar.iloc[:, 0].astype(str).str.contains("Auto", case=False, na=False)]
        mostrar_unidades(df_autos)

    with tab_motos:
        # Filtra la columna 1 (Categoría) buscando "Moto"
        df_motos = df_mostrar[df_mostrar.iloc[:, 0].astype(str).str.contains("Moto", case=False, na=False)]
        mostrar_unidades(df_motos)

except Exception as e:
    st.error(f"Error: {e}")










