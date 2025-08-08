from fastapi import FastAPI, HTTPException
import grpc

# Importar as classes geradas pelo gRPC
import calculator_pb2
import calculator_pb2_grpc

# Inicializa a aplicação FastAPI
app = FastAPI()

# Endereço do nosso microserviço gRPC
GRPC_SERVER_ADDRESS = 'grpc-server:50051'

# Função para se comunicar com o microserviço gRPC
def get_sum_from_microservice(number1: int, number2: int):
    """
    Chama o microserviço gRPC para somar dois números.
    """
    try:
        # Cria um canal de comunicação com o servidor gRPC
        with grpc.insecure_channel(GRPC_SERVER_ADDRESS) as channel:
            # Cria um stub (cliente) para o serviço Calculator
            stub = calculator_pb2_grpc.CalculatorStub(channel)
            
            # Monta a requisição com os números
            request = calculator_pb2.AddRequest(number1=number1, number2=number2)
            
            # Chama o método remoto 'Add' e obtém a resposta
            response = stub.Add(request)
            
            return response.result
    except grpc.RpcError as e:
        # Captura erros de comunicação com o gRPC (ex: serviço offline)
        print(f"Erro ao chamar o serviço gRPC: {e}")
        raise HTTPException(status_code=503, detail="O serviço de cálculo está indisponível.")


# Define o endpoint da API
@app.get("/somar")
def somar_numeros(parcela1: int, parcela2: int):
    """
    Recebe duas parcelas como query parameters, chama o microserviço gRPC
    para somá-las e retorna o resultado.
    
    Exemplo de uso: http://127.0.0.1:8000/somar?parcela1=25&parcela2=25
    """
    # Chama a função que se comunica com o microserviço
    resultado_soma = get_sum_from_microservice(parcela1, parcela2)
    
    # Retorna o resultado em um JSON
    return {
        "parcela1": parcela1,
        "parcela2": parcela2,
        "resultado": resultado_soma
    }

# Endpoint raiz para um teste rápido
@app.get("/")
def read_root():
    return {"message": "API para chamar o microserviço de soma. Use o endpoint /somar."}

# Para executar a API diretamente com `python api.py`
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
