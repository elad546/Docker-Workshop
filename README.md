# Docker Basics Interactive Workshop

A hands-on Docker tutorial you run inside **VS Code** with the [Runme](https://runme.dev) extension. Each command is a runnable cell — click ▶ and follow along.

**Estimated time:** 30–45 minutes

## Prerequisites

| Requirement | Notes |
|-------------|-------|
| [VS Code](https://code.visualstudio.com/) | Open this repo as a folder |
| [Runme extension](https://marketplace.visualstudio.com/items?itemName=stateful.runme) | VS Code will suggest it when you open the repo |
| [Docker Desktop](https://docs.docker.com/desktop/) | macOS / Windows — or Linux: Module 0 installs `docker.io` via apt |

> **Linux:** Module 0 covers `apt install docker.io`, permission fix (`usermod`, `util-linux-extra`, `newgrp`), then re-running `docker info`.

## Start here

1. **Clone** this repository and open the folder in VS Code.
2. **Install Runme** — click *Install* when VS Code recommends extensions, or open Extensions (`Ctrl+Shift+X` / `Cmd+Shift+X`) and search for **Runme**.
3. **Open [WORKSHOP.md](WORKSHOP.md)** — Runme renders it as an interactive notebook.
4. **Run each cell** in order from top to bottom (▶ button on each code block).

> **Tip:** If a `.md` file opens as plain text instead of a notebook, right-click the file → **Open With…** → **Runme**.

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

> **Linux setup & permission denied?** See Module 0 for `docker.io` install and the permission fix steps.

## Repository layout

```text
examples/
├── hello-docker/     # Single-container exercises (Modules 1–4)
└── compose-demo/     # Multi-service compose with bridge networks (Module 5)
WORKSHOP.md           # Interactive notebook — start here
```

## Cleanup

The workshop includes cleanup cells at the end of Module 5 and Module 6. Run them when finished to remove containers and images created during the exercises.
