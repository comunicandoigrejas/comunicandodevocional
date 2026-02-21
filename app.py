import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 1. Definição da Data (Logo no início para evitar NameError)
data_hoje_str = datetime.now().strftime("%d/%m/%Y")

# 2. Configuração da Página e Estilo
st.set_page_config(page_title="Comunicando Devocional", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: white; }
    h1, h2, h3 { color: #6c5ce7; } /* Roxo */
    .stButton>button { background-color: #ff7675; color: white; border-radius: 10px; } /* Laranja */
    </style>
    """, unsafe_allow_html=True)

# 3. Conexão com a Planilha
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error("Erro na conexão com a planilha. Verifique suas Secrets.")

st.title("📱 Comunicando Devocional")

tab_devocional, tab_leitura = st.tabs(["🙏 Devocional Diário", "📚 Planos de Leitura"])

# --- ABA 1: DEVOCIONAL ---
with tab_devocional:
    try:
        # Lendo a aba Diario
        df_diario = conn.read(worksheet="Diario")
        
        # Filtra na coluna 'Dia' a data de hoje (DD/MM/AAAA)
        # Importante: A coluna na sua planilha deve se chamar exatamente 'Dia'
        dev_hoje = df_diario[df_diario['Dia'].astype(str) == data_hoje_str]
        
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
            st.warning(f"A paz do Senhor, varão! Não encontrei o devocional para hoje ({data_hoje_str}) na aba 'Diario'.")
            st.info("Dica: Verifique se a data na planilha está escrita como texto, ex: 21/02/2026")

    except Exception as e:
        st.error(f"Erro ao carregar devocional: {e}")

# --- ABA 2: LEITURA ---
with tab_leitura:
    st.header("Escolha seu Plano de Leitura")
    try:
        df_leitura = conn.read(worksheet="Leitura")
        lista_planos = df_leitura['Plano'].unique()
        plano_escolhido = st.selectbox("Qual jornada deseja iniciar?", lista_planos)
        
        if st.button("Confirmar Plano"):
            novo_registro = pd.DataFrame([{
                "usuario": "19992148758", 
                "plano": plano_escolhido,
                "dia_atual": 1
            }])
            
            df_progresso = conn.read(worksheet="Progresso")
            df_final = pd.concat([df_progresso, novo_registro], ignore_index=True)
            conn.update(worksheet="Progresso", data=df_final)
            
            st.balloons()
            st.success(f"Glória a Deus! Plano '{plano_escolhido}' registrado!")
    except Exception as e:
        st.error(f"Erro nos Planos: {e}")
