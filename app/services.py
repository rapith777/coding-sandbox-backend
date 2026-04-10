# Importing necessary libraries and modules
from uuid import uuid4  # To generate unique session IDs and execution IDs
from pathlib import Path  # To work with file and directory paths in a cleaner way
from app.db import save_session, save_execution  # To save session and execution data to the database
from app.executor import run_code_in_docker  # To call the function that runs the code in Docker
from app.schemas import SessionCreate, ExecuteRequest  # To use the Pydantic models for data validation


# Service to create a new session
def create_session_service(data: SessionCreate):
    # Generate a unique session ID using UUID
    session_id = str(uuid4())

    # Save the session details (session ID, user ID, title) to the database
    save_session(session_id, data.user_id, data.title)

    # Return the session details as a dictionary
    return {
        "session_id": session_id,
        "user_id": data.user_id,
        "title": data.title
    }


# Service to execute user code inside Docker
def execute_code_service(data: ExecuteRequest):
    # Generate a unique execution ID for this execution
    execution_id = str(uuid4())

    try:
        # Use Pathlib to handle session folder paths (this is cleaner and more intuitive than os.path)
        session_folder = Path("data", "sessions", data.session_id).resolve()

        # Create the session folder if it doesn't exist (with parents=True, it will create all parent directories)
        session_folder.mkdir(parents=True, exist_ok=True)

        # Define the file path to store the user's code (save it as 'user_code.py')
        file_path = session_folder / "user_code.py"

        # Write the user's code into the file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(data.code)

        # Call the executor to run the code inside Docker (passing file_path and session_id)
        result = run_code_in_docker(file_path, data.session_id)

        # Save the execution details (stdout, stderr, exit code) to the database
        save_execution(
            execution_id,
            data.session_id,
            data.code,
            result["stdout"],
            result["stderr"],
            result["exit_code"]
        )

        # Return the results of the execution (stdout, stderr, and exit code)
        return {
            "execution_id": execution_id,
            "session_id": data.session_id,
            "stdout": result["stdout"],
            "stderr": result["stderr"],
            "exit_code": result["exit_code"]
        }

    except Exception as e:
        # If there is any error during execution, catch it and handle it gracefully
        error_message = str(e)

        try:
            # Save the error message to the database, indicating a failed execution
            save_execution(
                execution_id,
                data.session_id,
                data.code,
                "",
                error_message,
                1  # exit code 1 indicates an error
            )
        except Exception:
            pass  # If saving execution fails, just continue

        # Return the error response
        return {
            "execution_id": execution_id,
            "session_id": data.session_id,
            "stdout": "",
            "stderr": error_message,
            "exit_code": 1
        }


# Service to list all the artifacts (files) in a session's folder
def list_artifacts_service(session_id: str):
    # Use Pathlib to handle the session folder path
    session_folder = Path("data", "sessions", session_id).resolve()

    # If the session folder does not exist, return an empty list of artifacts
    if not session_folder.exists():
        return {"session_id": session_id, "artifacts": []}

    # List to store the names of files in the session folder
    files = []

    # Loop through all the files in the session folder
    for name in session_folder.iterdir():
        # If it's a file (not a directory), add it to the list of artifacts
        if name.is_file():
            files.append(name.name)

    # Return the list of files (artifacts) in the session folder
    return {
        "session_id": session_id,
        "artifacts": files
    }