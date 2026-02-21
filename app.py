import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Configuração da Página
st.set_page_config(page_title="Comunicando Devocional", layout="centered")

# Conexão com a Planilha (Corrigida)
conn = st.connection("gsheets", type=GSheetsConnection)

# --- ESTILO ---
st.markdown("""
    <style>
    .stApp { background-color: white; }
    h1, h2, h3 { color: #6c5ce7; } /* Roxo */
    .stButton>button { background-color: #ff7675; color: white; border-radius: 10px; } /* Laranja */
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE LOGIN (Baseada na sua imagem de Usuários) ---
# Usando o seu número como exemplo de sessão ativa
if 'user_tel' not in st.session_state:
    st.session_state['user_tel'] = "19992148758" 

st.title("📱 Comunicando Devocional")

tab_devocional, tab_leitura = st.tabs(["🙏 Devocional Diário", "📚 Planos de Leitura"])

# 1. ABA DEVOCIONAL (Busca na aba 'Diario')
with tab_devocional:
    try:
        df_diario = conn.read(worksheet="Diario")
        dia_hoje = datetime.now().day
        dados_dia = df_diario[df_diario['dia'] == dia_hoje].iloc[0]
        
        st.header(f"Dia {dia_hoje} - {dados_dia['titulo']}")
        st.subheader(f"📖 {dados_dia['referencia']}")
        st.info(f"*{dados_dia['versiculo_completo']}*")
        st.write(dados_dia['texto_devocional'])
        st.success(f"💡 **Aplicação:** {dados_dia['aplicacao_pratica']}")
    except Exception:
        st.warning("Abençoado, verifique se o devocional de hoje está preenchido na aba 'Diario'.")

# 2. ABA LEITURA (Integração abas 'Leitura' e 'Progresso')
with tab_leitura:
    st.header("Escolha o seu Plano de Leitura")
    try:
        # Lê a aba 'Leitura' (Colunas: Plano, Dia, Referência, Resumo)
        df_leitura = conn.read(worksheet="Leitura")
        lista_planos = df_leitura['Plano'].unique()
        
        plano_escolhido = st.selectbox("Qual jornada deseja iniciar?", lista_planos)
        
        if st.button("Iniciar Plano"):
            # Salva na aba 'Progresso' (Colunas: usuario, plano, dia_atual)
            novo_registro = pd.DataFrame([{
                "usuario": st.session_state['user_tel'],
                "plano": plano_escolhido,
                "dia_atual": 1
            }])
            
            # Adiciona à planilha existente
            df_progresso = conn.read(worksheet="Progresso")
            df_final = pd.concat([df_progresso, novo_registro], ignore_index=True)
            conn.update(worksheet="Progresso", data=df_final)
            
            st.balloons()
            st.success(f"Glória a Deus! Plano '{plano_escolhido}' registado na aba Progresso.")
            
        st.divider()
        st.subheader("Conteúdo do Plano")
        detalhes = df_leitura[df_leitura['Plano'] == plano_escolhido]
        st.table(detalhes[['Dia', 'Referência', 'Resumo para Meditação']])
        
    except Exception as e:
        st.error(f"Erro ao carregar os planos: {e}")
