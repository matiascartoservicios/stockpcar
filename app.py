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

# --- UBICACIÓN DE LA AGENCIA (Debajo del logo y arriba de Stock) ---
st.markdown(f"""
    <div style='text-align: center; margin-top: -10px; margin-bottom: 25px;'>
        <a href='https://maps.google.com/?cid=1158533433268707757&g_mp=CiVnb29nbGUubWFwcy5wbGFjZXMudjEuUGxhY2VzLkdldFBsYWNl' target='_blank' style='text-decoration: none;'>
            <div style='display: inline-block; background-color: #f0f2f6; padding: 10px 20px; border-radius: 10px; border: 1px solid #004080;'>
                <span style='color: #004080; font-weight: bold; font-size: 16px;'>
                    📍 PCAR AUTOS
                </span>
                <br>
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

# ... (Todo tu código anterior de logo y ubicación queda igual) ...

# 4. Buscador
st.markdown(f"<h2 style='color: #004080; margin-bottom: -10px;'>STOCK DISPONIBLE</h2>", unsafe_allow_html=True)
busqueda = st.text_input("", placeholder="🔍 Escribí Marca o Modelo...").strip().lower()

# --- NUEVA SECCIÓN DE PESTAÑAS ---
tab_autos, tab_motos = st.tabs(["🚗 AUTOS", "🏍️ MOTOS"])

# Función para mostrar la grilla (para no repetir código)
def mostrar_grilla(dataframe):
    if not dataframe.empty:
        cols = st.columns(3)
        for i, (index, row) in enumerate(dataframe.iterrows()):
            with cols[i % 3]:
                # 1. Foto Principal
                st.image(row['Foto_URL'], use_container_width=True)
                
                # 2. Galería de Fotos
                fotos_extra = []
                for col_name in row.index:
                    if col_name.startswith('Foto') and col_name != 'Foto_URL':
                        if pd.notna(row[col_name]) and str(row[col_name]).strip() != "":
                            fotos_extra.append(row[col_name])
                
                if fotos_extra:
                    with st.expander("📸 Ver más fotos"):
                        for url_foto in fotos_extra:
                            st.image(url_foto, use_container_width=True)
                
                # 3. Título y Datos
                km_texto = str(row['KM']).replace('.0', '')
                st.subheader(f"{row['Marca']} {row['Modelo']}")
                st.write(f"Año: {row['Año']} | KM: {km_texto}")
                
                if 'Motor' in row and pd.notna(row['Motor']) and str(row['Motor']).strip() != "":
                    st.write(str(row['Motor']))
                
                # 4. Precio
                precio_mostrar = str(row['Precio']) if pd.notna(row['Precio']) else "Consultar"
                st.markdown(f"<h3 style='color: #004080;'>{precio_mostrar}</h3>", unsafe_allow_html=True)
                st.markdown("---")
    else:
        st.info("No hay unidades disponibles en esta categoría.")

# --- LÓGICA DE FILTRADO POR PESTAÑA ---

# Filtro general por búsqueda
df_filtrado = df_mostrar.copy()
if busqueda:
    mask = (df_filtrado['Marca'].astype(str).str.lower().str.contains(busqueda, na=False) | 
            df_filtrado['Modelo'].astype(str).str.lower().str.contains(busqueda, na=False))
    df_filtrado = df_filtrado[mask]

# Pestaña 1: AUTOS
with tab_autos:
    # Filtramos por la primera columna (Categoría) que diga "Auto"
    df_solo_autos = df_filtrado[df_filtrado.iloc[:, 0].astype(str).str.contains("Auto", case=False, na=False)]
    mostrar_grilla(df_solo_autos)

# Pestaña 2: MOTOS
with tab_motos:
    # Filtramos por la primera columna (Categoría) que diga "Moto"
    df_solo_motos = df_filtrado[df_filtrado.iloc[:, 0].astype(str).str.contains("Moto", case=False, na=False)]
    mostrar_grilla(df_solo_motos)

# ... (El resto del bloque try/except queda igual) ...












