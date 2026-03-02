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

# 4. Buscador
    st.markdown(f"<h2 style='color: #004080; margin-bottom: -10px;'>STOCK DISPONIBLE</h2>", unsafe_allow_html=True)
    busqueda = st.text_input("", placeholder="🔍 Escribí Marca o Modelo...").lower()

    # --- FILTRO LÓGICO ---
    # Esto hace que la lista se achique a medida que escribís
    df_filtrado = df_mostrar.copy()
    if busqueda:
        df_filtrado = df_mostrar[
            df_mostrar['Marca'].str.lower().contains(busqueda, na=False) | 
            df_mostrar['Modelo'].str.lower().contains(busqueda, na=False)
        ]

    # 5. Grilla de Autos (Ahora usamos df_filtrado)
    if not df_filtrado.empty:
        # Armamos columnas de a 3 para que quede prolijo
        cols = st.columns(3)
        
        for i, (index, row) in enumerate(df_filtrado.iterrows()):
            with cols[i % 3]:
                # 1. Foto Principal
                st.image(row['Foto_URL'], use_container_width=True)
                
                # 2. Ver más fotos (Expander)
                fotos_extra = []
                for col_foto in ['Foto2', 'Foto3', 'Foto4']:
                    if col_foto in row and pd.notna(row[col_foto]):
                        fotos_extra.append(row[col_foto])
                
                if fotos_extra:
                    with st.expander("📸 Ver más fotos"):
                        for url in fotos_extra:
                            st.image(url, use_container_width=True)
                
                # 3. Título y Datos
                km_texto = str(row['KM']).replace('.0', '')
                st.subheader(f"{row['Marca']} {row['Modelo']}")
                
                # Aquí mostramos los datos (incluyendo la columna nueva que agregaste)
                # Si tu columna nueva se llama 'Motor', cambialo acá:
                motor_info = row['Motor'] if 'Motor' in row else ""
                st.write(f"Año: {row['Año']} | KM: {km_texto} | {motor_info}")
                
                # 4. Precio
                st.markdown(f"<h2 style='color: #004080;'>$ {row['Precio']}</h2>", unsafe_allow_html=True)
                st.markdown("---")
    else:
        st.warning("No se encontraron unidades que coincidan con tu búsqueda.")
except Exception as e:
    st.error(f"Hubo un error al conectar con la base de datos: {e}")





