import os
from uuid import uuid4
from app.db import save_session, save_execution
from app.executor import run_code_in_docker

def create_session_service(data):
    session_id = str(uuid4())
    save_session(session_id, data.user_id, data.title)

    return {
        "session_id": session_id,
        "user_id": data.user_id,
        "title": data.title
    }

def execute_code_service(data):
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

def list_artifacts_service(session_id: str):
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