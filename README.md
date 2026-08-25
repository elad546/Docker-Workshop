# Docker Basics Interactive Workshop

A hands-on Docker tutorial with two interactive formats — pick the one you prefer:

| Format | File | Best for |
|--------|------|----------|
| **Runme** (recommended for CLI) | [WORKSHOP.md](WORKSHOP.md) | Step-by-step shell runbooks in VS Code |
| **Jupyter** | [WORKSHOP.ipynb](WORKSHOP.ipynb) | Jupyter Lab / VS Code notebook users |

Both cover the same modules and use the same example projects under `examples/`.

**Estimated time:** 30–45 minutes

## Prerequisites

| Requirement | Runme | Jupyter |
|-------------|-------|---------|
| [Docker Engine](https://docs.docker.com/get-docker/) | Required | Required |
| [VS Code](https://code.visualstudio.com/) | Recommended | Recommended |
| [Runme extension](https://marketplace.visualstudio.com/items?itemName=stateful.runme) | Required | — |
| [Jupyter extension](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter) | — | Required |

Optional Runme CLI for named cells from the terminal:

```bash
runme run --filename WORKSHOP.md build-hello-image
```

## Start here

### Option A — Runme (Markdown notebook)

1. Clone this repository and open it in VS Code.
2. Install the Runme extension when prompted.
3. Open **[WORKSHOP.md](WORKSHOP.md)** — it renders as a notebook with runnable cells.
4. Run each cell in order (▶).

### Option B — Jupyter notebook

1. Clone this repository and open it in VS Code or Jupyter Lab.
2. Install the Jupyter extension (VS Code) or `pip install jupyterlab`.
3. Open **[WORKSHOP.ipynb](WORKSHOP.ipynb)**.
4. Select the Python 3 kernel and run each cell in order.

> **Interactive exec:** `docker exec -it` needs a real TTY. The Jupyter notebook includes a terminal command for that step; Runme supports it natively via an interactive cell.

## What you'll learn

- Creating an image with `docker build`
- Committing a container with `docker commit`
- Running containers and exec-ing into them (`docker run`, `docker exec`)
- Managing containers and images (`docker ps`, `rm`, `rmi`, `image`)
- Docker Compose with custom bridge networks

## Port reference

| Service | Host port | Used in |
|---------|-----------|---------|
| hello-docker (nginx) | 8080 | Module 2–4 |
| compose-demo (web) | 8081 | Module 5 |

Make sure these ports are free before starting the workshop.

## Repository layout

```text
examples/
├── hello-docker/     # Single-container exercises (Modules 1–4)
└── compose-demo/     # Multi-service compose with bridge networks (Module 5)
WORKSHOP.md           # Runme notebook
WORKSHOP.ipynb        # Jupyter notebook
```

## Cleanup

Both workshops include cleanup cells at the end of Module 5 and Module 6. Run them when finished to remove containers and images created during the exercises.
