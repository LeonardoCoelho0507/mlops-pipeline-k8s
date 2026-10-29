import os
import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score

# Configuração local para o Python (Host) conseguir empurrar o modelo (Artifact) para o Azurite
os.environ["AZURE_STORAGE_CONNECTION_STRING"] = (
    "DefaultEndpointsProtocol=http;"
    "AccountName=devstoreaccount1;"
    "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
    "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
)

def main():
    # 1. Configurar o experimento
    experiment_name = "iris-classification"
    mlflow.set_experiment(experiment_name)
    
    # Inicia a gravação da Run
    with mlflow.start_run() as run:
        print(f"🚀 Iniciando Run ID: {run.info.run_id}")
        
        # 2. Carregar e preparar dados
        data = load_iris()
        X_train, X_test, y_train, y_test = train_test_split(
            data.data, data.target, test_size=0.2, random_state=42
        )
        
        # 3. Definir hiperparâmetros
        n_estimators = 100
        max_depth = 5
        
        # Registrar hiperparâmetros no MLflow (Vai para o Postgres)
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("max_depth", max_depth)
        
        # 4. Treinar o modelo
        print("Treinando modelo RandomForest...")
        clf = RandomForestClassifier(
            n_estimators=n_estimators, 
            max_depth=max_depth, 
            random_state=42
        )
        clf.fit(X_train, y_train)
        
        # 5. Avaliar e registrar métricas
        y_pred = clf.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average="weighted")
        
        # Registrar métricas no MLflow (Vai para o Postgres)
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("f1_score", f1)
        
        # 6. Salvar o modelo empacotado (Vai para o Azurite / Blob Storage)
        # O MLflow detecta automaticamente as dependências do modelo
        mlflow.sklearn.log_model(clf, "random_forest_model")
        
        print("-" * 40)
        print(f"✅ Treino concluído!")
        print(f"📊 Acurácia: {accuracy:.4f} | F1-Score: {f1:.4f}")
        print(f"📦 Artefato salvo em: {mlflow.get_artifact_uri()}")
        print("-" * 40)

if __name__ == "__main__":
    main()