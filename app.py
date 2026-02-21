import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Configuração da página com as cores da ISOSED
st.set_page_config(page_title="Devocional ISOSED", page_icon="🙏")

# Conexão com a Planilha (Certifique-se de configurar os Secrets no Streamlit Cloud!)
conn = st.connection("gsheets", type=GSheetsConnection)

def login():
    st.markdown("<h2 style='color: #6c5ce7;'>ISOSED Cosmópolis</h2>", unsafe_allow_html=True)
    tel = st.text_input("Telefone")
    pw = st.text_input("Senha", type="password")
    
    if st.button("Entrar"):
        df = conn.read(worksheet="usuários")
        # Filtra pelo telefone e senha da sua planilha
        user = df[(df['telefone'].astype(str) == tel) & (df['senha'].astype(str) == pw)]
        
        if not user.empty:
            st.session_state['user'] = user.iloc[0].to_dict()
            st.rerun()
        else:
            st.error("Dados não encontrados na base do ISOSED.")

if 'user' not in st.session_state:
    login()
else:
    u = st.session_state['user']
    
    # Menu em Abas
    aba1, aba2, aba3 = st.tabs(["📖 Devocional", "📈 Progresso", "👤 Perfil"])
    
    with aba1:
        st.header(f"Olá, {u['nome']}!")
        st.subheader(f"Plano: {u['plano_escolhido']}")
        st.info(f"Hoje é o seu **Dia {u['dia_atual']}** de leitura.")
        # Espaço para o texto bíblico ARA
        st.write("---")
        st.markdown("### 📜 Leitura do Dia")
        st.write("Aqui buscaremos o texto da Bíblia ARA correspondente ao plano...")
        
    with aba2:
        st.write("### Seu desempenho")
        st.progress(int(u['dia_atual']) / 365) # Exemplo para plano anual
        
    with aba3:
        st.write(f"**Ministério:** {u['ministerio']}")
        st.write(f"**Data de Nascimento:** {u['nascimento']}")
        if st.button("Sair"):
            del st.session_state['user']
            st.rerun()
