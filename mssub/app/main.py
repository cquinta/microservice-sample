#### Telemetry ####
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from prometheus_client import generate_latest, REGISTRY
from fastapi.responses import Response
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
####

from .config import Config
from .routers import sub
from .routers import health

from fastapi import FastAPI
import logging

OTEL_HOST = Config.OTEL_HOST
OTEL_PORT = Config.OTEL_PORT
OTEL_INSECURE = Config.OTEL_INSECURE


resource = Resource(
    attributes={
        "service.name": "fastapi-service-sub",
        "service.version": "1.0.0",
        "deployment.environment": "dev",
    }
)

provider = TracerProvider(resource=resource)
trace.set_tracer_provider(provider)
otlp_trace_exporter = OTLPSpanExporter(
    endpoint=f"http://{OTEL_HOST}:{OTEL_PORT}", insecure=OTEL_INSECURE
)
span_processor = BatchSpanProcessor(otlp_trace_exporter)
provider.add_span_processor(span_processor)

otlp_metric_exporter = OTLPMetricExporter(
    endpoint=f"http://{OTEL_HOST}:{OTEL_PORT}", insecure=OTEL_INSECURE
)
metric_reader = PeriodicExportingMetricReader(
    otlp_metric_exporter, export_interval_millis=10000
)
prometheus_reader = PrometheusMetricReader()
meter_provider = MeterProvider(
    resource=resource, metric_readers=[metric_reader, prometheus_reader]
)
metrics.set_meter_provider(meter_provider)


logger_provider = LoggerProvider(resource=resource)
set_logger_provider(logger_provider)
otlp_log_exporter = OTLPLogExporter(
    endpoint=f"http://{OTEL_HOST}:{OTEL_PORT}", insecure=OTEL_INSECURE
)
logger_provider.add_log_record_processor(BatchLogRecordProcessor(otlp_log_exporter))
otel_log_handler = LoggingHandler(level=logging.INFO, logger_provider=logger_provider)

logging.basicConfig(level=logging.INFO)
logging.getLogger().addHandler(otel_log_handler)

logger = logging.getLogger("fastapi-service-sub")
logger.setLevel(logging.INFO)


app = FastAPI(title="Sub Microsservice")


@app.get("/metrics")
async def metrics_endpoint():
    return Response(content=generate_latest(REGISTRY), media_type="text/plain")


FastAPIInstrumentor.instrument_app(app)


app.include_router(sub.router)
app.include_router(health.router)


@app.get("/")
async def root():
    return {"message": "Microsserviço de Subtração", "host": Config.HOST, "versão" : Config.VERSION}
