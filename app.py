import streamlit as st
import pandas as pd

# 1. Configuración de la pestaña
st.set_page_config(page_title="PCAR - Stock", layout="wide", page_icon="🚗")

# --- CSS DEFINITIVO: STICKY FUNCIONAL, CAJA FINA Y AYUDA CARRUSEL ---
st.markdown("""
    <style>
    /* 1. Forza que el contenedor del buscador sea STICKY y fino */
    [data-testid="stVerticalBlock"] > div:has(div.stTextInput) {
        position: sticky !important;
        top: 65px !important;
        z-index: 750 !important;
        background-color: white !important;
        padding-top: 5px !important;
        padding-bottom: 5px !important;
        margin-top: 0px !important;
    }

    /* Ocultamos el label (título) para que no ocupe espacio arriba */
    div[data-testid="stTextInput"] label {
        display: none !important;
    }

    /* Ajuste de margen para que el input no tenga aire extra */
    div[data-testid="stTextInput"] > div {
        margin-top: -10px !important;
    }
    
    /* Estilo de las pestañas 50/50 */
    div[data-baseweb="tab-list"] {
        width: 100% !important;
        display: flex !important;
        justify-content: center !important;
    }
    button[data-baseweb="tab"] {
        width: 50% !important;
        flex-grow: 1 !important;
        height: 50px !important;
    }
    div[data-testid="stMarkdownContainer"] p {
        font-size: 18px !important;
        font-weight: bold !important;
    }
    
    /* Carrusel de fotos */
    .carrusel-contenedor {
        display: flex;
        overflow-x: auto;
        gap: 10px;
        scroll-snap-type: x mandatory;
        padding-bottom: 10px;
        scrollbar-width: none;
    }
    .carrusel-contenedor::-webkit-scrollbar { display: none; }
    .carrusel-img {
        flex: 0 0 100%;
        scroll-snap-align: center;
        border-radius: 12px;
        height: 320px;
        object-fit: cover;
        background-color: #f0f2f6;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# 2. LOGO
URL_DE_TU_LOGO = 'https://i.postimg.cc/Cx1wcv1f/PCARA-Mesa-de-trabajo-1.png' 
st.markdown(f"<div style='text-align: center;'><img src='{URL_DE_TU_LOGO}' width='400'></div>", unsafe_allow_html=True)

st.markdown("---")

# 3. BOTONES DE CONTACTO
NUMERO_WA = "+5491164977257" 
st.markdown(f"""
    <div style="display: flex; gap: 10px; justify-content: center; margin-bottom: 20px;">
        <a href="https://www.google.com/maps" target="_blank" style="text-decoration: none; width: 50%;">
            <div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px; border: 1px solid #004080; text-align: center; height: 80px; display: flex; flex-direction: column; justify-content: center;">
                <span style="color: #004080; font-weight: bold; font-size: 16px;">📍 UBICACIÓN</span>
            </div>
        </a>
        <a href="https://wa.me/{NUMERO_WA}" target="_blank" style="text-decoration: none; width: 50%;">
            <div style="background-color: #25D366; padding: 15px; border-radius: 10px; border: 1px solid #128C7E; text-align: center; height: 80px; display: flex; flex-direction: column; justify-content: center;">
                <span style="color: white; font-weight: bold; font-size: 16px;">💬 WHATSAPP</span>
            </div>
        </a>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# 4. TÍTULO Y LUEGO BUSCADOR
st.markdown(f"<h2 style='color: #004080; margin-bottom: 10px; text-align: center;'>STOCK DISPONIBLE</h2>", unsafe_allow_html=True)

# Buscador Sticky
busqueda = st.text_input(label="", placeholder="🔍 ¿Qué auto estás buscando?").strip().lower()

# 5. LÓGICA DE DATOS
SHEET_ID = '1TnIRP4doFAJk5u2lB6qGwqNJHPY4LNXWdx8KQaHWrSc'
url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv'

try:
    df = pd.read_csv(url)
    df_mostrar = df[df['Estado'] == 'Disponible'] if 'Estado' in df.columns else df

    def generar_carrusel_html(fotos):
        fotos_validas = [f for f in fotos if pd.notna(f) and str(f).strip().startswith('http')]
        if not fotos_validas: return "<p style='text-align:center; color:gray;'>Sin fotos</p>"
        img_tags = "".join([f'<img src="{f}" class="carrusel-img">' for f in fotos_validas])
        html = f"""
        <div class="carrusel-contenedor">
            {img_tags}
        </div>
        <p style="text-align: center; color: #888; font-size: 10px; margin-top: -5px;">⇠ Deslizá para ver más ⇢</p>
        """
        return html

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
                    
                    # Info básica
                    st.write(f"Año: {row['Año']} | KM: {str(row['KM']).replace('.0', '')}")
                    
                    # --- AQUÍ ESTÁ EL CAMBIO: MOSTRAR COLUMNA MOTOR ---
                    if 'MOTOR' in datos.columns and pd.notna(row['MOTOR']):
                        st.write(f" **{row['MOTOR']}**")
                    elif 'Motor' in datos.columns and pd.notna(row['Motor']):
                        st.write(f"**{row['Motor']}**")
                    # -------------------------------------------------

                    precio = str(row['Precio']) if pd.notna(row['Precio']) else "Consultar"
                    st.markdown(f"<h3 style='color: #004080;'>{precio}</h3>", unsafe_allow_html=True)
                    st.markdown("---")
        else:
            st.info("No hay unidades disponibles.")

    # 6. PESTAÑAS
    tab_autos, tab_motos = st.tabs(["AUTOS", "MOTOS"])
    with tab_autos:
        mostrar_unidades(df_mostrar[df_mostrar.iloc[:, 0].astype(str).str.contains("Auto", case=False, na=False)])
    with tab_motos:
        mostrar_unidades(df_mostrar[df_mostrar.iloc[:, 0].astype(str).str.contains("Moto", case=False, na=False)])

except Exception as e:
    st.error(f"Error: {e}")

