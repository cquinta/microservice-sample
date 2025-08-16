from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import grpc

# Importar as classes geradas pelo gRPC
import calculator_soma_pb2 as calculator_soma_pb2
import calculator_soma_pb2_grpc as calculator_soma_pb2_grpc
import calculator_sub_pb2 as calculator_sub_pb2
import calculator_sub_pb2_grpc as calculator_sub_pb2_grpc

# Inicializa a aplicação FastAPI
app = FastAPI()

# Endereço do nosso microserviço gRPC
GRPC_SOMA_SERVER_ADDRESS = 'grpc-server-soma:50051'
GRPC_SUB_SERVER_ADDRESS = 'grpc-server-sub:50052'

# Função para se comunicar com o microserviço gRPC
class CalcRequest(BaseModel):
    """Define o corpo da requisição esperado para o endpoint /somar."""
    parcela1: int
    parcela2: int

def get_sum_from_microservice(number1: int, number2: int):
    """
    Chama o microserviço gRPC para somar dois números.
    """
    try:
        # Cria um canal de comunicação com o servidor gRPC
        with grpc.insecure_channel(GRPC_SOMA_SERVER_ADDRESS) as channel_soma:
            # Cria um stub (cliente) para o serviço Calculator
            stub_soma = calculator_soma_pb2_grpc.CalculatoraddStub(channel_soma)
            
            # Monta a requisição com os números
            request_soma = calculator_soma_pb2.AddRequest(number1=number1, number2=number2)
            
            # Chama o método remoto 'Add' e obtém a resposta
            response_soma = stub_soma.Add(request_soma)
            
            return response_soma.result
    except grpc.RpcError as e:
        details = e.details()
        # Captura erros de comunicação com o gRPC (ex: serviço offline)
        print(f"Erro ao chamar o serviço gRPC_soma: {e}")
        raise HTTPException(status_code=503, detail=details)
    
def get_sub_from_microservice(number1: int, number2: int):
    """
    Chama o microserviço gRPC para subtrair dois números.
    """
    try:
        # Cria um canal de comunicação com o servidor gRPC
        with grpc.insecure_channel(GRPC_SUB_SERVER_ADDRESS) as channel_sub:
            # Cria um stub (cliente) para o serviço Calculator
            stub_sub = calculator_sub_pb2_grpc.CalculatorsubStub(channel_sub)
            
            # Monta a requisição com os números
            request_sub = calculator_sub_pb2.SubRequest(number1=number1, number2=number2)
            
            # Chama o método remoto 'Sub' e obtém a resposta
            #response_sub = stub_sub.Sub(request)
            response_sub = stub_sub.Sub(request_sub)
            
            return response_sub.result
    except grpc.RpcError as e:
        # Captura erros de comunicação com o gRPC (ex: serviço offline)
        print(f"Erro ao chamar o serviço gRPC: {e}")
        raise HTTPException(status_code=503, detail="O serviço de cálculo de subtração está indisponível.")


# Define o endpoint da API
@app.get("/somar")
async def somar_numeros(parcela1: int, parcela2: int):
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

@app.post("/sub")
async def sub_numeros(request_data: CalcRequest):
    """
    Recebe duas parcelas como query parameters, chama o microserviço gRPC
    para somá-las e retorna o resultado.
    
    Exemplo de uso: http://127.0.0.1:8000/sub?parcela1=25&parcela2=25
    """
    # Chama a função que se comunica com o microserviço
    parcela1 = request_data.parcela1
    parcela2 = request_data.parcela2
    resultado_sub = get_sub_from_microservice(parcela1, parcela2)
    
    # Retorna o resultado em um JSON
    return {
        "parcela1": parcela1,
        "parcela2": parcela2,
        "resultado": resultado_sub
    }



@app.post("/all")
async def all_numeros(request_data: CalcRequest):
    """
    Recebe duas parcelas como query parameters, chama o microserviço gRPC
    para somá-las e retorna o resultado.
    
    Exemplo de uso: http://127.0.0.1:8000/sub?parcela1=25&parcela2=25
    """
    # Chama a função que se comunica com o microserviço
    parcela1 = request_data.parcela1
    parcela2 = request_data.parcela2
    resultado_sub = get_sub_from_microservice(parcela1, parcela2)
    resultado_soma = get_sum_from_microservice(parcela1, parcela2)
    
    # Retorna o resultado em um JSON
    return {
        "parcela1": parcela1,
        "parcela2": parcela2,
        "resultado_sub": resultado_sub,
        "resultado_add": resultado_soma

    }


# Endpoint raiz para um teste rápido
@app.get("/")
def read_root():
    return {"message": "API para chamar o microserviço de soma. Use o endpoint /somar."}

# Para executar a API diretamente com `python api.py`
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
