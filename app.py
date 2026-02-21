import streamlit as st
import pandas as pd

# 1. Configuração de Estilo e Identidade (Azul, Roxo, Verde, Laranja, Amarelo)
st.set_page_config(page_title="Comunicando Devocional", page_icon="📖")

st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; font-weight: bold; }
    /* Botão ISOSED - Roxo */
    div.stButton > button:first-child { background-color: #6c5ce7; color: white; }
    </style>
    """, unsafe_allow_html=True)

# 2. Inicialização da Navegação
if 'pagina' not in st.session_state:
    st.session_state['pagina'] = 'inicio'

# --- TELA INICIAL: AS TRÊS PORTAS ---
if st.session_state['pagina'] == 'inicio':
    st.title("📖 Comunicando Devocional")
    st.subheader("Bem-vindo, abençoado! Como deseja acessar?")
    
    if st.button("🚀 Entrar com ISOSED Cosmópolis"):
        st.session_state['pagina'] = 'login_isosed'
        st.rerun()
        
    if st.button("🔐 Já tenho cadastro no Devocional"):
        st.session_state['pagina'] = 'login_direto'
        st.rerun()
        
    if st.button("✨ Sou novo aqui, quero me cadastrar"):
        st.session_state['pagina'] = 'cadastro'
        st.rerun()

# --- CAMINHO 1: LOGIN ISOSED ---
elif st.session_state['pagina'] == 'login_isosed':
    st.header("Login ISOSED Cosmópolis")
    tel = st.text_input("Telefone")
    senha = st.text_input("Senha", type="password")
    if st.button("Confirmar Entrada"):
        # Lógica de busca na planilha (Aba usuários)
        st.success("Conectando à base ISOSED...")
        st.session_state['pagina'] = 'devocional'
        st.rerun()
    if st.button("Voltar"):
        st.session_state['pagina'] = 'inicio'
        st.rerun()

# --- CAMINHO 2: LOGIN DIRETO APP ---
elif st.session_state['pagina'] == 'login_direto':
    st.header("Login Comunicando Devocional")
    user_app = st.text_input("Usuário ou E-mail")
    senha_app = st.text_input("Senha", type="password")
    if st.button("Acessar Devocional"):
        st.session_state['pagina'] = 'devocional'
        st.rerun()
    if st.button("Voltar"):
        st.session_state['pagina'] = 'inicio'
        st.rerun()

# --- CAMINHO 3: CADASTRO NOVO ---
elif st.session_state['pagina'] == 'cadastro':
    st.header("Criar minha conta")
    nome = st.text_input("Nome Completo")
    tel_novo = st.text_input("WhatsApp")
    plano = st.selectbox("Selecione seu Plano", ["Plano Anual", "Casais", "Jovens"])
    if st.button("Finalizar e Entrar"):
        st.balloons()
        st.session_state['pagina'] = 'devocional'
        st.rerun()
    if st.button("Cancelar"):
        st.session_state['pagina'] = 'inicio'
        st.rerun()

# --- ÁREA FINAL: O DEVOCIONAL ---
elif st.session_state['pagina'] == 'devocional':
    st.title("🙏 Momento com Deus")
    st.info("Aqui você terá acesso à Bíblia ARA e aos seus planos de leitura.")
    if st.sidebar.button("Sair / Trocar Conta"):
        st.session_state['pagina'] = 'inicio'
        st.rerun()
