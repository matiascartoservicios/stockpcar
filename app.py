import streamlit as st
import pandas as pd

# 1. Configuración de la pestaña
st.set_page_config(page_title="PCAR - Stock", layout="wide", page_icon="🚗")

# 2. LOGO DE LA AGENCIA
URL_DE_TU_LOGO = 'https://i.postimg.cc/Cx1wcv1f/PCARA-Mesa-de-trabajo-1.png' 

st.markdown(f"""
    <div style='text-align: center;'>
        <img src='{URL_DE_TU_LOGO}' width='400' style='margin-bottom: 20px;'>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- UBICACIÓN ---
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

# 3. Conexión con Google Sheets
SHEET_ID = '1TnIRP4doFAJk5u2lB6qGwqNJHPY4LNXWdx8KQaHWrSc'
url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv'

try:
    df = pd.read_csv(url)

    # Filtro de Estado: Solo "Disponible"
    if 'Estado' in df.columns:
        df_mostrar = df[df['Estado'] == 'Disponible']
    else:
        df_mostrar = df

    # 4. Buscador
    st.markdown(f"<h2 style='color: #004080; margin-bottom: -10px;'>STOCK DISPONIBLE</h2>", unsafe_allow_html=True)
    busqueda = st.text_input("", placeholder="🔍 Escribí Marca o Modelo...").strip().lower()

    # --- NUEVA SECCIÓN DE PESTAÑAS ---
    tab_autos, tab_motos = st.tabs(["🚗 AUTOS", "🏍️ MOTOS"])

    # Definimos como mostrar cada unidad
    def renderizar_unidad(dataframe):
        if not dataframe.empty:
            # Filtro por buscador dentro de la pestaña
            if busqueda:
                mask = (dataframe['Marca'].astype(str).str.lower().str.contains(busqueda, na=False) | 
                        dataframe['Modelo'].astype(str).str.lower().str.contains(busqueda, na=False))
                dataframe = dataframe[mask]

            if dataframe.empty:
                st.info("No hay unidades que coincidan con la búsqueda.")
                return

            cols = st.columns(3)
            for i, (index, row) in enumerate(dataframe.iterrows()):
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
            st.info("No hay unidades cargadas en esta categoría.")

    # --- APLICAMOS LAS PESTAÑAS ---
    with tab_autos:
        # Filtramos por la primera columna (0) que contenga "Auto"
        df_autos = df_mostrar[df_mostrar.iloc[:, 0].astype(str).str.contains("Auto", case=False, na=False)]
        renderizar_unidad(df_autos)

    with tab_motos:
        # Filtramos por la primera columna (0) que contenga "Moto"
        df_motos = df_mostrar[df_mostrar.iloc[:, 0].astype(str).str.contains("Moto", case=False, na=False)]
        renderizar_unidad(df_motos)

except Exception as e:
    st.error(f"Hubo un error al conectar con la base de datos: {e}")












