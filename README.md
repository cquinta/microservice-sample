# Microservice Sample — Calculator

Aplicação distribuída com microserviços REST (FastAPI) para operações matemáticas, com observabilidade via OpenTelemetry.

## Arquitetura

```
Cliente HTTP → msapi (8000) → mssum (8002) + mssub (8001)
                                    ↘           ↙
                              OTel Collector (4317)
                              ↙       ↓        ↘
                          Tempo   Prometheus    Loki
                              ↘       ↓        ↙
                                  Grafana (3000)
```

## Estrutura

```
microservice-sample/
├── msapi/                        # API Gateway (FastAPI)
│   └── app/
│       ├── __init__.py
│       ├── main.py
│       ├── config.py
│       └── routers/
│           ├── allops.py
│           └── health.py
├── mssum/                        # Microserviço de soma (FastAPI)
│   └── app/
│       ├── __init__.py
│       ├── main.py
│       ├── test_main.py
│       └── routers/
│           ├── sum.py
│           └── health.py
├── mssub/                        # Microserviço de subtração (FastAPI + OTel)
│   └── app/
│       ├── __init__.py
│       ├── main.py
│       ├── config.py
│       ├── test_main.py
│       └── routers/
│           ├── sub.py
│           └── health.py
├── telemetry-platform-config/    # Configs de observabilidade
│   ├── otel-collector-config.yml
│   ├── loki-config.yml
│   ├── prometheus.yml
│   ├── tempo.yml
│   └── grafana-datasources.yml
├── docker-compose.yml            # Compose (build + telemetria)
├── callapi.sh                    # Script de carga para testes
└── README.md
```

## Execução

### Docker Compose (recomendado)

Sobe todos os microsserviços + stack de observabilidade:

```bash
docker compose up --build
```

### Serviços

| Serviço | Porta | Descrição |
|---------|-------|-----------|
| msapi | 8000 | API Gateway |
| mssub | 8001 | Subtração (instrumentado com OTel) |
| mssum | 8002 | Soma |
| Grafana | 3000 | Dashboards |
| Prometheus | 9090 | Métricas |
| Loki | 3100 | Logs |
| Tempo | 3200 | Traces |
| OTel Collector | 4317/4318 | Coleta de telemetria |

### Local (desenvolvimento)

```bash
# Subtração
cd mssub && uv sync && uv run fastapi dev --port 8001

# Soma
cd mssum && uv sync && uv run fastapi dev --port 8002

# API Gateway
cd msapi && uv sync && uv run fastapi dev
```

## Endpoints

### msapi (Gateway)

**POST /allops** — Executa soma e subtração em paralelo:
```bash
curl -X POST "http://localhost:8000/allops" \
  -H "Content-Type: application/json" \
  -d '{"a": 25, "b": 10}'
```

**GET /health** — Health check

### mssum

**POST /sum**
```bash
curl -X POST "http://localhost:8002/sum" \
  -H "Content-Type: application/json" \
  -d '{"a": 25, "b": 10}'
```

**GET /health** — Health check

### mssub

**POST /sub**
```bash
curl -X POST "http://localhost:8001/sub" \
  -H "Content-Type: application/json" \
  -d '{"a": 25, "b": 10}'
```

**GET /metrics** — Métricas OpenTelemetry no formato Prometheus
```bash
curl http://localhost:8001/metrics
```

**GET /health** — Health check

## Script de carga

Gera requisições contínuas ao gateway para testar a observabilidade:

```bash
./callapi.sh
```

## Observabilidade

O `mssub` está instrumentado com OpenTelemetry exportando:
- **Traces** → OTel Collector → Tempo
- **Métricas** → OTel Collector → Prometheus + endpoint `/metrics`
- **Logs** → OTel Collector → Loki

O OTel Collector também coleta:
- Métricas de infraestrutura dos containers via `docker_stats` receiver
- Métricas do host via `hostmetrics` receiver (CPU, memória, disco)

### Configuração via variáveis de ambiente

| Variável | Default | Descrição |
|----------|---------|-----------|
| `OTEL_HOST` | `otel-collector` | Host do OTel Collector |
| `OTEL_PORT` | `4317` | Porta gRPC do Collector |
| `OTEL_INSECURE` | `true` | Conexão sem TLS |
| `VERSION` | `1.0.0` | Versão da aplicação |
| `SUM_SERVICE_URL` | `http://mssum:80/sum` | URL do serviço de soma |
| `SUB_SERVICE_URL` | `http://mssub:80/sub` | URL do serviço de subtração |

### Grafana

Acesse http://localhost:3000 (login anônimo habilitado).

Datasources pré-configurados:
- Prometheus (métricas)
- Loki (logs)
- Tempo (traces)

### Métricas de containers no Prometheus

As métricas de infraestrutura dos containers estão disponíveis com os seguintes nomes:

| Métrica | Descrição |
|---------|-----------|
| `container_cpu_usage_nanoseconds_total` | CPU total |
| `container_cpu_utilization_ratio` | % de CPU |
| `container_memory_usage_total_bytes` | Memória total |
| `container_memory_percent_ratio` | % de memória |
| `container_network_io_usage_rx_bytes_total` | Rede RX |
| `container_network_io_usage_tx_bytes_total` | Rede TX |

Filtrar por container: `container_cpu_utilization_ratio{container_name="mssub"}`

## Testes

```bash
cd mssub
uv add --dev pytest
uv run pytest -v app/test_main.py
```

```bash
cd mssum
uv add --dev pytest
uv run pytest -v app/test_main.py
```

## Documentação das APIs

- **msapi Swagger**: http://localhost:8000/docs
- **mssub Swagger**: http://localhost:8001/docs
- **mssum Swagger**: http://localhost:8002/docs
