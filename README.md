# Chatbot Sales

Um chatbot de vendas construído com **FastAPI**, **LangChain**, e **OpenAI**, que processa dados com **Pandas** e utiliza **SQLAlchemy** para integração com bancos de dados tornando a aplicação mais escalável e realista.

## Funcionalidades

- Responde perguntas de vendas usando dados de planilhas e bancos de dados.
- Integração com **OpenAI** para geração de respostas inteligentes.
- Interface web simples com FastAPI (não levar em consideração kkk).
- Gerenciamento de conversas com memória usando LangChain.

## Tecnologias Utilizadas

- Python 3.11+
- FastAPI
- Pandas
- SQLAlchemy
- LangChain (agents, memory, prompts)
- OpenAI API
- Uvicorn
- Nest AsyncIO
- Dotenv para variáveis de ambiente

## Instalação

1. Clone o repositório:

```bash
git clone https://github.com/FelpolhoIA/chatbot_sales.git
cd chatbot_sales

2. Crie um arquivo .env com suas credenciais, por exemplo:
OPENAI_API_KEY=...
DB_FILE=...

3. instale dependências:
pip install -r requirements.txt


## Execução com Dockerfile

1. **Construir a imagem:**
```bash
docker build -t chatbot_sales

2. **Rodar Container:**
docker run -p 8000:8000 --env-file .env chatbot_sales

3. **Acessar Aplicação:**
http://localhost:8000

## Estrutura:
chatbot_sales/
├─ bot.py  # Arquivo principal 
├─ criacao_sqlite.py  # Script para criar o banco
├─ dockerfile  # Dockerfile
├─ index.html # interface web 
├─ requirements.txt # Dependências do projeto
├─ sales.csv # CSV de dados de vendas
├─ sales.db # Banco de dados com as informações do CSV
