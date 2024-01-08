from sqlalchemy import create_engine, text
import pandas as pd
from fastapi import FastAPI, APIRouter
import uvicorn
import time
from typing import List
from pydantic import BaseModel
from for_swagger import ClientResponse, ClientNameResponse, Error404Response
from fastapi import HTTPException


class DatabaseConnection:
    def __init__(self):
        self.database = "ka_clients"
        self.host = "localhost"
        self.port = "5432"
        self.username = "postgres"
        self.password = "1111"

        self.conn_str = f'postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}'

    def __enter__(self):
        self.conn = create_engine(self.conn_str)
        self.cursor = self.conn.connect()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.conn.dispose()

app = FastAPI()
router = APIRouter()


def execute_query(query):
    with DatabaseConnection() as connection:
        result = connection.execute(query)
        columns = [col[0] for col in result.cursor.description] # Fetch column names separately
        rows = result.fetchall() # Fetch all rows from the result set
        return [dict(zip(columns, row)) for row in rows]


@router.get("/client/{phone_str}", response_model=List[ClientResponse],
            responses={200: {"description": "Success"}, 404: {"model": Error404Response, "description": "Not Found"}},
            tags=["Types of requests"])
async def get_client(phone_str: str):
    query = text(fr""" SELECT * FROM all_clients 
                                   WHERE phone like '%{phone_str}%' """)
    result = execute_query(query)
    if len(result) == 0:
        raise HTTPException(status_code=404, detail="No data found in the table")

    time.sleep(2)
    return result


@router.get("/client_name/{surname_str}", response_model=List[ClientNameResponse],
            responses={200: {"description": "Success"}, 404: {"model": Error404Response, "description": "Not Found"}},
            tags=["Types of requests"])
async def get_client_name(surname_str: str):
    query = text(fr""" SELECT fullname, phone FROM all_clients 
                                       WHERE fullname like '%{surname_str}%' """)
    result = execute_query(query)

    if len(result) == 0:
        raise HTTPException(status_code=404, detail="No data found in the table")

    time.sleep(2)
    return result


app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)