import streamlit as st
import datetime

# Configurações da Página
st.set_page_config(page_title="Devocional Comunicando Igrejas", page_icon="📖")

# Customização de Cores (CSS)
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { background-color: #6c5ce7; color: white; border-radius: 10px; }
    .title-text { color: #2e86de; font-weight: bold; }
    .sidebar-text { color: #d35400; }
    </style>
    """, unsafe_allow_html=True)

# Título Principal
st.markdown("<h1 class='title-text'>📖 Devocional Comunicando Igrejas</h1>", unsafe_allow_html=True)
st.write(f"Bem-vindo, varão! Hoje é dia {datetime.date.today().strftime('%d/%m/%Y')}. Que a paz do Senhor esteja contigo.")

# --- MENU LATERAL ---
st.sidebar.header("🙏 Menu de Edificação")
plano_selecionado = st.sidebar.selectbox(
    "Escolha seu Plano de Leitura:",
    ["Devocional Diário", "Bíblia em 1 Ano (ARA)", "Bíblia Cronológica", "Antigo Testamento", "Novo Testamento", "Casais (30 dias)", "Jovens (90 dias)"]
)

st.sidebar.markdown("---")
st.sidebar.info("Projeto: Comunicando Igrejas\nVersão Bíblica: ARA")

# --- CONTEÚDO DINÂMICO ---

if plano_selecionado == "Devocional Diário":
    st.subheader("🔥 Palavra do Dia")
    st.warning("**Versículo:** 'Lâmpada para os meus pés é tua palavra e luz, para o meu caminho.' — Salmos 119:105 (ARA)")
    
    col1, col2 = st.columns(2)
    with col1:
        st.success("✅ **Reflexão:** A Palavra é o mapa do cristão. Sem ela, tropeçamos nas trevas deste mundo.")
    with col2:
        st.info("🙏 **Oração:** Peça ao Senhor discernimento para as decisões de hoje.")

elif plano_selecionado == "Casais (30 dias)":
    st.subheader("💍 Plano para Casais Abençoados")
    dia = st.slider("Selecione o dia da jornada:", 1, 30, 1)
    st.write(f"**Dia {dia}:** Leitura sugerida em Efésios 5.")
    st.progress(dia / 30)
    st.checkbox("Concluí a leitura de hoje!")

elif plano_selecionado == "Bíblia em 1 Ano (ARA)":
    st.subheader("📜 Percorrendo as Escrituras")
    st.write("Siga o cronograma para ler toda a Bíblia este ano.")
    # Exemplo de tabela de leitura
    st.table({
        "Data": ["Hoje", "Amanhã"],
        "Leitura": ["Gênesis 1-3", "Gênesis 4-6"],
        "Status": ["Pendente", "Pendente"]
    })

# --- RODAPÉ ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: #16a085;'>Feito para a glória de Deus pelo Comunicando Igrejas</p>", unsafe_allow_html=True)
