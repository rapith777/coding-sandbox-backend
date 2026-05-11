# Coding Sandbox & LLM Backend API

A backend system for safely executing user-submitted Python code in isolated Docker containers, with session tracking, result storage, and LLM/Open WebUI integration support.

## Overview

This project is built with FastAPI, Docker, SQLite, and a simple HTML/JavaScript frontend.

The main goal is to create a secure coding sandbox where user-submitted Python code can be executed in an isolated environment instead of running directly on the host machine.

The project is also being extended toward an LLM-powered workflow using Ollama and Open WebUI. In this setup, the LLM can help generate or explain code, while the FastAPI backend and Docker sandbox handle the actual execution.

## Current Architecture

```text
Simple Frontend
HTML + JavaScript
        ↓
FastAPI Backend
        ↓
SQLite Database
        ↓
Docker Sandbox
        ↓
Execution Output
```

LLM direction:

```text
Open WebUI
        ↓
Ollama Local Model
        ↓
Open WebUI Tool
        ↓
FastAPI Backend
        ↓
Docker Sandbox
        ↓
Execution Output
```

## Features

- Execute Python code inside isolated Docker containers
- Session-based execution tracking
- Store submitted code, stdout, stderr, exit status, and metadata
- SQLite persistence layer for sessions and executions
- Workspace/session folder structure for execution files and artifacts
- REST APIs for session creation, code execution, and artifact listing
- Simple frontend using HTML and JavaScript
- Local LLM workflow prepared using Ollama and Open WebUI
- Open WebUI installed as a project dependency, not cloned into the repository

## Execution Safety

Each code execution is designed to run in an isolated Docker container with:

- limited CPU usage
- limited memory usage
- disabled network access
- separated execution workspace

This helps prevent user code from running directly on the host system.

## Tech Stack

- Python 3.12
- FastAPI
- Pydantic
- Docker
- SQLite
- HTML
- JavaScript
- Ollama
- Open WebUI

## How It Works

1. A user creates a session.
2. The user submits Python code through the frontend or API.
3. The FastAPI backend receives and validates the request.
4. The code is saved inside a session-specific workspace.
5. Docker runs the code inside an isolated container.
6. stdout, stderr, exit code, and metadata are collected.
7. Results are stored in SQLite.
8. The backend returns the result to the frontend or API caller.

## API Endpoints

```text
POST /sessions
```

Creates a new execution session.

```text
POST /execute
```

Executes submitted Python code inside the Docker sandbox.

```text
GET /sessions/{session_id}/artifacts
```

Lists generated files or artifacts for a session.

## Local Development

### 1. Create and activate virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Start Docker Desktop

Make sure Docker Desktop is running before executing code.

Check with:

```powershell
docker ps
```

### 4. Run the FastAPI backend

```powershell
python -m uvicorn app.main:app --reload
```

Backend runs at:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

### 5. Run the simple frontend

Open a second terminal:

```powershell
cd frontend
python -m http.server 5500
```

Frontend runs at:

```text
http://localhost:5500/
```

### 6. Run Open WebUI

Open another terminal:

```powershell
.\.venv\Scripts\Activate.ps1
open-webui serve
```

Open WebUI runs at:

```text
http://localhost:8080
```

Ollama should be running locally for local model usage.

Check available Ollama models with:

```powershell
ollama list
```

## Current LLM Integration Status

Open WebUI and Ollama are running locally and can communicate with each other.

Current working flow:

```text
Open WebUI
        ↓
Ollama
        ↓
Local LLM response
```

Planned/next integration:

```text
Open WebUI Tool
        ↓
FastAPI /execute endpoint
        ↓
Docker sandbox
        ↓
Real execution output returned to chat
```

In this architecture:

- Ollama acts as the local LLM.
- Open WebUI acts as the chat interface and coordinator.
- The Open WebUI tool will call the FastAPI backend.
- FastAPI sends the code to Docker for real execution.
- Docker returns the actual output.

## Use Cases

- AI coding assistants
- Secure Python code execution
- Code execution platforms
- Automated evaluation systems
- LLM-assisted programming workflows
- Educational coding sandboxes

## Project Status

This is an active learning and development project.

Completed so far:

- FastAPI backend
- Docker-based Python execution
- SQLite persistence
- Session-based execution tracking
- Simple frontend
- Open WebUI installation
- Ollama local model connection

In progress:

- Connecting Open WebUI tools to the FastAPI sandbox backend
- Improving LLM-assisted code execution workflow
- Strengthening execution safety and error handling

## Notes

Do not commit local virtual environments, databases, or Open WebUI secret files to GitHub.

Recommended `.gitignore` entries:

```gitignore
.venv/
.venv-1/
__pycache__/
*.pyc
sandbox.db
*.db
data/sessions/*
.webui_secret_key
open-webui/
```