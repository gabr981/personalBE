from fastapi import FastAPI, Depends, HTTPException
from fastapi import Header, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()  # Carica variabili d'ambiente da un file .env
MONGO_URL=os.getenv("MONGO_URL", "mongodb://localhost:27017")

app = FastAPI()

# Connetti a MongoDB
client = AsyncIOMotorClient(MONGO_URL)
db = client.my_database

# Modello per esempio API
class Item(BaseModel):
    name: str
    description: str

# Middleware per l'API Key

async def api_key_auth(api_key: str = Header(None)):
    if api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=403, detail="API Key non valida")
    return True

@app.get("/api/items/", dependencies=[Depends(api_key_auth)])
async def read_items():
    #items = await db.items.find().to_list(100)
    return "items"

@app.post("/api/item/", dependencies=[Depends(api_key_auth)])
async def create_item(item: Item):
    result = await db.items.insert_one(item.dict())
    return {"id": str(result.inserted_id)}