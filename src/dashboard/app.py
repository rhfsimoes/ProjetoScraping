import streamlit as st
import pandas as pd
import sqlite3

# Conectar ao banco de dados SQLIT
conn =sqlite3.connect('../data/quotes.db')

# Carregar os dados da tabela 'mercadolivre_items'

df = pd.read_sql_query ("SELECT * FROM mercadolivre_items", conn)

# Fechar essa conexão com o banco

conn.close()

# Título da aplicação

st.title("Pesquisa de Mercado - Tênis esportivo no Mercado livre")

# Melhorar Layout com coluna para os KPIs

st.subheader('KPIs principais da página do sistema')
col1, col2, col3 = st.columns(3)

# KPI 1: Número total de itens
total_itens = df.shape[0]
col1.metric(label="Número total de itens", value=total_itens)

st.write(df)

# KPI 2: Número de marcas únicas

unique_brands = df['brand'].nunique()
col2.metric(label="Número de marcas distintas", value=unique_brands)

# KPI 3: Preço médio novo (em reais)

avarage_new_price = df['new_price'].mean()
col3.metric(label="Preço novo médio em R$", value=f"{avarage_new_price:.2f}")

# Marcas que mais aparecem
st.subheader('Marcas que mais aparecem')
col1,col2 = st.columns([4,2])
top_brands = df['brand'].value_counts().sort_values(ascending=False)
col1.bar_chart(top_brands)
col2.write(top_brands)

# Preço médio por marca
col1,col2 = st.columns([4,2])
df_non_zero_price = df[df['new_price'] > 0]
mean_new_prices = df_non_zero_price.groupby('brand')['new_price'].mean().sort_values(ascending=False)
col1.bar_chart(mean_new_prices)
col2.write(mean_new_prices)

# Satisfação com a marca
col1,col2 = st.columns([4,2])
df_non_zero_reviews = df[df['reviews_rating_number']>0]
satisfaction_by_brand = df_non_zero_reviews.groupby('brand')['reviews_rating_number'].mean().sort_values(ascending=False)
col1.bar_chart(satisfaction_by_brand)
col2.write(satisfaction_by_brand)