# Microservice Sample (Mocapp)

Este projeto é um exemplo prático de uma arquitetura de microsserviços construída em Python utilizando o framework **FastAPI**. Ele demonstra a comunicação assíncrona entre serviços, conteinerização com Docker e integração/entrega contínua (CI/CD) com GitHub Actions.

## 🏗️ Arquitetura

O sistema é composto por três microsserviços independentes:

1. **API Gateway / Orquestrador (`msapi`)**: Ponto de entrada principal. Recebe os dados do usuário e faz chamadas assíncronas (via `httpx` e `asyncio`) para os serviços de soma e subtração simultaneamente, agregando os resultados.
2. **Microsserviço de Soma (`mssum`)**: Responsável por receber dois inteiros e retornar a soma.
3. **Microsserviço de Subtração (`mssub`)**: Responsável por receber dois inteiros e retornar a subtração.

## 🚀 Tecnologias Utilizadas

- **Python 3.11**
- **FastAPI** (Framework Web assíncrono e de alta performance)
- **Pydantic** (Validação de dados)
- **HTTPX** (Cliente HTTP assíncrono para comunicação entre microsserviços)
- **Pytest** (Testes unitários e de integração)
- **Docker & Docker Hub** (Conteinerização e registro de imagens)
- **GitHub Actions** (Pipeline de CI/CD)

## 📡 Endpoints

Abaixo estão os detalhes de funcionamento das rotas principais de cada serviço. O payload (corpo da requisição) esperado para todas as operações matemáticas é:
```json
{
  "a": 10,
  "b": 4
}
```

### 1. Gateway de Cálculos (`msapi`)
- **Rota**: `POST /allops`
- **Comportamento**: Envia o payload simultaneamente para `mssum` e `mssub` e retorna o agrupamento das respostas.
- **Variáveis de Ambiente**:
  - `SUM_SERVICE_URL` (Padrão: `http://mssum:80/sum`)
  - `SUB_SERVICE_URL` (Padrão: `http://mssub:80/sub`)

### 2. Serviço de Soma (`mssum`)
- **Rota**: `POST /sum`
- **Retorno Sucesso**: `{"result": 14, "op": "sum"}`

### 3. Serviço de Subtração (`mssub`)
- **Rota**: `POST /sub`
- **Retorno Sucesso**: `{"result": 6, "op": "sub"}`

## 🛠️ Como rodar localmente (Desenvolvimento)

1. Clone o repositório.
2. Crie e ative um ambiente virtual (`.venv`):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # No Linux/Mac
   # .venv\Scripts\activate   # No Windows
   ```
3. Instale as dependências:
   ```bash
   pip install fastapi pydantic httpx uvicorn
   ```
4. Inicie os serviços individualmente (em terminais separados):
   ```bash
   # Iniciando o serviço de soma na porta 8001
   cd mssum && uvicorn app.main:app --port 8001
   
   # Iniciando o serviço de subtração na porta 8002
   cd mssub && uvicorn app.main:app --port 8002
   
   # Iniciando a API principal na porta 8000
   # (Exportando as variáveis para apontar para o localhost)
   export SUM_SERVICE_URL="http://localhost:8001/sum"
   export SUB_SERVICE_URL="http://localhost:8002/sub"
   cd msapi && uvicorn app.main:app --port 8000
   ```

## 🧪 Testes

Os testes foram implementados utilizando o `pytest` juntamente com o `TestClient` do FastAPI.
Para executar os testes de um serviço, por exemplo, o de subtração:

```bash
cd mssub
pip install pytest
pytest -v app/test_main.py
```

## ⚙️ CI/CD (GitHub Actions)

O projeto possui uma pipeline automatizada (`.github/workflows/docker-publish.yml`). Toda vez que há um push para o repositório, o GitHub Actions:
1. Configura um ambiente Python.
2. Roda os testes unitários via `pytest` para os serviços.
3. Se os testes passarem, constrói as imagens Docker (`mocapp-api`, `mocapp-soma` e `mocapp-sub`).
4. Publica as imagens automaticamente no Docker Hub.