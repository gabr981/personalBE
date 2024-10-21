from fastapi import FastAPI, Depends, HTTPException, APIRouter, Header
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
import os
from dotenv import load_dotenv

#load_dotenv()  # Carica variabili d'ambiente da un file .env
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
API_KEY = os.getenv("API_KEY")

app = FastAPI(root_path="/api")  # Aggiungi root_path

api = APIRouter()




# Connetti a MongoDB
client = AsyncIOMotorClient(MONGO_URL)
db = client.my_database

# Modello per esempio API
class Item(BaseModel):
    name: str
    description: str

# Middleware per l'API Key

@api.get("/test")
async def test_route():
    return "Route di test funzionante"

async def api_key_auth(api_key: str = Header(None)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="API Key non valida")
    return True

@api.get("/items", dependencies=[Depends(api_key_auth)])
async def read_items():
    #items = await db.items.find().to_list(100)
    return "Ciao questo è un test e se mi vedi vuol dire che funziona"



app.include_router(api)