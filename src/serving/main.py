import os
import mlflow
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="MLOps Inference API")

# Conexão com o nosso "Azure Blob Storage" local
os.environ["AZURE_STORAGE_CONNECTION_STRING"] = (
    "DefaultEndpointsProtocol=http;"
    "AccountName=devstoreaccount1;"
    "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
    "BlobEndpoint=http://azurite:10000/devstoreaccount1;"
)

class PredictRequest(BaseModel):
    features: List[List[float]]

model = None

@app.on_event("startup")
def load_model():
    global model
    run_id = os.getenv("MODEL_RUN_ID")
    if not run_id:
        raise ValueError("Variável MODEL_RUN_ID não definida.")
    
    print(f"Descarregando o modelo do Run ID: {run_id}...")
    try:
        model = mlflow.sklearn.load_model(f"runs:/{run_id}/random_forest_model")
        print("Modelo carregado com sucesso!")
    except Exception as e:
        print(f"Erro ao carregar o modelo: {e}")

@app.get("/health")
def health_check():
    if model is None:
        raise HTTPException(status_code=503, detail="Modelo não carregado")
    return {"status": "healthy", "run_id": os.getenv("MODEL_RUN_ID")}

@app.post("/predict")
def predict(request: PredictRequest):
    if model is None:
        raise HTTPException(status_code=503, detail="Modelo indisponível")
    predictions = model.predict(request.features)
    return {"predictions": predictions.tolist()}