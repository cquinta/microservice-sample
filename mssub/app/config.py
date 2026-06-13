import os


class Config:
    OTEL_HOST = os.environ.get("OTEL_HOST", "otel-collector")
    OTEL_PORT = os.environ.get("OTEL_PORT", "4317")
    OTEL_INSECURE = os.environ.get("OTEL_INSECURE", "True")
    VERSION = os.environ.get("VERSION", "1.0.0")
    HOST = os.environ.get("HOSTNAME", "localhost")



