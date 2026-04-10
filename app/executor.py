import docker
from pathlib import Path

def run_code_in_docker(file_path, session_id):
    client = docker.from_env()  # Connect to Docker using the environment variables

    # Use Pathlib to handle session folder path
    session_folder = Path("data", "sessions", session_id).resolve()

    # Extract the file name from the provided file path
    file_name = Path(file_path).name

    try:
        # Run the container using the "sandbox-runner" image
        container = client.containers.run(
            "sandbox-runner",  # Docker image to use
            ["python", f"/workspace/{file_name}"],  # Command to run inside the container
            volumes={
                str(session_folder): {
                    "bind": "/workspace",  # Mount the session folder to the container's /workspace
                    "mode": "rw"           # Read-write mode
                }
            },
            working_dir="/workspace",  # Set the working directory inside the container
            mem_limit="512m",          # Set memory limit for the container (512 MB)
            nano_cpus=500000000,       # Set CPU limit (0.5 CPU)
            network_disabled=True,     # Disable networking in the container
            remove=True                # Remove the container after execution
        )

        # Return the output of the container execution
        return {
            "stdout": container.decode("utf-8"),  # Get the stdout output from the container
            "stderr": "",                         # No stderr here, it's an empty string
            "exit_code": 0                        # Exit code 0 means success
        }

    except Exception as e:
        # If there's an error during the execution, catch the exception and return the error
        return {
            "stdout": "",
            "stderr": str(e),  # Convert the error to a string
            "exit_code": 1     # Exit code 1 means failure
        }