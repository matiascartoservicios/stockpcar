import streamlit as st
import pandas as pd

# 1. Configuración de la pestaña
st.set_page_config(page_title="PCAR - Stock", layout="wide", page_icon="🚗")

# 2. LOGO DE LA AGENCIA
URL_DE_TU_LOGO = 'https://i.postimg.cc/4ybLF4cF/pcar-Mesa-de-trabajo-1.png' 

st.markdown(f"""
    <div style='text-align: center;'>
        <img src='{URL_DE_TU_LOGO}' width='400' style='margin-bottom: 20px;'>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

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
    st.subheader("Filtrar Unidades")
    busqueda = st.text_input("", placeholder="Escribí Marca o Modelo...")

    if busqueda:
        df_mostrar = df_mostrar[
            df_mostrar['Marca'].astype(str).str.contains(busqueda, case=False) | 
            df_mostrar['Modelo'].astype(str).str.contains(busqueda, case=False)
        ]

    st.markdown(f"**{len(df_mostrar)} Unidades Disponibles**")

    # 5. Grilla de Autos (Estructura limpia para evitar rectángulos)
    if len(df_mostrar) > 0:
        cols = st.columns(3)
        
        for i, (index, row) in enumerate(df_mostrar.iterrows()):
            with cols[i % 3]:
                # Mostramos la foto
                st.image(row['Foto_URL'], use_container_width=True)
                
                # Datos del auto
                st.subheader(f"{row['Marca']} {row['Modelo']}")
                
                # Info SIN ICONOS
                st.write(f"Año: {row['Año']} | KM: {row['KM']}")
                
                # Opción B: Más grande y color de la agencia
                st.markdown(f"<h2 style='color: #004080;'>$ {row['Precio']}</h2>", unsafe_allow_html=True)
                
                st.markdown("---")
    else:
        st.info("No hay unidades que coincidan con la búsqueda.")

except Exception as e:
    st.error(f"Hubo un error al conectar con la base de datos: {e}")