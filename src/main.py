from fastapi import FastAPI, HTTPException
from typing import Optional, Dict, List
from pydantic import BaseModel
import redis.asyncio as aioredis  # Import redis.asyncio instead of aioredis
import json

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

# Redis setup
REDIS_HOST = "redis"  # Redis server address, use the appropriate address if you're using a cloud instance
REDIS_PORT = 6379  # Default Redis port
redis = None

async def get_redis():
    global redis
    if not redis:
        redis = await aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}")
    return redis

@app.get("/", summary="Home Endpoint", description="Returns a simple Hello World message. Can be used as base_url")
def home():
    return {"Hello": "World"}

@app.get("/getdata", response_model=Dict[str, List[Data]], description="Leaving the employee_id blank will return all")  # Get Results
async def get_data(employee_id: Optional[int] = None):
    redis = await get_redis()

    if employee_id is not None:  # If ID is provided, return that specific data
        data = await redis.get(f"employee:{employee_id}")
        if data:
            return {"employees": [json.loads(data)]}  # Deserialize the data from Redis and return it as a list
        else:
            raise HTTPException(status_code=404, detail="Data not found")
    else:  # If ID is not provided, return all data as a list under "Employees"
        keys = await redis.keys("employee:*")  # Get all employee keys
        if not keys:
            return {"employees": []}

        employees = []
        for key in keys:
            data = await redis.get(key)
            if data:
                employees.append(json.loads(data))
        return {"employees": employees}

@app.post("/postdata", response_model=Data, description="employee_id needs to be unique as it is used as a key value")  # Post Results
async def post_data(data: Data):
    redis = await get_redis()

    if await redis.exists(f"employee:{data.employee_id}"):
        raise HTTPException(status_code=400, detail="Data already exists")

    await redis.set(f"employee:{data.employee_id}", json.dumps(data.dict()))  # Store the Data object as JSON
    return data

@app.put("/putdata/{employee_id}", response_model=Data)  # Update Results
async def put_data(employee_id: int, data: Data):
    redis = await get_redis()

    if not await redis.exists(f"employee:{employee_id}"):
        raise HTTPException(status_code=404, detail="Data not found")

    await redis.set(f"employee:{employee_id}", json.dumps(data.dict()))  # Update the data in Redis
    return data

@app.delete("/deletedata/{employee_id}", response_model=Data)  # Delete Results
async def delete_data(employee_id: int):
    redis = await get_redis()

    if not await redis.exists(f"employee:{employee_id}"):
        raise HTTPException(status_code=404, detail="Data not found")

    data = await redis.get(f"employee:{employee_id}")
    await redis.delete(f"employee:{employee_id}")  # Remove the data from Redis
    return json.loads(data)  # Return the deleted data
