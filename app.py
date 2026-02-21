import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# 1. Configuração da Identidade Visual (Cores Comunicando Igrejas)
st.set_page_config(page_title="Devocional Comunicando Igrejas", page_icon="📖")

# Mock de Banco de Dados (Em um app real, carregaríamos de um arquivo YAML ou Banco de Dados)
# Aqui definimos o usuário: 'willian' e a senha: '123' (exemplo abençoado)
config = {
    'credentials': {
        'usernames': {
            'willian': {
                'email': 'contato@comunicandoigrejas.com',
                'name': 'Willian - Comunicando Igrejas',
                'password': 'abc' # No código real, use senhas criptografadas
            }
        }
    },
    'cookie': {
        'expiry_days': 30,
        'key': 'devocional_signature',
        'name': 'devocional_cookie'
    }
}

# Criptografia simples para o exemplo (O Streamlit requer isso)
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# Renderiza o formulário de Login
# O parâmetro 'location' define onde o formulário aparece
# O título agora é definido dentro da função ou por um st.header antes
st.header("Login - Paz do Senhor!")
authentication_status = authenticator.login(location='main')

# Nas versões novas, os dados ficam guardados no st.session_state
name = st.session_state["name"]
authentication_status = st.session_state["authentication_status"]
username = st.session_state["username"]

if authentication_status:
    # --- ÁREA LOGADA DO IRMÃO ---
    authenticator.logout('Sair do App', 'sidebar')
    
    st.sidebar.title(f"Bem-vindo, {name}!")
    st.sidebar.markdown("---")
    
    # Simulação de progresso salvo (isso viria de um banco de dados)
    # No Streamlit, usamos 'session_state' para manter enquanto o app roda
    if 'progresso' not in st.session_state:
        st.session_state['progresso'] = 10  # Exemplo: parou no dia 10

    st.title("🙏 Seu Progresso de Leitura")
    
    plano = st.selectbox("Selecione seu plano ativo:", ["Bíblia em 1 Ano", "Casais 30 Dias", "Jovens 90 Dias"])
    
    # Barra de progresso baseada no que foi salvo
    progresso_atual = st.session_state['progresso']
    st.write(f"Varão, você está no **Dia {progresso_atual}** do plano {plano}.")
    st.progress(progresso_atual / 365 if "1 Ano" in plano else progresso_atual / 30)

    if st.button("✅ Marcar dia de hoje como lido"):
        st.session_state['progresso'] += 1
        st.success("Glória a Deus! Progresso salvo com sucesso.")
        st.balloons()

    # --- ÁREA DA PALAVRA (ARA) ---
    st.markdown("---")
    st.subheader("📖 Leitura de Hoje (Versão ARA)")
    st.info("João 3:16 - 'Porque Deus amou ao mundo de tal maneira que deu o seu Filho unigênito, para que todo o que nele crê não pereça, mas tenha a vida eterna.'")

elif authentication_status == False:
    st.error('Usuário ou senha incorretos, irmão. Tente novamente.')
elif authentication_status == None:
    st.warning('Por favor, insira suas credenciais para continuar a leitura.')

# Rodapé Colorido
st.markdown("""
    <style>
    .footer { position: fixed; bottom: 0; width: 100%; text-align: center; color: #8e44ad; }
    </style>
    <div class="footer">Comunicando Igrejas - Levando a Palavra ao Digital</div>
    """, unsafe_allow_html=True)
