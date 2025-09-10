# Http Requests
# GET, POST, PUT, DELETE
# HTTP Requests
# FastAPI, Pydantic, Uvicorn

from fastapi import FastAPI, status, Path, HTTPException
from typing import Optional
from pydantic import BaseModel, Field

app = FastAPI()

users = {
    1: {
        "name": "Ratan",
        "age": 25,
        "role": "Data Scientist"
        },
    4: {
        "name": "John",
        "age": 30,
        "role": "Developer"
        },
    5: {
        "name": "Jane",
        "age": 28,
        "role": "Designer"
        }
}



class User(BaseModel):
    name:str
    age:int
    role:str  
    
class UpdateUser(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    role: Optional[str] = None
    
    
# endpoint is a url
@app.get("/")
def root():
    return {"message": "9/9/9[2025] - Welcome to FastAPI"}

#get users
@app.get("/users/{user_id}")
def get_users(user_id: int = Path(..., description ="The ID of the user you want to get", gt =0, lt=100)):
    if user_id not in users:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "User not found!")
    
    return users[user_id] 

#create user
@app.post("/users/{user_id}", status_code = status.HTTP_201_CREATED)
def create_user(user_id: int, user:User):
    if user_id in users:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "User already exists!")
    users[user_id] = user.dict()
    return user
    
    
#update a user
@app.put("/users/{user_id}")
def update_user(user_id:int, user:UpdateUser):
    if user_id not in users:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "User not found!")
    
    current_user = users[user_id]
    if user.name != None:
        current_user["name"] = user.name
    if user.age != None:
        current_user["age"] = user.age
    if user.role != None:
        current_user["role"] = user.role
    
    return users[user_id]

#delete a user
@app.delete("/users/{user_id}")
def delete_user(user_id:int):
    if user_id not in users:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "User not found!")
    deleted_user =  users.pop(user_id)
    
    return {"message": "User has been  deleted successfully!", "deleted_user": deleted_user}


    
# search user 
@app.get("/users/search/")
def search_user(name:Optional[str]=None):
    if not name:
        return {"message": "Name parameter is required!"}

    
    for user in users.values():
        if user["name"].lower()== name.lower():
            return user
    raise HTTPException(staus_code = 404, detail = "user not found error")