# FastAPI + gRPC Calculator

Aplicação distribuída demonstrando comunicação entre API REST (FastAPI) e microserviços gRPC para operações matemáticas.

## Arquitetura

```
Cliente HTTP → FastAPI (8000) → gRPC Soma (50051) + gRPC Subtração (50052)
```

## Estrutura

```
microservice-sample/
├── api_service/              # API FastAPI
│   ├── api.py               # Aplicação principal
│   ├── calculator_*_pb2.py  # Classes gRPC geradas
│   └── requirements.txt
├── grpc_service_soma/       # Microserviço de soma
│   ├── server.py           # Servidor gRPC
│   └── calculator_soma.proto
├── grpc_service_sub/        # Microserviço de subtração
│   ├── server.py           # Servidor gRPC
│   └── calculator_sub.proto
└── client.py               # Cliente de teste
```

## Execução

### Local

1. **Servidor gRPC Soma:**
   ```bash
   cd grpc_service_soma
   pip install -r requirements.txt
   python server.py
   ```

2. **Servidor gRPC Subtração:**
   ```bash
   cd grpc_service_sub
   pip install -r requirements.txt
   python server.py
   ```

3. **API FastAPI:**
   ```bash
   cd api_service
   pip install -r requirements.txt
   python api.py
   ```

### Docker

```bash
# Soma
cd grpc_service_soma
docker build -t grpc-soma .
docker run -d --name grpc-server-soma -p 50051:50051 grpc-soma

# Subtração
cd grpc_service_sub
docker build -t grpc-sub .
docker run -d --name grpc-server-sub -p 50052:50052 grpc-sub

# API
cd api_service
docker build -t fastapi-calc .
docker run -d --name api -p 8000:8000 --link grpc-server-soma --link grpc-server-sub fastapi-calc
```

## Endpoints

### `GET /somar`
```bash
curl "http://127.0.0.1:8000/somar?parcela1=25&parcela2=25"
```

### `POST /sub`
```bash
curl -X POST "http://127.0.0.1:8000/sub" \
  -H "Content-Type: application/json" \
  -d '{"parcela1": 25, "parcela2": 10}'
```

### `POST /all`
```bash
curl -X POST "http://127.0.0.1:8000/all" \
  -H "Content-Type: application/json" \
  -d '{"parcela1": 25, "parcela2": 10}'
```

## Documentação

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## Regenerar gRPC

```bash
python -m grpc_tools.protoc --python_out=. --grpc_python_out=. calculator_soma.proto
python -m grpc_tools.protoc --python_out=. --grpc_python_out=. calculator_sub.proto
```