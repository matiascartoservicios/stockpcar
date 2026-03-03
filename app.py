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

# 4. Buscador (Convertimos a minúsculas para que no falle)
    st.markdown(f"<h2 style='color: #004080; margin-bottom: -10px;'>STOCK DISPONIBLE</h2>", unsafe_allow_html=True)
    busqueda = st.text_input("", placeholder="🔍 Escribí Marca o Modelo...").strip().lower()

    # --- FILTRO LÓGICO SEGURO ---
    df_filtrado = df_mostrar.copy()

    if busqueda:
        # Esto busca en Marca y Modelo ignorando mayúsculas/minúsculas y errores de datos vacíos
        mask_marca = df_filtrado['Marca'].astype(str).str.lower().str.contains(busqueda, na=False)
        mask_modelo = df_filtrado['Modelo'].astype(str).str.lower().str.contains(busqueda, na=False)
        df_filtrado = df_filtrado[mask_marca | mask_modelo]

    # 5. Grilla de Autos
    if not df_filtrado.empty:
        cols = st.columns(3)
        
        for i, (index, row) in enumerate(df_filtrado.iterrows()):
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
                        for url in fotos_extra:
                            st.image(url, use_container_width=True)
                        
                        # BOTÓN SIMPLE PARA VOLVER AL INICIO
                        if st.button("⬆️ Volver al Inicio", key=f"btn_{index}"):
                            st.rerun() # Esto refresca la página y cierra todos los desplegables
                
              # 3. Título y Datos
                km_texto = str(row['KM']).replace('.0', '')
                st.subheader(f"{row['Marca']} {row['Modelo']}")
                
                # Datos básicos (Año y KM siempre van)
                st.write(f"Año: {row['Año']} | KM: {km_texto}")
                
                # --- COLUMNA EXTRA (Solo si tiene texto y no es nan) ---
                if 'Motor' in row and pd.notna(row['Motor']) and str(row['Motor']).strip() != "":
                    st.write(str(row['Motor']))
                
                # 4. Precio (Limpio, tal cual lo pongas en el Excel)
                precio_mostrar = str(row['Precio']) if pd.notna(row['Precio']) else "Consultar"
                st.markdown(f"<h2 style='color: #004080;'>{precio_mostrar}</h2>", unsafe_allow_html=True)
                st.markdown("---")
                
               
    else:
        st.info("No hay unidades que coincidan con esa búsqueda. ¡Probá con otra!")
except Exception as e:
    st.error(f"Hubo un error al conectar con la base de datos: {e}")











