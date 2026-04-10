# Platform Dev Task

## Core Task

**"Coding Agent Isolation & Data Persistence"** — Design and prototype an isolated execution environment for a coding agent that could be integrated into OpenWebUI, with CPU/memory limits, persistent storage for code and execution results, and the ability to scale to multiple concurrent users on a single server.

Users should be able to return to a previous session and re-execute or review their code and results. This means code, execution outputs, and any generated artifacts must persist across agent lifecycle events (restarts, scaling, cleanup).

Compare and evaluate approaches from:

- **Option A: Container-based Sandboxing** — Isolate execution using Docker containers, gVisor, or similar self-hosted sandboxing (e.g. pre-built container pools, cgroup limits, seccomp profiles). For reference, see [Docker AI Sandboxes](https://docs.docker.com/ai/sandboxes/) and [E2B](https://github.com/e2b-dev/e2b)
- **Option B: Pydantic Monty** — Secure Python interpreter with zero-access-by-default and microsecond startup
  https://github.com/pydantic/monty
- **Option C:** Your own suggested approach that fits the task



## Deliverables

- **Working, runnable prototype** — the solution must run on localhost and be demo-ready. We expect you to demo it after the task is finished. From MR we expect to clone your repo, follow setup instructions, and see it working. Include clear `README` with setup and run steps
- **OpenWebUI integration** — connect the sandbox to OpenWebUI so a user can trigger code execution from the chat interface. Choose the integration method that best fits your design (e.g. Tools/Functions, Pipelines, or MCP server).
- Brief `DECISIONS.md` explaining:
  - Which approaches you compared and why
  - Your chosen approach and its trade-offs
  - How CPU/memory isolation is achieved
  - How code and execution data are persisted and retrievable across sessions
  - What would be needed for production (multi-tenant, 25+ concurrent agents)
- MR to develop branch of this repository

## Additional Info

- OpenWebUI documentation: https://docs.openwebui.com
- Our production environment runs on Hetzner dedicated servers (bare metal, no managed K8s)
- **Hardware constraints:** assume a single server with 8 vCPU, 32 GB RAM, where ~30% is already consumed by the OpenWebUI — your sandbox resource limits should account for the remaining capacity


## Bonus Task

**API Gateway & Lifecycle Management** — Build a FastAPI service that manages the full agent lifecycle: create an isolated agent instance, execute code within it, retrieve results, and destroy it. Include health check endpoints, structured error responses (Pydantic models), and proper async handling for concurrent agent sessions.
