from pydantic import BaseModel

class SessionCreate(BaseModel):
    user_id: str
    title: str

class ExecuteRequest(BaseModel):
    session_id: str
    code: str