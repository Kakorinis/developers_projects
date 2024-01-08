from pydantic import BaseModel #for swagger customing

class ClientResponse(BaseModel):
    id: int
    fullname: str
    phone: str

class ClientNameResponse(BaseModel):
    fullname: str
    phone: str

class Error404Response(BaseModel):
    detail: str
