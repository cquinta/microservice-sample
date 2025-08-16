import grpc
from concurrent import futures
import time

# Importar as classes geradas
import calculator_sub_pb2 as calculator_sub_pb2
import calculator_sub_pb2_grpc as calculator_sub_pb2_grpc

# Criar uma classe que herda do servicer gerado e implementa o método Sub
class CalculatorsubServicer(calculator_sub_pb2_grpc.CalculatorsubServicer):
    def Sub(self, request, context):
        # A lógica da sua função: somar os dois números da requisição
        subtracao = request.number1 - request.number2
        print(f"Recebida requisição para somar {request.number1} e {request.number2}. Resultado: {subtracao}")
        # Retornar a resposta no formato da mensagem SubResponse
        return calculator_sub_pb2.SubResponse(result=subtracao)

# Função para iniciar o servidor
def serve():
    # Criar uma instância do servidor gRPC
    #server = grpc.server(futures.ThreadPoolExecutor(max_workers=20))
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=100))

    # Adicionar o servicer ao servidor
    calculator_sub_pb2_grpc.add_CalculatorsubServicer_to_server(CalculatorsubServicer(), server)
    # Definir a porta em que o servidor irá escutar
    print('Iniciando o servidor. Escutando na porta 50052.')
    server.add_insecure_port('[::]:50052')
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