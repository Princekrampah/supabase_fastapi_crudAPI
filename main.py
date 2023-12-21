from fastapi import FastAPI, status
from decouple import config
from supabase import create_client, Client
from pydantic import BaseModel
import random

url = config("SUPERBASE_URL")
key = config("SUPERBASE_KEY")

app = FastAPI()
supabase: Client = create_client(url, key)

@app.get("/todos/")
def get_todos():
    todos = supabase.table("todos").select("*").execute()
    return todos


@app.get("/todos/{id}")
def get_todo(id: int):
    todo = supabase.table("todos").select("*").eq("id", id).execute()
    return todo

class TodoSchema(BaseModel):
    title: str
    description: str

@app.post("/todos/", status_code=status.HTTP_201_CREATED)
def create_todo(todo: TodoSchema):
    id = random.randint(0, 100000000)
    todo = supabase.table("todos").insert({
        "id": id,
        "title": todo.title,
        "description": todo.description 
    }).execute()
    
    return todo

@app.delete("/todos/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(id: str):
    todo =supabase.table("todos").delete().eq("id", id).execute()
    return {"msg": "Deleted"}