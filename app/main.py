from fastapi import FastAPI
from pydantic import BaseModel
from uuid import uuid4
from app.db import init_db, save_session, save_execution
import os
from app.executor import run_code_in_docker

app = FastAPI(title="Coding Agent Sandbox")


class SessionCreate(BaseModel):
    user_id: str
    title: str


class ExecuteRequest(BaseModel):
    session_id: str
    code: str


@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def root():
    return {"message": "Sandbox API is running"}


@app.post("/sessions")
def create_session(data: SessionCreate):
    session_id = str(uuid4())

    save_session(session_id, data.user_id, data.title)

    return {
        "session_id": session_id,
        "user_id": data.user_id,
        "title": data.title
    }


@app.post("/execute")
def execute_code(data: ExecuteRequest):
    execution_id = str(uuid4())

    try:
        session_folder = os.path.abspath(os.path.join("data", "sessions", data.session_id))
        os.makedirs(session_folder, exist_ok=True)

        file_path = os.path.join(session_folder, "main.py")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(data.code)

        result = run_code_in_docker(file_path, data.session_id)

        save_execution(
            execution_id,
            data.session_id,
            data.code,
            result["stdout"],
            result["stderr"],
            result["exit_code"]
        )

        return {
            "execution_id": execution_id,
            "session_id": data.session_id,
            "stdout": result["stdout"],
            "stderr": result["stderr"],
            "exit_code": result["exit_code"]
        }

    except Exception as e:
        error_message = str(e)

        try:
            save_execution(
                execution_id,
                data.session_id,
                data.code,
                "",
                error_message,
                1
            )
        except Exception:
            pass

        return {
            "execution_id": execution_id,
            "session_id": data.session_id,
            "stdout": "",
            "stderr": error_message,
            "exit_code": 1
        }
    

@app.get("/sessions/{session_id}/artifacts")
def list_artifacts(session_id: str):
    session_folder = os.path.abspath(os.path.join("data", "sessions", session_id))

    if not os.path.exists(session_folder):
        return {"session_id": session_id, "artifacts": []}

    files = []

    for name in os.listdir(session_folder):
        file_path = os.path.join(session_folder, name)

        if os.path.isfile(file_path):
            files.append(name)

    return {
        "session_id": session_id,
        "artifacts": files
    }