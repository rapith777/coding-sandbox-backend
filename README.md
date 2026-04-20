# Coding Sandbox Backend

A backend system to safely execute user-submitted code in isolated environments.

## Overview

This project is built using FastAPI and Docker to run user code securely.

Each execution is isolated with:
- limited CPU and memory
- no network access

The system uses a session-based architecture to manage executions and store results.

## Features

- Run user code inside Docker containers
- Session-based execution tracking
- Store stdout, stderr, and execution metadata
- REST APIs for execution and session management
- Basic LLM integration for structured responses

## Tech Stack

- Python
- FastAPI
- Docker
- SQLite

## How it Works

1. Create a session using API
2. Submit code for execution
3. Code is saved inside a session folder
4. Docker container runs the code safely
5. Output is stored and returned via API

## API Endpoints

- `POST /sessions` → create session  
- `POST /execute` → execute code  
- `GET /sessions/{id}/artifacts` → list generated files  

## Use Cases

- AI coding assistants  
- Code execution platforms  
- Automated evaluation systems  

## Status

This is an active project focused on improving execution safety and system design.