import streamlit as st
import pandas as pd
import sqlite3

# Conectar ao banco de dados SQLIT
conn = sqlite3.connect('C:/Users/Rafael/documents/ProjetoScraping/data/tnikequotes.db')

# Carregar os dados da tabela 'mercadolivre_items'
df = pd.read_sql_query("SELECT * FROM mercadolivre_items", conn)

# Fechar essa conexão com o banco
conn.close()

st.set_page_config(page_title="Promoções do mercado livre", layout="wide")

# Título da aplicação
with st.sidebar:
    st.title("Promoções do mercado livre")
    st.header("⚙️ Settings")
    marcas_unicas = df['brand'].unique()  # Pegando as marcas únicas
    item_selection = st.selectbox("Select a chart type", ("Camisa", "Tênis", 'Short', 'Bermuda'))
    marca_selection = st.multiselect(
        'Selecione as marcas',
        marcas_unicas,
        default=marcas_unicas.tolist()  # Definindo as marcas como selecionadas por padrão
    )

# Filtrando o DataFrame com base na seleção das marcas
df_filtrado = df[df['brand'].isin(marca_selection)]

st.subheader('Informações principais da página')
col1, col2, col3 = st.columns(3)

# Preço médio
avarage_new_price = df_filtrado['new_price'].mean() if not df_filtrado.empty else 0
col1.metric(label="Preço novo médio em R$", value=f"{avarage_new_price:.2f}")

# Desconto médio
avarage_discount = df_filtrado['discount'].mean() if not df_filtrado.empty else 0
col2.metric(label="Desconto médio em %", value=f"{avarage_discount:.2f}")

# Data da consulta
df_filtrado['_data_coleta'] = pd.to_datetime(df_filtrado['_data_coleta'])
datacoletada = df_filtrado['_data_coleta'].iloc[0].date() if not df_filtrado.empty else 'N/A'
datacoletada_str = datacoletada.strftime("%d/%m/%Y") if datacoletada != 'N/A' else 'N/A'
col3.metric(label='Data da coleta', value=datacoletada_str)

st.divider()

# Top 5 tenis com maior desconto
st.subheader('Top 5 maiores descontos')
df_filtrado['link_clicavel'] = df_filtrado.apply(lambda row: f"[{row['name']}]({row['link']})", axis=1)
top5 = df_filtrado.nlargest(5, 'discount')
top5_formatado = [f"{row['name']} - {row['discount']}% - link: {row['link_clicavel']}" for _, row in top5.iterrows()]
for item in top5_formatado:
    st.markdown(item)

st.divider()

# Tenis mais caros
st.subheader('Visão sobre os produtos')
top_names = df_filtrado['name'].value_counts().sort_values(ascending=False)
st.caption('Produtos com mais anúncios')
col1 = st.container()  # Criando um container para o gráfico
col1.bar_chart(top_names)
st.divider()

# Tentando exibir uma tabela ordenada
df_sorted = df_filtrado.sort_values(
    by=["new_price", "discount", "reviews_rating_number", "reviews_amount"], 
    ascending=[True, False, False, False]
)
st.subheader("Tabela Ordenada")
st.dataframe(df_sorted)
st.divider()

# Tabela Analítica
st.subheader('Analítico')
st.write(df_filtrado)

st.divider()
