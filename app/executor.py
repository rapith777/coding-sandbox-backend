import docker
import os

def run_code_in_docker(file_path, session_id):
    client = docker.from_env()
    session_folder = os.path.abspath(os.path.join("data", "sessions", session_id))
    session_folder = session_folder.replace("\\", "/")

    file_name = os.path.basename(file_path)

    try:
        container = client.containers.run(
            "sandbox-runner",
            ["python", f"/workspace/{file_name}"],
            volumes={
                session_folder: {
                    "bind": "/workspace",
                    "mode": "rw"
                }
            },
            working_dir="/workspace",
            mem_limit="512m",
            nano_cpus=500000000,
            network_disabled=True,
            remove=True
        )

        return {
            "stdout": container.decode("utf-8"),
            "stderr": "",
            "exit_code": 0
        }

    except Exception as e:
        return {
            "stdout": "",
            "stderr": str(e),
            "exit_code": 1
        }