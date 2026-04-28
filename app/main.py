from fastapi import FastAPI
from app.schemas import SessionCreate, ExecuteRequest, EchoRequest
from app.db import init_db
from app.services import create_session_service, execute_code_service, list_artifacts_service
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Coding Agent Sandbox")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500",
                   "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@app.post("/echo")
def echo(data: EchoRequest):
    return {"message": f"You said: {data.text}"}