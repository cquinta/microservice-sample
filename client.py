import grpc

# Importar as classes geradas
import calculator_pb2
import calculator_pb2_grpc

def run():
    # Abrir um canal de comunicação com o servidor
    with grpc.insecure_channel('localhost:50051') as channel:
        # Criar um stub (cliente)
        stub = calculator_pb2_grpc.CalculatorStub(channel)
        
        # Criar a requisição com os números que você quer somar
        numero1 = 15
        numero2 = 10
        request = calculator_pb2.AddRequest(number1=numero1, number2=numero2)
        
        # Chamar o método Add do servidor
        response = stub.Add(request)
        
        # Imprimir o resultado
        print(f"A soma de {numero1} e {numero2} é: {response.result}")

if __name__ == '__main__':
    run()