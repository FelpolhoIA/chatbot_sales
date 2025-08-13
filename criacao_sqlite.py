import pandas as pd
from sqlalchemy import create_engine
import os
import sys

DB_FILE = "sales.db"


try:
    engine = create_engine(f"sqlite:///{DB_FILE}")
except Exception as e:
    print(f" Erro ao conectar ao banco SQLite: {e}")
    sys.exit(1)


df = pd.read_csv("sales.csv", sep=';')

df.columns = df.columns.str.strip().str.lower()


df['date'] = pd.to_datetime(df['date'], dayfirst=True).dt.strftime('%Y-%m-%d')
df['actual_quantity'] = pd.to_numeric(df['actual_quantity'], errors='coerce')
df['planned_quantity'] = pd.to_numeric(df['planned_quantity'], errors='coerce')
df['planned_price'] = pd.to_numeric(df['planned_price'], errors='coerce')
df['actual_price'] = pd.to_numeric(df['actual_price'], errors='coerce')
df['flag_preco_invalido'] = ((df['planned_price'] == 0) & (df['actual_price'] == 0))


try:
    df.to_sql("sales", engine, if_exists="replace", index=False)
    print("Dados inseridos no SQLite com sucesso!")
except Exception as e:
    print(f"Erro ao inserir dados no SQLite: {e}")
    sys.exit(1)
