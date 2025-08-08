# api_service/Dockerfile

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

# 6. Expor a porta que a API usará
EXPOSE 8000

# 7. Definir o comando para iniciar a API quando o container for executado
# O host 0.0.0.0 permite que a aplicação seja acessível de fora do container
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]