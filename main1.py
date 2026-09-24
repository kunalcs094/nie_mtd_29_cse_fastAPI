from fastapi import FASTAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId

app = FastAPI()
URL="mongodb://127.0.0.1:27017"
client = MongoClient(URL)
db = client["service_ticket_db"]
tickets_collection = db["tickets"]
class Ticket(BaseModel):
    title: str
    description: str
    category: str
    status: str
def ticket_read_all():
    return{
        id: str(ticket["_id"]),
        "title": ticket["title"],
        "description": ticket["description"],
        "category": ticket["category"],
        "status": ticket["status"]
    }
@app.post("/tickets", status_code=201)
def ticket_create(ticket_payload: Ticket):
    ticket_dict = ticket_payload_.model_dump()
    result = tickets_collection.insert_one(ticket_dict)
    new_ticket= tickets_collection.find_one({"_id": result.inserted_id})
    return {"id": str(result.inserted_id), **ticket_dict}
@app.get("/tickets",response_model=list[Ticket])
def ticket_read_all():
    docs = tickets_collection.find()
    tickets = [ticket_helper(doc) for doc in docs]
    return tickets
@app.get("/tickets/{id}",response_model=Ticket)
def ticket_read(id: str):
    ticket = tickets_collection.find_one({"_id": ObjectId(id)})
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    doc=tickets_collection.find_one({"_id": ObjectId(id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket_helper(doc)
@app.put("/tickets/{id}",response_model=Ticket)
def ticket_update(id: str, ticket_payload: Ticket):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ticket ID")
    ticket_dict = ticket_payload.model_dump()
    result = tickets_collection.update_one({"_id": ObjectId(id)}, {"$set": ticket_dict})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Ticket not found")
    updated_ticket = tickets_collection.find_one({"_id": ObjectId(id)})
    return ticket_helper(updated_ticket)
@app.delete("/tickets/{id}")
def ticket_delete(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ticket ID")
    result = tickets_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return {"message": "Ticket deleted successfully"}
