import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Configuração da página - Cores que você pediu
st.set_page_config(page_title="Devocional ISOSED", page_icon="📖")

# Estilo visual Comunicando Igrejas
st.markdown("""
    <style>
    .stApp { background: linear-gradient(to right, #6c5ce7, #a29bfe); color: white; }
    .stButton>button { background-color: #ff9f43; border: none; color: white; }
    </style>
    """, unsafe_allow_html=True)

# Tenta conectar na planilha
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error(f"Erro de conexão: {e}")

# --- TELA DE LOGIN ---
if 'logado' not in st.session_state:
    st.session_state['logado'] = False

if not st.session_state['logado']:
    st.title("🛡️ ISOSED Cosmópolis")
    st.subheader("Login do Devocional")
    
    tel = st.text_input("Telefone (igual na planilha)")
    pw = st.text_input("Senha", type="password")
    
    if st.button("Entrar no Plano de Leitura"):
        try:
            df = conn.read(worksheet="usuários")
            # Ajuste: garantindo que telefone e senha sejam comparados como texto
            user = df[(df['telefone'].astype(str) == str(tel)) & (df['senha'].astype(str) == str(pw))]
            
            if not user.empty:
                st.session_state['logado'] = True
                st.session_state['user'] = user.iloc[0].to_dict()
                st.rerun()
            else:
                st.error("Irmão, não encontramos esse telefone ou senha.")
        except Exception as e:
            st.warning("Verifique se o nome da aba na planilha é exatamente 'usuários'.")
            st.error(f"Detalhe do erro: {e}")

# --- ÁREA DO IRMÃO ---
else:
    u = st.session_state['user']
    st.header(f"A paz do Senhor, {u['nome']}!")
    
    tab1, tab2 = st.tabs(["📖 Leitura", "⚙️ Dados"])
    
    with tab1:
        st.subheader(f"Plano: {u['plano_escolhido']}")
        st.info(f"Você está no **Dia {u['dia_atual']}**")
        st.write("---")
        st.markdown("### 📜 Palavra de Hoje (ARA)")
        st.write("Em breve: O texto bíblico aparecerá aqui automaticamente!")
        
    with tab2:
        st.write(f"**Ministério:** {u['ministerio']}")
        if st.sidebar.button("Sair"):
            st.session_state['logado'] = False
            st.rerun()
