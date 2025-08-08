# FastAPI + gRPC Calculator

Uma aplicação distribuída que demonstra a comunicação entre uma API REST (FastAPI) e um microserviço gRPC para operações de cálculo.

## 📋 Visão Geral

Este projeto implementa uma arquitetura de microserviços com:
- **API Service**: API REST usando FastAPI que expõe endpoints HTTP
- **gRPC Service**: Microserviço gRPC que realiza operações de cálculo
- **Comunicação**: A API REST comunica-se com o microserviço gRPC para processar requisições

## 🏗️ Arquitetura

```
Cliente HTTP → FastAPI (porta 8000) → gRPC Server (porta 50051)
```

## 📁 Estrutura do Projeto

```
fastapi-tutorial/
├── api_service/           # Serviço FastAPI
│   ├── api.py            # Aplicação FastAPI principal
│   ├── calculator_pb2.py # Classes gRPC geradas
│   ├── calculator_pb2_grpc.py
│   ├── requirements.txt  # Dependências da API
│   └── Dockerfile       # Container da API
├── grpc_service/         # Microserviço gRPC
│   ├── server.py        # Servidor gRPC
│   ├── calculator_pb2.py # Classes gRPC geradas
│   ├── calculator_pb2_grpc.py
│   ├── requirements.txt # Dependências do gRPC
│   └── Dockerfile      # Container do gRPC
├── calculator.proto     # Definição do protocolo gRPC
└── client.py           # Cliente de teste
```

## 🚀 Como Executar

### Pré-requisitos

- Python 3.9+
- pip

### Opção 1: Execução Local

1. **Clone o repositório**
   ```bash
   git clone <repository-url>
   cd fastapi-tutorial
   ```

2. **Execute o servidor gRPC**
   ```bash
   cd grpc_service
   pip install -r requirements.txt
   python server.py
   ```

3. **Execute a API FastAPI** (em outro terminal)
   ```bash
   cd api_service
   pip install -r requirements.txt
   python api.py
   ```

### Opção 2: Usando Docker

1. **Construa as imagens**
   ```bash
   # Construir imagem do gRPC
   cd grpc_service
   docker build -t grpc-calculator .
   
   # Construir imagem da API
   cd ../api_service
   docker build -t fastapi-calculator .
   ```

2. **Execute os containers**
   ```bash
   # Executar servidor gRPC
   docker run -d --name grpc-server -p 50051:50051 grpc-calculator
   
   # Executar API FastAPI
   docker run -d --name fastapi-api -p 8000:8000 --link grpc-server fastapi-calculator
   ```

## 📖 Uso da API

### Endpoints Disponíveis

#### `GET /`
Endpoint de teste que retorna informações básicas da API.

**Resposta:**
```json
{
  "message": "API para chamar o microserviço de soma. Use o endpoint /somar."
}
```

#### `GET /somar`
Soma dois números usando o microserviço gRPC.

**Parâmetros:**
- `parcela1` (int): Primeiro número
- `parcela2` (int): Segundo número

**Exemplo de uso:**
```bash
curl "http://127.0.0.1:8000/somar?parcela1=25&parcela2=25"
```

**Resposta:**
```json
{
  "parcela1": 25,
  "parcela2": 25,
  "resultado": 50
}
```

### Documentação Interativa

Acesse a documentação automática do FastAPI:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## 🛠️ Desenvolvimento

### Regenerar Classes gRPC

Se você modificar o arquivo `calculator.proto`, regenere as classes Python:

```bash
python -m grpc_tools.protoc --python_out=. --grpc_python_out=. calculator.proto
```

### Estrutura do Protocolo gRPC

O arquivo `calculator.proto` define:
- **Serviço**: `Calculator` com método `Add`
- **Mensagens**: `AddRequest` e `AddResponse`

## 🔧 Configuração

### Variáveis de Ambiente

- `GRPC_SERVER_ADDRESS`: Endereço do servidor gRPC (padrão: `grpc-server:50051`)

### Dependências

**API Service:**
- fastapi
- uvicorn[standard]
- grpcio
- grpcio-tools

**gRPC Service:**
- grpcio
- grpcio-tools

## 🐛 Tratamento de Erros

A API trata os seguintes cenários de erro:
- **503 Service Unavailable**: Quando o microserviço gRPC está indisponível
- **Validação de parâmetros**: FastAPI valida automaticamente os tipos dos parâmetros

## 🧪 Testes

Execute um teste rápido:

```bash
# Teste o endpoint raiz
curl http://127.0.0.1:8000/

# Teste a soma
curl "http://127.0.0.1:8000/somar?parcela1=10&parcela2=20"
```

## 📝 Próximos Passos

- [ ] Adicionar mais operações matemáticas (subtração, multiplicação, divisão)
- [ ] Implementar autenticação e autorização
- [ ] Adicionar testes unitários e de integração
- [ ] Configurar logging estruturado
- [ ] Implementar health checks
- [ ] Adicionar métricas e monitoramento

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.