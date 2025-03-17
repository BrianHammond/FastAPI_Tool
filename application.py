from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from typing import Optional, Dict, List
from pydantic import BaseModel
import redis
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
    employee_id: int
    name: Name
    age: Optional[int] = None
    title: Optional[str] = None
    address: Address
    misc: Optional[str] = None

# Connect to Redis Cloud (replace this whole section with the code provided by redis)
r = redis.Redis(
    host='redis-16921.c290.ap-northeast-1-2.ec2.redns.redis-cloud.com',
    port=16921,
    decode_responses=True,
    username="default",
    password="3CVeV4kwwj17Mt62T15lWlaJtIJRAOlr",
)

@app.get("/", summary="Home Endpoint", description="Returns a simple Hello World message. Can be used as base_url")
def home():
    return HTMLResponse(content="For more information go to <a href='/docs'>docs</a>")

@app.get("/getdata", response_model=Dict[str, List[Data]], description="Leaving the employee_id blank will return all")  # Get Results
def get_data(employee_id: Optional[int] = None):
    if employee_id is not None:  # If ID is provided, return that specific data
        data = r.get(f"employee:{employee_id}")
        if data:
            return {"employees": [json.loads(data)]}  # Deserialize the data from Redis and return it as a list
        else:
            raise HTTPException(status_code=404, detail="Data not found")
    else:  # If ID is not provided, return all data as a list under "Employees"
        keys = r.keys("employee:*")  # Get all employee keys
        if not keys:
            return {"employees": []}

        employees = []
        for key in keys:
            data = r.get(key)
            if data:
                employees.append(json.loads(data))
        return {"employees": employees}

@app.post("/postdata", response_model=Data, description="employee_id needs to be unique as it is used as a key value")  # Post Results
def post_data(data: Data):
    if r.exists(f"employee:{data.employee_id}"):
        raise HTTPException(status_code=400, detail="Data already exists")

    r.set(f"employee:{data.employee_id}", json.dumps(data.dict()))  # Store the Data object as JSON
    return data

@app.put("/putdata/{employee_id}", response_model=Data)  # Update Results
def put_data(employee_id: int, data: Data):
    if not r.exists(f"employee:{employee_id}"):
        raise HTTPException(status_code=404, detail="Data not found")

    r.set(f"employee:{employee_id}", json.dumps(data.dict()))  # Update the data in Redis
    return data

@app.delete("/deletedata/{employee_id}", response_model=Data)  # Delete Results
def delete_data(employee_id: int):
    if not r.exists(f"employee:{employee_id}"):
        raise HTTPException(status_code=404, detail="Data not found")

    data = r.get(f"employee:{employee_id}")
    r.delete(f"employee:{employee_id}")  # Remove the data from Redis
    return json.loads(data)  # Return the deleted data

application = app  # Alias for AWS Elastic Beanstalk