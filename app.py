# Código do novo app.py com GPT integrado para gerar insights

app_with_gpt = """
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import openai

# CONFIGURAÇÕES INICIAIS
st.set_page_config(page_title="Radar Nocap", layout="wide")
st.title("📍 Radar de Trigger Cities - Nocap")

# CHAVE OPENAI
openai.api_key = st.secrets["OPENAI_API_KEY"]

# CARREGAR DADOS
df = pd.read_csv("tabela_dados_plataformas_trigger.csv")
cidades_df = pd.read_csv("tabela_cidades_com_latlong.csv")
merged_df = pd.merge(df, cidades_df, left_on='cidade_id', right_on='id')

# MAPA
st.subheader("🌍 Mapa de Crescimento")
m = folium.Map(location=[-14.2350, -51.9253], zoom_start=4)
for _, row in merged_df.iterrows():
    if pd.notnull(row["Latitude"]) and pd.notnull(row["Longitude"]):
        folium.CircleMarker(
            location=[row["Latitude"], row["Longitude"]],
            radius=row["taxa_crescimento"] / 2,
            popup=f"{row['nome']} | {row['plataforma']} | Crescimento: {row['taxa_crescimento']}%",
            color="red" if row["taxa_crescimento"] > 20 else "blue",
            fill=True,
            fill_opacity=0.6
        ).add_to(m)
folium_static(m)

# INSIGHTS COM GPT
st.subheader("🔎 Geração de Insights por Cidade")

# Selecionar cidade para análise
cidades_unicas = merged_df["nome"].unique()
cidade_escolhida = st.selectbox("Escolha uma cidade para analisar:", cidades_unicas)

# Filtrar os dados da cidade escolhida
cidade_data = merged_df[merged_df["nome"] == cidade_escolhida].iloc[0]
cidade = cidade_data["nome"]
crescimento = cidade_data["taxa_crescimento"]
plataforma = cidade_data["plataforma"]
artistas = cidade_data["artistas_em_alta"]

# Botão para gerar insight
if st.button("Gerar Insight com IA"):
    prompt = f\"\"\"
    Cidade: {cidade}
    Crescimento: {crescimento}%
    Plataforma destaque: {plataforma}
    Artistas em alta: {artistas}

    Gere uma análise no estilo Nocap, com linguagem direta, urbana e provocativa. A ideia é ajudar um artista independente a tomar uma ação estratégica nessa cidade, com base nesses dados. Dê 2 ou 3 sugestões práticas.
    \"\"\"

    resposta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    insight = resposta["choices"][0]["message"]["content"]
    st.markdown("### 💡 Insight Gerado pela IA:")
    st.write(insight)
"""

# Salvar novo app.py
app_with_gpt_path = "/mnt/data/app.py"
with open(app_with_gpt_path, "w") as f:
    f.write(app_with_gpt)

app_with_gpt_path
