# grpc_service/Dockerfile

# 1. Usar uma imagem base oficial do Python
FROM python:3.9-slim

# 2. Definir o diretório de trabalho dentro do container
WORKDIR /app

# 3. Copiar o arquivo de dependências para o container
COPY requirements.txt .

# 4. Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar os arquivos da aplicação para o diretório de trabalho
COPY . .

# 6. Expor a porta que o serviço gRPC usará
EXPOSE 50051

# 7. Definir o comando para iniciar o servidor gRPC quando o container for executado
CMD ["python", "server.py"]