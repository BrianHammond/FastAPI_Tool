from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from typing import Optional, Dict, List
from pydantic import BaseModel
from redis_cloud import redis_cloud
import json

app = FastAPI(
    title="Employment Management API",
    description="For educational purposes only",
    version="1.0"
)

class Address(BaseModel):
    address_1: Optional[str] = None
    address_2: Optional[str] = None
    country: Optional[str] = None

class Name(BaseModel):
    first_name: str
    middle_name: Optional[str] = None
    last_name: Optional[str] = None

class Data(BaseModel):
    id: str
    name: Name
    age: Optional[int] = None
    title: Optional[str] = None
    address: Address
    misc: Optional[str] = None

@app.get("/", summary="Home Endpoint", description="Returns a simple Hello World message. Can be used as base_url")
def home():
    return HTMLResponse(content="For more information go to <a href='/docs'>docs</a>")

@app.get("/getdata", response_model=Dict[str, List[Data]], description="Leaving the employee_id blank will return all")  # Get Results
def get_data(id: Optional[int] = None):
    if id is not None:  # If ID is provided, return that specific data
        data = redis_cloud.get(f"employee:{id}")
        if data:
            return {"employees": [json.loads(data)]}  # Deserialize the data from Redis and return it as a list
        else:
            raise HTTPException(status_code=404, detail="Data not found")
    else:  # If ID is not provided, return all data as a list under "Employees"
        keys = redis_cloud.keys("employee:*")  # Get all employee keys
        if not keys:
            return {"employees": []}

        employees = []
        for key in keys:
            data = redis_cloud.get(key)
            if data:
                employees.append(json.loads(data))
        return {"employees": employees}

@app.post("/postdata", response_model=Data, description="employee_id needs to be unique as it is used as a key value")  # Post Results
def post_data(data: Data):
    if redis_cloud.exists(f"employee:{data.id}"):
        raise HTTPException(status_code=400, detail="Data already exists")

    redis_cloud.set(f"employee:{data.id}", json.dumps(data.model_dump()))  # Store the Data object as JSON
    return data

@app.put("/putdata/{id}", response_model=Data)  # Update Results
def put_data(id: str, data: Data):
    if not redis_cloud.exists(f"employee:{id}"):
        raise HTTPException(status_code=404, detail="Data not found")

    redis_cloud.set(f"employee:{id}", json.dumps(data.model_dump()))  # Update the data in Redis
    return data

@app.delete("/deletedata/{id}", response_model=Data)  # Delete Results
def delete_data(id: str):
    if not redis_cloud.exists(f"employee:{id}"):
        raise HTTPException(status_code=404, detail="Data not found")

    data = redis_cloud.get(f"employee:{id}")
    redis_cloud.delete(f"employee:{id}")  # Remove the data from Redis
    return json.loads(data)  # Return the deleted data

application = app  # Alias for AWS Elastic Beanstalk