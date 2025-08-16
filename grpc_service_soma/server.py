# server.py

import grpc
from concurrent import futures
import time

# Importa as classes geradas pelo compilador do protocol buffer
import calculator_soma_pb2
import calculator_soma_pb2_grpc

# 1. CRIAR A CLASSE DO SERVIÇO (SERVICER)
#    Esta classe herda do servicer gerado e implementa os métodos RPC.
class CalculatorServicer(calculator_soma_pb2_grpc.CalculatoraddServicer):
    """
    Implementa a lógica do serviço Calculatoradd definido no .proto.
    """

    # O nome do método (Add) deve ser exatamente o mesmo definido no .proto
    def Add(self, request, context):
        """
        Implementa a lógica do método RPC Add.
        Recebe um objeto 'request' (do tipo AddRequest) e o 'context' da chamada.
        """
        print(f"Requisição recebida: somar {request.number1} + {request.number2}")

        # Realiza a lógica de negócio (neste caso, uma simples soma)
        soma_resultado = request.number1 + request.number2

        # Retorna um objeto de resposta (do tipo AddResponse)
        # O nome do campo (result) também deve ser o mesmo do .proto
        return calculator_soma_pb2.AddResponse(result=soma_resultado)


# 2. FUNÇÃO PARA INICIAR O SERVIDOR
def serve():
    """
    Inicializa e executa o servidor gRPC.
    """
    # Cria uma instância do servidor gRPC com um pool de 10 threads.
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=100))

    # Adiciona a nossa classe Servicer ao servidor.
    # Isso registra nossa implementação para que o servidor saiba como lidar com as requisições.
    calculator_soma_pb2_grpc.add_CalculatoraddServicer_to_server(
        CalculatorServicer(), server
    )

    # Define a porta em que o servidor irá escutar.
    # '[::]:50051' significa que ele irá escutar em todas as interfaces de rede disponíveis (IPv4 e IPv6).
    # 50051 é uma porta comumente usada para gRPC como exemplo.
    port = "50051"
    server.add_insecure_port("[::]:" + port)

    # Inicia o servidor. Esta chamada não bloqueia a execução.
    server.start()
    print(f"Servidor gRPC iniciado e escutando na porta {port}...")

    # Mantém o servidor rodando indefinidamente.
    # O servidor irá esperar por requisições até que o processo seja encerrado.
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        # Permite encerrar o servidor de forma limpa com Ctrl+C
        print("Encerrando o servidor...")
        server.stop(0)


# Ponto de entrada do script
if __name__ == "__main__":
    serve()