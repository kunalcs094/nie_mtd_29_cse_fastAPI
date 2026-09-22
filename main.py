from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

db = {
    1: {
        "id": 1,
        "title": "Laptop not working",
        "description": "My laptop is not turning on",
        "category": "Hardware",
        "status": "open"
    },
    2: {
        "id": 2,
        "title": "Email not syncing",
        "description": "My emails are not syncing on my phone",
        "category": "Software",
        "status": "open"
    }
}

class Ticket(BaseModel):
    
    title: str
    description: str
    category: str
    status: str
class TicketResponse(Ticket):
      id: int

@app.get("/")
def home():
    return {"message": "Enterprise IT Service Desk"}

@app.get("/tickets")
def ticket_read_all():
    return list(db.values())

@app.get("/tickets/{id}")
def ticket_read(id: int):
    if id not in db:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db[id]
@app.post("/tickets",status_code=201,response_model=TicketResponse)
def ticket_create(ticket_payload: Ticket):
    new_id = max(db.keys()) + 1 
    db[new_id] = {"id": new_id, **ticket_payload.model_dump()}
    return db[new_id]
@app.put("/tickets/{id}",response_model=TicketResponse)
def ticket_update(id: int, ticket_payload: Ticket):
    if id not in db:
        raise HTTPException(status_code=404, detail="Ticket not found")
    db[id].update(ticket_payload.model_dump())
    return db[id]
@app.delete("/tickets/{id}")
def ticket_delete(id: int):
    if id not in db:
        raise HTTPException(status_code=404, detail="Ticket not found")
    del db[id]
    return {"message": "Ticket deleted successfully"}