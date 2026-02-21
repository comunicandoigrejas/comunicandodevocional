import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 1. Definição da Data
data_hoje_str = datetime.now().strftime("%d/%m/%Y")

# 2. Configuração da Página
st.set_page_config(page_title="Comunicando Devocional", layout="centered")

# 3. Conexão com a Planilha (USANDO O LINK DIRETO)
# Varão, substitua o link abaixo pelo link da sua planilha
url_planilha = "https://docs.google.com/spreadsheets/d/1XSVQH3Aka3z51wPP18JvxNjImLVDxyCWUsVACqFcPK0/edit?usp=sharing"

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    # Lendo a aba Diario usando a URL
    df_diario = conn.read(spreadsheet=url_planilha, worksheet="Diario")
    
    st.title("📱 Comunicando Devocional")
    
    # --- ABA 1: DEVOCIONAL ---
    # Convertendo a coluna Dia para string e removendo espaços para não dar erro
    df_diario['Dia'] = df_diario['Dia'].astype(str).str.strip()
    
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
        st.info("Verifique se a data na planilha está exatamente como: " + data_hoje_str)

except Exception as e:
    st.error(f"Erro ao carregar devocional: {e}")
    st.info("Verifique se o link da planilha está correto e se ela está compartilhada como 'Qualquer pessoa com o link'.")
