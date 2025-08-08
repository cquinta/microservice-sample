import grpc
from concurrent import futures
import time

# Importar as classes geradas
import calculator_pb2
import calculator_pb2_grpc

# Criar uma classe que herda do servicer gerado e implementa o método Add
class CalculatorServicer(calculator_pb2_grpc.CalculatorServicer):
    def Add(self, request, context):
        # A lógica da sua função: somar os dois números da requisição
        soma = request.number1 + request.number2
        print(f"Recebida requisição para somar {request.number1} e {request.number2}. Resultado: {soma}")
        # Retornar a resposta no formato da mensagem AddResponse
        return calculator_pb2.AddResponse(result=soma)

# Função para iniciar o servidor
def serve():
    # Criar uma instância do servidor gRPC
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # Adicionar o servicer ao servidor
    calculator_pb2_grpc.add_CalculatorServicer_to_server(CalculatorServicer(), server)
    # Definir a porta em que o servidor irá escutar
    print('Iniciando o servidor. Escutando na porta 50051.')
    server.add_insecure_port('[::]:50051')
    # Iniciar o servidor
    server.start()
    # Manter o servidor rodando
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()