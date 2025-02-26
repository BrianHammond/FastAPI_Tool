from fastapi import FastAPI, HTTPException
from typing import Optional, Dict, List
from pydantic import BaseModel
import uvicorn

app = FastAPI(
    title="Employment Management API",
    description="For educational purposes only",
    version="1.0"
)

class Address(BaseModel):
    address_1: Optional[str] = None
    address_2: Optional[str] = None

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

data_store = {}

@app.get("/", summary="Home Endpoint", description="Returns a simple Hello World message. Can be used as base_url")
def home():
    return {"Hello": "World"}

@app.get("/getdata", response_model=Dict[str, List[Data]], description="Leaving the employee_id blank will return all") # Get Results
def get_data(employee_id: Optional[int] = None):
    if employee_id is not None:  # If ID is provided, return that specific data
        if employee_id in data_store:
            return {"employees": [data_store[employee_id]]}  # Wrap in a list under "Employees"
        else:
            raise HTTPException(status_code=404, detail="Data not found")
    else:  # If ID is not provided, return all data as a list under "Employees"
        return {"employees": list(data_store.values())}

@app.post("/postdata", response_model=Data, description="employee_id needs to be unique as it is used as a key value") # Post Results
def post_data(data: Data):
    if data.employee_id in data_store:
        raise HTTPException(status_code=400, detail="Data already exists")
    data_store[data.employee_id] = data  # Store the Data object by ID
    return data

@app.put("/putdata/{employee_id}", response_model=Data) # Update Results
def put_data(employee_id: int, data: Data):
    if employee_id not in data_store:
        raise HTTPException(status_code=404, detail="Data not found")
    # Update the data for the given ID
    data_store[employee_id] = data
    return data

@app.delete("/deletedata/{employee_id}", response_model=Data) # Delete Results
def delete_data(employee_id: int):
    if employee_id not in data_store:
        raise HTTPException(status_code=404, detail="Data not found")
    # Delete the data for the given ID
    data = data_store.pop(employee_id)
    return data

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
