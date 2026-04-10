Goal:

Building a prototype of isolated code execution for openWebUI with cpu memory limit, persistent websessions and saved output logs, files.
Also support for running into previous sessions.


path and approach: small backend fastapi skeleton and then adding persistance and later executing sandbox and integrating openWebUI


Decision 1: starting with Fastapi service because it is simple and fast for a localhost demo and also comes with automatic OpenAPI docs and easy to integrate later with OPENWebUI as external tool

Decision 2: creating early sessions so that user can come and look itno previous sessions and cansee the store , saved files and logs and outputs.

Decision 3: used sqlite because no separate database server was needed and can run locally and also enough for now to store sessions and data 

Decision 4:  i have selected Docker for code execution because it provides string isolation and easy cpu plus memory limits and widely used in production level.

before this trying to run locally and then jumping into docker isolation make it more clearer

Decision 5: Execution Endpoint Decision

First i am trying to implemented a basic /execute endpoint that runs user Python code using subprocess and the code is written to a temporary .py file, executed and the output stdout, stderr, exit code is returned.

and later i will be replace with a Docker based sandbox for proper isolation.

Decision 6: i created a small Docker runner image based on python:3.11-slim so that user code can be executed inside an isolated container instead of directly on my local machine

I used the Python Docker SDK so the FastAPI service can create and control containers directly from the backend code.
Each execution runs in the sandbox-runner image to provide isolation from the main system.

Based on the server resources (8 CPU, 32 GB RAM) and the 30% usage by OpenWebUI approximately 5–6 CPU cores and 22 GB RAM remain. I limited each execution container to 512 MB RAM and 0.5 CPU. This allows roughly 11 concurrent executions before CPU becomes the limiting factor which provides safe multi-user execution without exhausting the server.