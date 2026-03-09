import streamlit as st
import pandas as pd

# 1. Configuración de la pestaña
st.set_page_config(page_title="PCAR - Stock", layout="wide", page_icon="🚗")

# --- ESTILO CSS ACTUALIZADO: BUSCADOR STICKY, CARRUSEL Y PESTAÑAS ---
st.markdown("""
    <style>
    /* Buscador Sticky (se queda arriba al hacer scroll) */
    div[data-testid="stForm"], div[data-testid="stVerticalBlock"] > div:has(div.stTextInput) {
        position: sticky;
        top: 0;
        z-index: 1000;
        background-color: white;
        padding: 10px 0px;
    }
    
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
    /* Estilo del texto en pestañas */
    div[data-testid="stMarkdownContainer"] p {
        font-size: 18px !important;
        font-weight: bold !important;
    }
    
    /* Estilo del Carrusel Deslizable */
    .carrusel-contenedor {
        display: flex;
        overflow-x: auto;
        gap: 10px;
        scroll-snap-type: x mandatory;
        padding-bottom: 15px;
        scrollbar-width: none;
    }
    .carrusel-contenedor::-webkit-scrollbar {
        display: none;
    }
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

# 2. LOGO DE LA AGENCIA
URL_DE_TU_LOGO = 'https://i.postimg.cc/Cx1wcv1f/PCARA-Mesa-de-trabajo-1.png' 

st.markdown(f"""
    <div style='text-align: center;'>
        <img src='{URL_DE_TU_LOGO}' width='400' style='margin-bottom: 20px;'>
    </div>
""", unsafe_allow_html=True)

# 3. --- BUSCADOR PRINCIPAL (Sticky y Ancho Completo) ---
# Lo ponemos arriba de los botones para que sea lo primero que se fije al scrollear
busqueda = st.text_input("¿Qué estás buscando?", placeholder="🔍 Ej: Hilux, Fiat Toro, BMW...").strip().lower()

st.markdown("---")

# 4. --- BOTONES DE CONTACTO ---
NUMERO_WA = "+5491164977257" 

st.markdown(f"""
    <div style="display: flex; gap: 10px; justify-content: center; margin-bottom: 25px;">
        <a href="https://maps.google.com" target="_blank" style="text-decoration: none; width: 50%;">
            <div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px; border: 1px solid #004080; text-align: center; height: 85px; display: flex; flex-direction: column; justify-content: center;">
                <span style="color: #004080; font-weight: bold; font-size: 16px;">📍 UBICACIÓN</span>
                <span style="color: #555; font-size: 12px;">VISITANOS!!</span>
            </div>
        </a>
        <a href="https://wa.me/{NUMERO_WA}?text=Hola!%20Vengo%20desde%20el%20catálogo%20PCAR" target="_blank" style="text-decoration: none; width: 50%;">
            <div style="background-color: #25D366; padding: 15px; border-radius: 10px; border: 1px solid #128C7E; text-align: center; height: 85px; display: flex; flex-direction: column; justify-content: center;">
                <span style="color: white; font-weight: bold; font-size: 16px;">💬 WHATSAPP</span>
                <span style="color: white; font-size: 12px;">CONSULTANOS!!</span>
            </div>
        </a>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# 5. Conexión con Google Sheets
SHEET_ID = '1TnIRP4doFAJk5u2lB6qGwqNJHPY4LNXWdx8KQaHWrSc'
url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv'

try:
    df = pd.read_csv(url)

    if 'Estado' in df.columns:
        df_mostrar = df[df['Estado'] == 'Disponible']
    else:
        df_mostrar = df

    # --- FUNCIÓN PARA RENDERIZAR EL CARRUSEL ---
    def generar_carrusel_html(fotos):
        fotos_validas = [f for f in fotos if pd.notna(f) and str(f).strip().startswith('http')]
        if not fotos_validas:
            return "<p style='color: gray;'>Sin fotos disponibles</p>"
        
        img_tags = "".join([f'<img src="{f}" class="carrusel-img">' for f in fotos_validas])
        html = f"""
        <div class="carrusel-contenedor">
            {img_tags}
        </div>
        <p style="text-align: center; color: #888; font-size: 10px; margin-top: -5px;">⇠ Deslizá para ver más ⇢</p>
        """
        return html

    # --- FUNCIÓN PARA RENDERIZAR GRILLA ---
    def mostrar_unidades(datos):
        if not datos.empty:
            # El filtro de búsqueda ahora aplica aquí globalmente
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
                    # Recopilamos todas las fotos
                    todas_las_fotos = [row['Foto_URL']] + [row[c] for c in row.index if c.startswith('Foto') and c != 'Foto_URL']
                    
                    st.markdown(generar_carrusel_html(todas_las_fotos), unsafe_allow_html=True)
                    
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

    # --- PESTAÑAS 50/50 ---
    st.markdown(f"<h2 style='color: #004080; margin-top: 10px;'>STOCK DISPONIBLE</h2>", unsafe_allow_html=True)
    tab_autos, tab_motos = st.tabs(["AUTOS", "MOTOS"])

    with tab_autos:
        df_autos = df_mostrar[df_mostrar.iloc[:, 0].astype(str).str.contains("Auto", case=False, na=False)]
        mostrar_unidades(df_autos)

    with tab_motos:
        df_motos = df_mostrar[df_mostrar.iloc[:, 0].astype(str).str.contains("Moto", case=False, na=False)]
        mostrar_unidades(df_motos)

except Exception as e:
    st.error(f"Error: {e}")










