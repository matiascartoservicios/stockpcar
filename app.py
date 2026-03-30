import streamlit as st
import pandas as pd
import urllib.parse

# 1. Configuración de la pestaña
st.set_page_config(page_title="PCAR - Stock", layout="wide", page_icon="🚗")

# --- CSS (TU ESTILO ORIGINAL + BOTÓN COMPARTIR) ---
st.markdown("""
    <style>
    [data-testid="stVerticalBlock"] > div:has(div.stTextInput) {
        position: sticky !important;
        top: 65px !important;
        z-index: 750 !important;
        background-color: white !important;
        padding-top: 5px !important;
        padding-bottom: 5px !important;
        margin-top: 0px !important;
    }
    div[data-testid="stTextInput"] label { display: none !important; }
    div[data-testid="stTextInput"] > div { margin-top: -10px !important; }
    div[data-baseweb="tab-list"] { width: 100% !important; display: flex !important; justify-content: center !important; }
    button[data-baseweb="tab"] { width: 50% !important; flex-grow: 1 !important; height: 50px !important; }
    
    .carrusel-contenedor { display: flex; overflow-x: auto; gap: 10px; scroll-snap-type: x mandatory; padding-bottom: 10px; scrollbar-width: none; }
    .carrusel-contenedor::-webkit-scrollbar { display: none; }
    .carrusel-img { 
        flex: 0 0 100%; 
        scroll-snap-align: center; 
        border-radius: 12px; 
        height: 450px; 
        object-fit: contain; 
        background-color: #f0f2f6; 
        box-shadow: 2px 2px 8px rgba(0,0,0,0.1); 
    }
    
    /* Estilo para el nuevo botón de compartir */
    .btn-compartir {
        background-color: #25D366;
        color: white !important;
        padding: 8px;
        border-radius: 8px;
        text-decoration: none;
        display: block;
        text-align: center;
        font-weight: bold;
        margin-bottom: 10px;
        font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. LOGO
URL_DE_TU_LOGO = 'https://i.postimg.cc/Cx1wcv1f/PCARA-Mesa-de-trabajo-1.png' 
st.markdown(f"<div style='text-align: center;'><img src='{URL_DE_TU_LOGO}' width='400'></div>", unsafe_allow_html=True)

st.markdown("---")

# 3. BOTONES DE CONTACTO (RECUPERADOS)
NUMERO_WA = "+5491164977257" 

st.markdown(f"""
    <div style="display: flex; gap: 10px; justify-content: center; margin-bottom: 15px;">
        <a href="https://maps.google.com" target="_blank" style="text-decoration: none; width: 50%;">
            <div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px; border: 1px solid #004080; text-align: center; height: 80px; display: flex; flex-direction: column; justify-content: center;">
                <span style="color: #004080; font-weight: bold; font-size: 16px;">📍 UBICACIÓN VISITANOS!!</span>
            </div>
        </a>
        <a href="https://wa.me/{NUMERO_WA}" target="_blank" style="text-decoration: none; width: 50%;">
            <div style="background-color: #25D366; padding: 15px; border-radius: 10px; border: 1px solid #128C7E; text-align: center; height: 80px; display: flex; flex-direction: column; justify-content: center;">
                <span style="color: white; font-weight: bold; font-size: 16px;">💬 WHATSAPP CONSULTANOS!!</span>
            </div>
        </a>
    </div>
""", unsafe_allow_html=True)

# 4. LÓGICA DE DATOS
SHEET_ID = '1TnIRP4doFAJk5u2lB6qGwqNJHPY4LNXWdx8KQaHWrSc'
url_csv = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv'

try:
    df = pd.read_csv(url_csv)
    
    # --- CHEQUEO DE DEEP LINK ---
    unidad_id = st.query_params.get("id")

    # Botón Oportunidades (Original)
    if 'filtro_oportunidad' not in st.session_state:
        st.session_state.filtro_oportunidad = False

    def toggle_oportunidad():
        st.session_state.filtro_oportunidad = not st.session_state.filtro_oportunidad

    if not unidad_id:
        texto_boton = "❌ VER TODO EL STOCK" if st.session_state.filtro_oportunidad else "🔥 VER OPORTUNIDADES!!! 🔥"
        st.button(texto_boton, on_click=toggle_oportunidad, use_container_width=True)
        st.markdown("---")
        st.markdown(f"<h2 style='color: #004080; margin-bottom: 10px; text-align: center;'>STOCK DISPONIBLE</h2>", unsafe_allow_html=True)
        busqueda = st.text_input(label="", placeholder="🔍 ¿Qué auto estás buscando?").strip().lower()
    else:
        if st.button("⬅️ VOLVER AL CATÁLOGO COMPLETO", use_container_width=True):
            st.query_params.clear()
            st.rerun()
        busqueda = ""

    def generar_carrusel_html(fotos):
        fotos_validas = [f for f in fotos if pd.notna(f) and str(f).strip().startswith('http')]
        if not fotos_validas: return "<p style='text-align:center; color:gray;'>Sin fotos</p>"
        img_tags = "".join([f'<img src="{f}" class="carrusel-img">' for f in fotos_validas])
        return f'<div class="carrusel-contenedor">{img_tags}</div>'

    def mostrar_unidades(datos):
        if unidad_id:
            datos = datos[datos['ID'].astype(str) == str(unidad_id)]
        
        if not datos.empty:
            if busqueda and not unidad_id:
                mask = (datos['Marca'].astype(str).str.lower().str.contains(busqueda, na=False) | 
                        datos['Modelo'].astype(str).str.lower().str.contains(busqueda, na=False))
                datos = datos[mask]

            cols = st.columns(3)
            for i, (index, row) in enumerate(datos.iterrows()):
                with cols[i % 3]:
                    todas_las_fotos = [row['Foto_URL']] + [row[c] for c in row.index if c.startswith('Foto') and c != 'Foto_URL']
                    st.markdown(generar_carrusel_html(todas_las_fotos), unsafe_allow_html=True)
                    st.subheader(f"{row['Marca']} {row['Modelo']}")
                    
                    # --- BOTÓN COMPARTIR ---
                    link_app = f"https://pcar-stock.streamlit.app/?id={row['ID']}"
                    msg = urllib.parse.quote(f"Hola! Mirá este {row['Marca']} {row['Modelo']} en PCAR: {link_app}")
                    st.markdown(f'<a href="https://wa.me/?text={msg}" target="_blank" class="btn-compartir">📤 COMPARTIR UNIDAD</a>', unsafe_allow_html=True)
                    
                    st.write(f"Año: {row['Año']} | KM: {str(row['KM']).replace('.0', '')}")
                    precio = str(row['Precio']) if pd.notna(row['Precio']) else "Consultar"
                    st.markdown(f"<h3 style='color: #004080;'>{precio}</h3>", unsafe_allow_html=True)
                    st.markdown("---")

    # Filtrado por Estado
    df_mostrar = df[df['Estado'].isin(['Disponible', 'Oportunidad'])] if 'Estado' in df.columns else df
    if st.session_state.filtro_oportunidad and not unidad_id:
        df_mostrar = df_mostrar[df_mostrar['Estado'] == 'Oportunidad']

    if unidad_id:
        mostrar_unidades(df_mostrar)
    else:
        tab_autos, tab_motos = st.tabs(["AUTOS", "MOTOS"])
        with tab_autos:
            mostrar_unidades(df_mostrar[df_mostrar.iloc[:, 0].astype(str).str.contains("Auto", case=False, na=False)])
        with tab_motos:
            mostrar_unidades(df_mostrar[df_mostrar.iloc[:, 0].astype(str).str.contains("Moto", case=False, na=False)])

except Exception as e:
    st.error(f"Error: {e}")
