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

# 4. Buscador con título nuevo
    st.markdown(f"<h2 style='color: #004080; margin-bottom: -10px;'>STOCK DISPONIBLE</h2>", unsafe_allow_html=True)
    busqueda = st.text_input("", placeholder="🔍 Escribí Marca o Modelo...")

  # 5. Grilla de Autos
    if len(df_mostrar) > 0:
        cols = st.columns(3)
        
        for i, (index, row) in enumerate(df_mostrar.iterrows()):
            with cols[i % 3]:
                # --- AQUÍ EMPIEZA LO NUEVO ---
                
                # 1. Foto Principal
                st.image(row['Foto_URL'], use_container_width=True)
                
                # 2. Galería Desplegable (Lo que querías esconder)
                fotos_extra = []
                for col_foto in ['Foto2', 'Foto3', 'Foto4']:
                    if col_foto in row and pd.notna(row[col_foto]):
                        fotos_extra.append(row[col_foto])
                
                if fotos_extra:
                    with st.expander("📸 Ver más fotos de esta unidad"):
                        for url in fotos_extra:
                            st.image(url, use_container_width=True)
                
                # 3. Título y Datos
                km_texto = str(row['KM']).replace('.0', '')
                st.subheader(f"{row['Marca']} {row['Modelo']}")
                
                # Agregamos la nueva columna aquí:
                motor_info = row['Motor'] if 'Motor' in row else ""
                
                st.write(f"Año: {row['Año']} | KM: {km_texto} | {motor_info}")
                
                # 4. Precio Grande y Azul
                st.markdown(f"<h2 style='color: #004080;'>$ {row['Precio']}</h2>", unsafe_allow_html=True)
                
                st.markdown("---")
    else:
        st.info("No hay unidades que coincidan con la búsqueda.")

except Exception as e:
    st.error(f"Hubo un error al conectar con la base de datos: {e}")




