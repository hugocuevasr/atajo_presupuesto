import os
from datetime import datetime
from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

# Tus credenciales
NOTION_DB_ID = "3d4fe8890dc680698819fb3f7b62fa01"
# Es recomendable pasar el token como variable de entorno por seguridad
NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "TU_TOKEN_SECRET_AQUI")

@app.get("/api/gasto")
def registrar_gasto(concepto: str, importe: float):
    url = "https://api.notion.com/v1/pages"
    
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    
    # Construimos el JSON nativo que Notion exige
    payload = {
        "parent": {"database_id": NOTION_DB_ID},
        "properties": {
            "Concepto": {
                "title": [{"text": {"content": concepto}}]
            },
            "Importe": {
                "number": importe
            },
            "Fecha": {
                "date": {"start": datetime.now().isoformat()}
            }
        }
    }
    
    # Hacemos el POST desde el servidor, aislando a iOS del problema
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return {"status": "éxito", "mensaje": f"{concepto} registrado correctamente."}
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)