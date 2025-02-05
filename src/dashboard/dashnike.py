import streamlit as st
import pandas as pd
import sqlite3

# Conectar ao banco de dados SQLIT
conn =sqlite3.connect('C:/Users/Rafael/documents/ProjetoScraping/data/tnikequotes.db')

# Carregar os dados da tabela 'mercadolivre_items'

df = pd.read_sql_query ("SELECT * FROM mercadolivre_items", conn)

# Fechar essa conexão com o banco

conn.close()

# Título da aplicação

st.title("Pesquisa de Mercado - Tênis da nike no Mercado livre")

# Melhorar Layout com coluna para os KPIs

st.subheader('KPIs principais da página do sistema')
col1, col2, col3 = st.columns(3)


# Preço médio
avarage_new_price = df['new_price'].mean()
col1.metric(label="Preço novo médio em R$", value=f"{avarage_new_price:.2f}")

# Desconto médio
avarage_discount = df['discount'].mean()
col2.metric(label="Desconto médio em %", value=f"{avarage_discount:.2f}")

# Data da consulta
df['_data_coleta'] = pd.to_datetime(df['_data_coleta'])
datacoletada = df['_data_coleta'].iloc[0].date()
datacoletada_str = datacoletada.strftime("%d/%m/%Y")
col3.metric(label='Data da coleta', value = datacoletada_str)

st.divider()

# top 3 tenis com maior desconto
# Criando lista formatada de nome + desconto
top3 = df.nlargest(3, 'discount')
top3_formatado = [f"{row['name']} - {row['discount']}%" for _, row in top3.iterrows()]

# Exibir no Streamlit
st.write("Top 3 maiores descontos:")
st.write("\n".join(top3_formatado))
st.divider()

# tenis mais caros
st.subheader('Visão sobre os produtos')
top_names = df['name'].value_counts().sort_values(ascending=False)
st.caption('Produtos com mais anúncios')
col1 = st.container()  # Criando um container para o gráfico
col1.bar_chart(top_names)
st.divider()

# tentando exibir uma tabela ordenada
df_sorted = df.sort_values(
    by=["new_price", "discount", "reviews_rating_number", "reviews_amount"], 
    ascending=[True, False, False, False])
st.subheader("Tabela Ordenada")
st.dataframe(df_sorted)
st.divider()

# Tabela Analítica
st.subheader('Analítico')
st.write(df)

st.divider()
