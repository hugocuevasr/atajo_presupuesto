import os
import time
from datetime import datetime
from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

NOTION_DB_ID = "3d4fe8890dc680698819fb3f7b62fa01"
NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "TU_TOKEN_SECRET_AQUI")

ultimo_gasto = {"tiempo": 0, "concepto": "", "importe": 0}

@app.get("/api/gasto")
def registrar_gasto(concepto: str, importe: float):
    global ultimo_gasto
    ahora = time.time()
    
    # ANTI-REBOTE: Si es el mismo gasto en menos de 10 segundos, lo interrumpimos
    if (ahora - ultimo_gasto["tiempo"] < 10 and 
        ultimo_gasto["concepto"] == concepto and 
        ultimo_gasto["importe"] == importe):
        return {"status": "ignorado", "mensaje": "Duplicado fantasma de iOS interceptado."}
        
    # Si es un gasto nuevo, actualizamos la memoria
    ultimo_gasto = {"tiempo": ahora, "concepto": concepto, "importe": importe}
    
    # ---- A partir de aquí, el código de Notion normal ----
    url = "https://api.notion.com/v1/pages"
    
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    
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
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return {"status": "éxito", "mensaje": f"{concepto} registrado correctamente."}
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)