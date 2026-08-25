# Docker Basics Interactive Workshop

A hands-on Docker tutorial you run directly inside VS Code using the [Runme](https://runme.dev) extension. Each command is a runnable cell — click ▶ and follow along.

**Estimated time:** 30–45 minutes

## Prerequisites

| Requirement | Notes |
|-------------|-------|
| [Docker Engine](https://docs.docker.com/get-docker/) | Docker Desktop or native Docker on Linux |
| [VS Code](https://code.visualstudio.com/) | Any recent version |
| [Runme extension](https://marketplace.visualstudio.com/items?itemName=stateful.runme) | Opens `.md` files as interactive notebooks |

Optional: install the [Runme CLI](https://docs.runme.dev/installation/cli) to run named cells from the terminal:

```bash
runme run --filename WORKSHOP.md build-hello-image
```

## Start here

1. Clone this repository and open it in VS Code.
2. Install the Runme extension when prompted (or from the Extensions panel).
3. Open **[WORKSHOP.md](WORKSHOP.md)** — it renders as a notebook with runnable cells.
4. Run each cell in order from top to bottom.

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
WORKSHOP.md           # Interactive notebook — start here
```

## Cleanup

The workshop includes cleanup cells at the end of Module 5 and Module 6. Run them when finished to remove containers and images created during the exercises.
