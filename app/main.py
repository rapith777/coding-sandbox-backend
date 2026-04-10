from fastapi import FastAPI
from app.schemas import SessionCreate, ExecuteRequest
from app.db import init_db
from app.services import create_session_service, execute_code_service, list_artifacts_service

app = FastAPI(title="Coding Agent Sandbox")

@app.on_event("startup")
def startup():
    init_db()

@app.get("/")
def root():
    return {"message": "Sandbox API is running"}

@app.post("/sessions")
def create_session(data: SessionCreate):
    return create_session_service(data)

@app.post("/execute")
def execute_code(data: ExecuteRequest):
    return execute_code_service(data)

@app.get("/sessions/{session_id}/artifacts")
def list_artifacts(session_id: str):
    return list_artifacts_service(session_id)