import streamlit as st
from streamlit_gsheets 
import GSheetsConnection
import pandas as pd

# Configuração visual - Cores Comunicando Igrejas
st.set_page_config(page_title="Devocional ISOSED", page_icon="🙏")

# Conexão com a Planilha
conn = st.connection("gsheets", type=GSheetsConnection)

def carregar_dados():
    # Carrega a aba 'usuários' (ajuste o nome se for diferente na planilha)
    return conn.read(worksheet="usuários")

def atualizar_progresso(telefone, novo_dia):
    # Aqui adicionaríamos a lógica para salvar de volta na planilha
    st.info(f"Progresso do telefone {telefone} atualizado para o dia {novo_dia}!")

# --- TELA DE LOGIN ---
if 'logado' not in st.session_state:
    st.session_state['logado'] = False

if not st.session_state['logado']:
    st.markdown("<h2 style='color: #2e86de;'>Portal ISOSED Cosmópolis</h2>", unsafe_allow_html=True)
    st.write("Identifique-se para continuar sua leitura bíblica.")
    
    campo_tel = st.text_input("Telefone (com DDD)")
    campo_senha = st.text_input("Senha", type="password")
    
    if st.button("Entrar no Devocional"):
        df = carregar_dados()
        # Busca o usuário pelo telefone e senha
        usuario = df[(df['telefone'].astype(str) == campo_tel) & (df['senha'].astype(str) == campo_senha)]
        
        if not usuario.empty:
            st.session_state['logado'] = True
            st.session_state['user_data'] = usuario.iloc[0].to_dict()
            st.rerun()
        else:
            st.error("Varão, telefone ou senha incorretos. Verifique seus dados no ISOSED.")

# --- ÁREA DO DEVOCIONAL ---
else:
    user = st.session_state['user_data']
    st.sidebar.title(f"A paz do Senhor,")
    st.sidebar.subheader(f"{user['nome']}")
    st.sidebar.markdown(f"**Ministério:** {user['ministerio']}")
    
    if st.sidebar.button("Sair"):
        st.session_state['logado'] = False
        st.rerun()

    # Conteúdo Principal
    st.title(f"📖 {user['plano_escolhido']}")
    dia_atual = int(user['dia_atual'])
    
    st.info(f"✨ Você está no **Dia {dia_atual}** da sua jornada com Deus.")
    
    # Simulação da Versão ARA
    st.subheader("Leitura de Hoje (ARA)")
    st.write("Aqui aparecerá o texto bíblico baseado no dia e plano...")
    
    if st.button("Marcar dia como concluído"):
        # Lógica para avançar o dia
        novo_dia = dia_atual + 1
        atualizar_progresso(user['telefone'], novo_dia)
        st.balloons()
        st.success("Glória a Deus! Até amanhã!")
