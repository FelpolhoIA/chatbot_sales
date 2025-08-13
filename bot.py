from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy import create_engine
import pandas as pd
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import SystemMessagePromptTemplate
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
import uvicorn
import nest_asyncio
import logging
import os
from dotenv import load_dotenv

app = FastAPI()


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
DB_FILE = os.getenv("DB_FILE")
engine = create_engine(f"sqlite:///{DB_FILE}")



llm = ChatOpenAI(
    temperature=0,
    openai_api_key=api_key,
    model_name="gpt-4o"
)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

system_message = SystemMessagePromptTemplate.from_template("""
Você é um assistente analítico com acesso a um DataFrame chamado `df`.

Regras obrigatórias:
1. Sempre responda em português do Brasil.
2. As colunas disponíveis são:
   - product_id, local, date, planned_quantity, actual_quantity, planned_price, actual_price, promotion_type, service_level, flag_preco_invalido
3. Ignore linhas com flag_preco_invalido == True ao calcular totais ou médias.
4. Mostre sempre o código Python que você executou e depois o resultado.
""")

prompt = ChatPromptTemplate.from_messages([
    system_message,
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])


chat_history = []


def load_df():
    df = pd.read_sql("SELECT * FROM sales", engine)
    df['date'] = pd.to_datetime(df['date'], errors='coerce')  
    df['actual_quantity'] = pd.to_numeric(df['actual_quantity'], errors='coerce')
    df['planned_quantity'] = pd.to_numeric(df['planned_quantity'], errors='coerce')
    df['planned_price'] = pd.to_numeric(df['planned_price'], errors='coerce')
    df['actual_price'] = pd.to_numeric(df['actual_price'], errors='coerce')
    df['flag_preco_invalido'] = df['flag_preco_invalido'].astype(bool)
    df['promotion_type'] = df['promotion_type'].fillna("sem promoção").replace(r'^\s*$', "sem promoção", regex=True)
    return df

def create_agent(df):
    agent = create_pandas_dataframe_agent(
        llm=llm,
        df=df,
        agent_type="openai-tools",
        verbose=True,
        agent_executor_kwargs={
            "memory": memory,
            "prompt": prompt
        },
        allow_dangerous_code=True
    )
    return agent


@app.get("/", response_class=HTMLResponse)
async def index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/history")
async def history():
    return JSONResponse(chat_history)

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message")
    if not user_message:
        return JSONResponse({"response": "Mensagem vazia."})

    df = load_df()
    agent = create_agent(df)
    try:
        result = agent.invoke({"input": user_message})
        bot_response = f"{result.get('output', '')}"
    except Exception as e:
        bot_response = f"Erro ao processar a pergunta: {e}"

    chat_history.append({"user_message": user_message, "bot_response": bot_response})
    return JSONResponse({"response": bot_response})


if __name__ == "__main__":
    nest_asyncio.apply()
    logging.basicConfig(level=logging.INFO)
    uvicorn.run("bot:app", host="127.0.0.1", port=8000, log_level="info")
