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

# 3. --- BUSCADOR PRINCIPAL (Sticky y











