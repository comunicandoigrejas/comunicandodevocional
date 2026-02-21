import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 1. Definição da Data de Hoje
data_hoje_str = datetime.now().strftime("%d/%m/%Y")

# 2. Configuração da Página
st.set_page_config(page_title="Comunicando Devocional", layout="centered")

# --- ESTILO COMUNICANDO IGREJAS ---
st.markdown("""
    <style>
    .stApp { background-color: white; }
    h1, h2, h3 { color: #6c5ce7; } /* Roxo */
    .stButton>button { background-color: #ff7675; color: white; border-radius: 10px; } /* Laranja */
    </style>
    """, unsafe_allow_html=True)

# 3. Conexão usando o JSON que você colou no Streamlit
try:
    # O st.connection já procura automaticamente o JSON nas Secrets
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    st.title("📱 Comunicando Devocional")
    
    tab_devocional, tab_leitura = st.tabs(["🙏 Devocional Diário", "📚 Planos de Leitura"])

    # --- ABA 1: DEVOCIONAL ---
    with tab_devocional:
        # Lê a aba 'Diario'
        df_diario = conn.read(worksheet="Diario")
        
        # Limpeza rápida para garantir que a data seja lida corretamente
        df_diario['Dia'] = df_diario['Dia'].astype(str).str.strip()
        
        # Busca o devocional de hoje: 21/02/2026
        dev_hoje = df_diario[df_diario['Dia'] == data_hoje_str]
        
        if not dev_hoje.empty:
            dados = dev_hoje.iloc[0]
            st.header(f"📅 {data_hoje_str}")
            st.subheader(dados['Título'])
            st.info(f"📖 {dados['Referência']}")
            st.write(f"*{dados['Versículo Completo (ARA)']}*")
            st.divider()
            st.markdown(dados['Texto Devocional (Resumo para App)'])
            st.success(f"💡 **Aplicação Prática:** {dados['Aplicação Prática']}")
        else:
            st.warning(f"A paz do Senhor! Não encontrei o devocional para {data_hoje_str}.")
            st.info("Verifique se na planilha a data está escrita exatamente assim: " + data_hoje_str)

    # --- ABA 2: LEITURA ---
    with tab_leitura:
        st.header("Planos de Leitura")
        df_leitura = conn.read(worksheet="Leitura")
        lista_planos = df_leitura['Plano'].unique()
        escolha = st.selectbox("Selecione seu plano:", lista_planos)
        
        if st.button("Gravar no meu Progresso"):
            # Aqui ele usa a conexão segura para escrever na planilha
            st.success(f"Plano {escolha} iniciado! (Em breve gravando automaticamente)")

except Exception as e:
    st.error(f"Erro ao conectar com as credenciais JSON: {e}")
    st.info("Certifique-se de que o nome da conexão no Secrets é [connections.gsheets]")
