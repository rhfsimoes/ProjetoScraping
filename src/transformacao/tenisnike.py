# Parte de importações
import pandas as pd
import sqlite3
import datetime

# Definir o caminho para o JSONL
df = pd.read_json('C:/Users/Rafael/documents/ProjetoScraping/data/tnike.jsonl', lines=True)



# Adicionar a coluna _source com valor fixo
df['_source'] = "https://lista.mercadolivre.com.br/tenis-nike-masculino"

# Adicionar a coluna _data_coleta com data e hora atuais
df['_data_coleta'] = datetime.datetime.now()

# Tratar valores nulos para colunas numéricas e de texto

df['old_price_reais'] = df['old_price_reais'].fillna(0).astype(float)
df['old_price_centavos'] = df['old_price_centavos'].fillna(0).astype(float)
df['new_price_reais'] = df['new_price_reais'].fillna(0).astype(float)
df['new_price_centavos'] = df['new_price_centavos'].fillna(0).astype(float)
df['reviews_rating_number'] = df['reviews_rating_number'].fillna(0).astype(float)
df['discount'] = df['discount'].str.replace(r"\D", "", regex=True).fillna(0).astype(float)

# Remover os parenteses do review_amount

df['reviews_amount']= df['reviews_amount'].str.replace('[\(\)]', '', regex=True)
df['reviews_amount']= df['reviews_amount'].fillna(0).astype(int)

# Juntar os prices

df['old_price'] = df['old_price_reais'] + df['old_price_centavos'] / 100
df['new_price'] = df['new_price_reais'] + df['new_price_centavos'] / 100

# Remover as colunas antigas de preços

df.drop(columns=['old_price_reais','old_price_centavos','new_price_reais','new_price_centavos'], inplace=True)

# Conectar no banco de dados

conn = sqlite3.connect('C:/Users/Rafael/documents/ProjetoScraping/data/tnikequotes.db')

# Salvar o Banco de dados

df.to_sql('mercadolivre_items', conn, if_exists='replace',index=False)

# Fechar a conexão com o banco de dados

conn.close()
print(df.head())