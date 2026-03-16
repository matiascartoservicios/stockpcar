import streamlit as st
import pandas as pd

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
        margin-top: 0px !important;
    }
    div[data-testid="stTextInput"] label { display: none !important; }
    div[data-testid="stTextInput"] > div { margin-top: -10px !important; }
    div[data-baseweb="tab-list"] { width: 100% !important; display: flex !important; justify-content: center !important; }
    button[data-baseweb="tab"] { width: 50% !important; flex-grow: 1 !important; height: 50px !important; }
    div[data-testid="stMarkdownContainer"] p { font-size: 18px !important; font-weight: bold !important; }
    
    .carrusel-contenedor { display: flex; overflow-x: auto; gap: 10px; scroll-snap-type: x mandatory; padding-bottom: 10px; scrollbar-width: none; }
    .carrusel-contenedor::-webkit-scrollbar { display: none; }
    .carrusel-img { flex: 0 0 100%; scroll-snap-align: center; border-radius: 12px; height: 320px; object-fit: cover; background-color: #f0f2f6; box-shadow: 2px 2px 8px rgba(0,0,0,0.1); }
    
    .badge-oportunidad {
        background-color: #ff4b2b;
        color: white;
        padding: 4px 10px;
        border-radius: 5px;
        font-weight: bold;
        font-size: 14px;
        display: inline-block;
        margin-bottom: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. LOGO
URL_DE_TU_LOGO = 'https://i.postimg.cc/Cx1wcv1f/PCARA-Mesa-de-trabajo-1.png' 
st.markdown(f"<div style='text-align: center;'><img src='{URL_DE_TU_LOGO}' width='400'></div>", unsafe_allow_html=True)

st.markdown("---")

# 3. BOTONES DE CONTACTO (EL DISEÑO QUE TE GUSTA)
NUMERO_WA = "+5491164977257" 

st.markdown(f"""
    <div style="display: flex; gap: 10px; justify-content: center; margin-bottom: 15px;">
        <a href="https://maps.app.goo.gl/QbNXhUTyTyd793Zq8" target="_blank" style="text-decoration: none; width: 50%;">
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

# --- LÓGICA DEL BOTÓN DE OPORTUNIDADES ---
if 'filtro_oportunidad' not in st.session_state:
    st.session_state.filtro_oportunidad = False

def toggle_oportunidad():
    st.session_state.filtro_oportunidad = not st.session_state.filtro_oportunidad

# El botón ahora usa todo el ancho y cambia de texto según el estado
texto_boton = "❌ VER TODO EL STOCK" if st.session_state.filtro_oportunidad else "🔥 VER OPORTUNIDADES Y LIQUIDACIONES 🔥"
st.button(texto_boton, on_click=toggle_oportunidad, use_container_width=True)

st.markdown("---")

# 4. TÍTULO Y BUSCADOR
st.markdown(f"<h2 style='color: #004080; margin-bottom: 10px; text-align: center;'>STOCK DISPONIBLE</h2>", unsafe_allow_html=True)
busqueda = st.text_input(label="", placeholder="🔍 ¿Qué auto estás buscando?").strip().lower()

# 5. LÓGICA DE DATOS
SHEET_ID = '1TnIRP4doFAJk5u2lB6qGwqNJHPY4LNXWdx8KQaHWrSc'
url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv'

try:
    df = pd.read_csv(url)
    # Filtramos para que aparezcan tanto Disponible como Oportunidad
    df_mostrar = df[df['Estado'].isin(['Disponible', 'Oportunidad'])] if 'Estado' in df.columns else df

    # Si el botón de oportunidad está activado, filtramos solo esas
    if st.session_state.filtro_oportunidad:
        df_mostrar = df_mostrar[df_mostrar['Estado'] == 'Oportunidad']

    def generar_carrusel_html(fotos):
        fotos_validas = [f for f in fotos if pd.notna(f) and str(f).strip().startswith('http')]
        if not fotos_validas: return "<p style='text-align:center; color:gray;'>Sin fotos</p>"
        img_tags = "".join([f'<img src="{f}" class="carrusel-img">' for f in fotos_validas])
        return f'<div class="carrusel-contenedor">{img_tags}</div><p style="text-align: center; color: #888; font-size: 10px; margin-top: -5px;">⇠ Deslizá para ver más ⇢</p>'

    def mostrar_unidades(datos):
        if not datos.empty:
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
                    todas_las_fotos = [row['Foto_URL']] + [row[c] for c in row.index if c.startswith('Foto') and c != 'Foto_URL']
                    st.markdown(generar_carrusel_html(todas_las_fotos), unsafe_allow_html=True)
                    st.subheader(f"{row['Marca']} {row['Modelo']}")
                    st.write(f"Año: {row['Año']} | KM: {str(row['KM']).replace('.0', '')}")
                    
                    if 'MOTOR' in datos.columns and pd.notna(row['MOTOR']):
                        st.write(f"⚙️ {row['MOTOR']}")

                    if 'UBICACION' in datos.columns and pd.notna(row['UBICACION']):
                        st.markdown(f"📍 <span style='color: #004080; font-weight: bold;'>{row['UBICACION']}</span>", unsafe_allow_html=True)

                    # Etiqueta de Oportunidad
                    if 'Estado' in row and row['Estado'] == 'Oportunidad':
                        st.markdown('<div class="badge-oportunidad">🔥 PRECIO DE LIQUIDACIÓN</div>', unsafe_allow_html=True)

                    precio = str(row['Precio']) if pd.notna(row['Precio']) else "Consultar"
                    st.markdown(f"<h3 style='color: #004080;'>{precio}</h3>", unsafe_allow_html=True)
                    st.markdown("---")
        else:
            st.info("No hay unidades disponibles en esta selección.")

    tab_autos, tab_motos = st.tabs(["AUTOS", "MOTOS"])
    with tab_autos:
        mostrar_unidades(df_mostrar[df_mostrar.iloc[:, 0].astype(str).str.contains("Auto", case=False, na=False)])
    with tab_motos:
        mostrar_unidades(df_mostrar[df_mostrar.iloc[:, 0].astype(str).str.contains("Moto", case=False, na=False)])

except Exception as e:
    st.error(f"Error: {e}")
