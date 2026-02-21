import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Conexão com a Planilha
conn = st.connection("gsheets", type=GSheetsConnection)

# --- ESTILO ---
st.markdown("""
    <style>
    .stApp { background-color: white; }
    h1, h2, h3 { color: #6c5ce7; } /* Roxo */
    .stButton>button { background-color: #ff7675; color: white; border-radius: 10px; } /* Laranja */
    </style>
    """, unsafe_allow_html=True)

st.title("📱 Comunicando Devocional")

tab_devocional, tab_leitura = st.tabs(["🙏 Devocional Diário", "📚 Planos de Leitura"])

# 1. ABA DEVOCIONAL (Busca por Data Completa DD/MM/AAAA)
with tab_devocional:
    try:
        df_diario = conn.read(worksheet="Diario")
        
        # AJUSTE DA DATA: Transforma a data de hoje em texto '21/02/2026'
        data_hoje_str = datetime.now().strftime("%d/%m/%Y")
        
        # Filtra na coluna 'Dia' o texto igual a data de hoje
        dados_dia = df_diario[df_diario['Dia'] == data_hoje_str].iloc[0]
        
        st.header(f"📅 {data_hoje_str}")
        st.subheader(dados_dia['Título'])
        st.info(f"📖 {dados_dia['Referência']}")
        st.write(f"*{dados_dia['Versículo Completo (ARA)']}*")
        st.divider()
        st.markdown(dados_dia['Texto Devocional (Resumo para App)'])
        st.success(f"💡 **Aplicação Prática:** {dados_dia['Aplicação Prática']}")
        
    except Exception as e:
        st.warning(f"A paz do Senhor! Não encontrei o devocional para a data {data_hoje_str}. Verifique se a coluna 'Dia' está como texto e no formato DD/MM/AAAA.")

# 2. ABA LEITURA (Registro de Progresso)
with tab_leitura:
    st.header("Escolha seu Plano de Leitura")
    try:
        df_leitura = conn.read(worksheet="Leitura")
        lista_planos = df_leitura['Plano'].unique()
        plano_escolhido = st.selectbox("Qual jornada deseja iniciar?", lista_planos)
        
        if st.button("Confirmar Plano"):
            # Registro na aba 'Progresso'
            novo_registro = pd.DataFrame([{
                "usuario": "19992148758", # Telefone do irmão Willian
                "plano": plano_escolhido,
                "dia_atual": 1
            }])
            
            df_progresso = conn.read(worksheet="Progresso")
            df_final = pd.concat([df_progresso, novo_registro], ignore_index=True)
            conn.update(worksheet="Progresso", data=df_final)
            
            st.balloons()
            st.success(f"Benção pura! Plano '{plano_escolhido}' registado com sucesso!")
    except Exception as e:
        st.error(f"Erro nos Planos: {e}")
