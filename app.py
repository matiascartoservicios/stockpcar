import streamlit as st
import pandas as pd
import urllib.parse

# 1. Configuración de la pestaña
st.set_page_config(page_title="PCAR - Stock", layout="wide", page_icon="🚗")

# --- CSS DEFINITIVO ---
st.markdown("""
    <style>
    [data-testid="stVerticalBlock"] > div:has(div.stTextInput) {
        position: sticky !important;
        top: 65px !important;
        z-index: 750 !important;
        background-color: white !important;
        padding-top: 5px !important;
        padding-bottom: 5px !important;
    }
    .carrusel-contenedor { display: flex; overflow-x: auto; gap: 10px; scroll-snap-type: x mandatory; padding-bottom: 10px; scrollbar-width: none; }
    .carrusel-contenedor::-webkit-scrollbar { display: none; }
    .carrusel-img { 
        flex: 0 0 100%; 
        scroll-snap-align: center; 
        border-radius: 12px; 
        height: 450px; 
        object-fit: contain; 
        background-color: #f0f2f6; 
    }
    .btn-compartir {
        background-color: #25D366;
        color: white !important;
        padding: 10px;
        border-radius: 8px;
        text-decoration: none;
        display: block;
        text-align: center;
        font-weight: bold;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. LOGO
URL_DE_TU_LOGO = 'https://i.postimg.cc/Cx1wcv1f/PCARA-Mesa-de-trabajo-1.png' 
st.markdown(f"<div style='text-align: center;'><img src='{URL_DE_TU_LOGO}' width='400'></div>", unsafe_allow_html=True)

# 3. DATOS Y LÓGICA DE URL
SHEET_ID = '1TnIRP4doFAJk5u2lB6qGwqNJHPY4LNXWdx8KQaHWrSc'
url_csv = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv'
NUMERO_WA = "+5491164977257"

try:
    df = pd.read_csv(url_csv)
    
    # --- NUEVO: Lógica de Deep Linking ---
    params = st.query_params
    unidad_id = params.get("id")

    if unidad_id:
        # Si hay un ID en la URL, filtramos solo esa unidad
        # Nota: Asegurate que en tu Excel la columna se llame 'ID'
        df_mostrar = df[df['ID'].astype(str) == str(unidad_id)]
        st.info("📍 Mostrando unidad específica seleccionada.")
        if st.button("⬅️ Ver todo el catálogo"):
            st.query_params.clear()
            st.rerun()
    else:
        # Lógica normal de filtros
        df_mostrar = df[df['Estado'].isin(['Disponible', 'Oportunidad'])] if 'Estado' in df.columns else df
        
        # Filtro de Oportunidades
        if 'filtro_oportunidad' not in st.session_state:
            st.session_state.filtro_oportunidad = False
        
        col1, col2 = st.columns([2, 1])
        with col1:
            busqueda = st.text_input(label="", placeholder="🔍 ¿Qué auto estás buscando?").strip().lower()
        with col2:
            if st.button("🔥 OPORTUNIDADES" if not st.session_state.filtro_oportunidad else "✅ TODO", use_container_width=True):
                st.session_state.filtro_oportunidad = not st.session_state.filtro_oportunidad
                st.rerun()
        
        if st.session_state.filtro_oportunidad:
            df_mostrar = df_mostrar[df_mostrar['Estado'] == 'Oportunidad']
        
        if busqueda:
            df_mostrar = df_mostrar[df_mostrar['Marca'].astype(str).str.lower().str.contains(busqueda) | 
                                    df_mostrar['Modelo'].astype(str).str.lower().str.contains(busqueda)]

    # --- FUNCIONES DE RENDERIZADO ---
    def generar_carrusel_html(row):
        fotos = [row['Foto_URL']] + [row[c] for c in row.index if c.startswith('Foto') and c != 'Foto_URL']
        fotos_validas = [f for f in fotos if pd.notna(f) and str(f).strip().startswith('http')]
        img_tags = "".join([f'<img src="{f}" class="carrusel-img">' for f in fotos_validas])
        return f'<div class="carrusel-contenedor">{img_tags}</div>'

    def mostrar_unidades(datos):
        if datos.empty:
            st.warning("No se encontraron unidades.")
            return

        cols = st.columns(3)
        for i, (index, row) in enumerate(datos.iterrows()):
            with cols[i % 3]:
                # Imágenes
                st.markdown(generar_carrusel_html(row), unsafe_allow_html=True)
                
                # Datos del auto
                st.subheader(f"{row['Marca']} {row['Modelo']}")
                st.write(f"Año: {row['Año']} | KM: {row['KM']}")
                
                # Link de compartir (NUEVO)
                # Creamos el link que el cliente va a abrir
                link_app = f"https://pcar-stock.streamlit.app/?id={row['ID']}"
                texto_wa = urllib.parse.quote(f"Hola! Te paso la info de esta unidad: {row['Marca']} {row['Modelo']}. Podés ver las fotos acá: {link_app}")
                link_wa = f"https://wa.me/?text={texto_wa}"
                
                st.markdown(f'<a href="{link_wa}" target="_blank" class="btn-compartir">📤 COMPARTIR POR WHATSAPP</a>', unsafe_allow_html=True)
                
                precio = str(row['Precio']) if pd.notna(row['Precio']) else "Consultar"
                st.markdown(f"<h3 style='color: #004080;'>{precio}</h3>", unsafe_allow_html=True)
                st.markdown("---")

    # Tabs de navegación
    if not unidad_id:
        tab_autos, tab_motos = st.tabs(["AUTOS", "MOTOS"])
        with tab_autos:
            mostrar_unidades(df_mostrar[df_mostrar.iloc[:, 0].astype(str).str.contains("Auto", case=False, na=False)])
        with tab_motos:
            mostrar_unidades(df_mostrar[df_mostrar.iloc[:, 0].astype(str).str.contains("Moto", case=False, na=False)])
    else:
        mostrar_unidades(df_mostrar)

except Exception as e:
    st.error(f"Error: {e}")
