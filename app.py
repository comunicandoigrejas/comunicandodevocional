import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configuração de Estilo (Cores: Azul, Roxo, Verde, Laranja, Amarelo)
st.set_page_config(page_title="Comunicando Devocional", page_icon="📖")

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 20px; font-weight: bold; }
    .isosed-btn { background-color: #6c5ce7 !important; color: white !important; }
    .cadastro-btn { background-color: #ff9f43 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Conexão com a Planilha (Usando o segredo do Streamlit)
# Certifique-se de que o st.secrets esteja configurado no Cloud
try:
    from streamlit_gsheets import GSheetsConnection
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error("Erro na conexão com a base de dados. Verifique os Secrets.")

# --- LÓGICA DE NAVEGAÇÃO ---
if 'pagina' not in st.session_state:
    st.session_state['pagina'] = 'home'

# --- TELA INICIAL (AS DUAS OPÇÕES) ---
if st.session_state['pagina'] == 'home':
    st.image("https://via.placeholder.com/150", width=100) # Coloque sua logo aqui
    st.title("📖 Comunicando Devocional")
    st.write("Escolha como deseja acessar sua leitura diária:")

    if st.button("Logar com ISOSED Cosmópolis", key="btn_isosed"):
        st.session_state['pagina'] = 'login_isosed'
        st.rerun()

    if st.button("Criar novo cadastro no Devocional", key="btn_novo"):
        st.session_state['pagina'] = 'cadastro'
        st.rerun()

# --- OPÇÃO 1: LOGIN ISOSED ---
elif st.session_state['pagina'] == 'login_isosed':
    st.subheader("🔐 Login ISOSED Cosmópolis")
    tel = st.text_input("Telefone (com DDD)")
    senha = st.text_input("Senha", type="password")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Entrar"):
            df = conn.read(worksheet="usuários")
            user = df[(df['telefone'].astype(str) == tel) & (df['senha'].astype(str) == senha)]
            if not user.empty:
                st.session_state['user'] = user.iloc[0].to_dict()
                st.session_state['pagina'] = 'devocional'
                st.rerun()
            else:
                st.error("Usuário não encontrado na base ISOSED.")
    with col2:
        if st.button("Voltar"):
            st.session_state['pagina'] = 'home'
            st.rerun()

# --- OPÇÃO 2: CADASTRO NOVO ---
elif st.session_state['pagina'] == 'cadastro':
    st.subheader("✨ Novo Cadastro")
    with st.form("form_cadastro"):
        nome = st.text_input("Nome Completo")
        tel_novo = st.text_input("Telefone")
        minis = st.text_input("Ministério")
        passw = st.text_input("Crie uma Senha", type="password")
        plano = st.selectbox("Escolha seu Plano", ["Plano Anual", "Novo Testamento", "Casais", "Jovens"])
        
        if st.form_submit_button("Finalizar Cadastro"):
            # Aqui você usaria conn.create para salvar na planilha
            st.success("Cadastro realizado! (Integração de escrita pendente)")
            st.session_state['pagina'] = 'home'

# --- ÁREA DO DEVOCIONAL ---
elif st.session_state['pagina'] == 'devocional':
    u = st.session_state['user']
    st.title(f"A paz do Senhor, {u['nome']}!")
    st.write(f"**Plano Ativo:** {u['plano_escolhido']} (Dia {u['dia_atual']})")
    
    st.divider()
    st.markdown("### 📜 Leitura de Hoje (ARA)")
    st.write("Texto bíblico sendo carregado...")
    
    if st.button("Sair"):
        st.session_state.clear()
        st.rerun()
