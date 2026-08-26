# Docker Basics Interactive Workshop

Welcome! This notebook walks through Docker fundamentals step by step.

**Estimated time:** 30–45 minutes

## Before you start (VS Code)

1. Open this repository in [VS Code](https://code.visualstudio.com/).
2. Install the [Runme extension](vscode:extension/stateful.runme) when prompted (Extensions panel → `Ctrl+Shift+X` → search **Runme**).
3. Open this file — VS Code renders it as a notebook.
4. Click **Run** (▶) on each cell, top to bottom.

Module 0 below installs Docker and fixes socket permissions if needed.

---

## Module 0: Prerequisites

### Install Docker

```sh {"terminalRows":"8"}
sudo apt update && sudo apt install -y docker.io
```

```sh {"terminalRows":"3"}
sudo systemctl start docker && sudo systemctl enable docker
```

### Verify Docker

```sh {"terminalRows":"2"}
docker --version
```

```sh {"terminalRows":"6","name":"verify-docker-info"}
docker info --format '{{.ServerVersion}}' 2>/dev/null || docker info | head -5
```

### Fix: permission denied

If the **second cell above** shows `permission denied while trying to connect to the docker API at unix:///var/run/docker.sock`, work through these steps:

**Step 1** — add your user to the `docker` group:

```sh {"terminalRows":"6"}
sudo usermod -aG docker $USER
sudo apt install -y util-linux-extra
echo "Added $(whoami) to the docker group."
```

**Step 2** — confirm the fix:

```sh {"terminalRows":"6"}
sg docker -c "docker info --format '{{.ServerVersion}}' 2>/dev/null || docker info | head -5"
```

**Why does Step 2 work but the second cell doesn't?**

`usermod` updates the system config, but VS Code (and each Runme cell) still runs with the **groups from when you logged in**. `sg docker` starts a one-off shell with the `docker` group applied, so `docker info` succeeds. The second cell uses plain `docker` without that — so it keeps failing until you refresh your session (Step 3).

**Step 3** — refresh groups, then re-run the second cell. Try **A**, then **B** if needed:

**A) Reload Window** — `Ctrl+Shift+P` → **Developer: Reload Window** → re-run the second cell (`docker info`).

**B) newgrp** — close VS Code, open a regular terminal, and run:

```sh
newgrp docker
code .
```

Re-open `WORKSHOP.md` and re-run the second cell (`docker info`).

**C) Log out** of Linux and back in, reopen VS Code, re-run the second cell.

---

## Module 1: Creating an Image

A **Dockerfile** describes how to build an image. The `docker build` command reads that file and produces a tagged image you can run as containers.

Inspect the example project at `examples/hello-docker/` — it uses nginx to serve a simple HTML page.

### Build the image

```sh {"terminalRows":"12"}
cd examples/hello-docker && docker build -t hello-docker:1.0 .
```

The `-t` flag **tags** the image with a name (`hello-docker`) and version (`1.0`). Docker caches each instruction as a **layer** to speed up rebuilds.

### List the new image

```sh {"terminalRows":"4"}
docker images hello-docker
```

You should see `hello-docker` with tag `1.0`, along with its image ID and size.

---

## Module 2: Docker Run and Exec

`docker run` creates and starts a container from an image. `docker exec` runs a command inside an already-running container.

### Start a container in the background

```sh {"terminalRows":"2"}
docker run -d --name hello -p 8080:80 hello-docker:1.0
```

- `-d` runs detached (in the background)
- `--name hello` gives the container a friendly name
- `-p 8080:80` maps host port 8080 to container port 80

### List running containers

```sh {"terminalRows":"5"}
docker ps
```

```sh {"terminalRows":"6"}
docker ps -a
```

`docker ps` shows only **running** containers. Add `-a` to include stopped ones.

### Verify the app is reachable

```sh {"terminalRows":"5"}
curl -s localhost:8080
```

### Exec a command (non-interactive)

```sh {"terminalRows":"6"}
docker exec hello cat /usr/share/nginx/html/index.html
```

`docker exec` runs a single command inside the container without opening a full shell.

### Exec an interactive shell

```sh {"interactive":"true","terminalRows":"8"}
docker exec -it hello sh
```

This opens an interactive shell inside the container. Try running `hostname` or `ls /usr/share/nginx/html`, then type `exit` to leave.

### View container logs

```sh {"terminalRows":"6"}
docker logs hello
```

---

## Module 3: Commit an Image

`docker commit` saves a container's current filesystem state as a **new image**. This is useful for learning, but in production you should prefer updating the Dockerfile and rebuilding.

### Create a marker file inside the container

```sh {"terminalRows":"2"}
docker exec hello sh -c 'echo "committed-layer" > /tmp/marker'
```

### Commit the container as a new image

```sh {"terminalRows":"2"}
docker commit hello hello-docker:committed
```

### Compare images

```sh {"terminalRows":"5"}
docker images hello-docker
```

You should now see both `1.0` and `committed` tags.

### Prove the change persisted

```sh {"terminalRows":"2"}
docker run --rm hello-docker:committed cat /tmp/marker
```

The marker file exists in the committed image even though it was never in the original Dockerfile.

---

## Module 4: Container and Image Management

These commands manage the lifecycle of containers and images.

### Stop and start a container

```sh {"terminalRows":"2"}
docker stop hello
```

```sh {"terminalRows":"4"}
docker ps -a --filter name=hello
```

The container still exists but its status is **Exited**.

```sh {"terminalRows":"2"}
docker start hello
```

```sh {"terminalRows":"4"}
docker ps --filter name=hello
```

### Remove the container

> Run this cell when you are ready — it permanently removes the `hello` container.

```sh {"terminalRows":"2"}
docker rm -f hello
```

`-f` forces removal even if the container is still running.

### Remove an image

> Run after the container is removed.

```sh {"terminalRows":"2"}
docker rmi hello-docker:1.0
```

You cannot remove an image that is still in use by a container.

### List images (alternative command)

```sh {"terminalRows":"4"}
docker image ls hello-docker
```

`docker image ls` is equivalent to `docker images`.

### Prune unused images (optional)

> This removes dangling (untagged) images. Safe to skip if you have none.

```sh {"terminalRows":"3"}
docker image prune -f
```

---

## Module 5: Docker Compose with Bridge Networks

Docker Compose orchestrates multi-container applications. Custom **bridge** networks isolate services while allowing DNS-based discovery by service name.

Inspect the project at `examples/compose-demo/`:
- **web** (nginx) on the `frontend` network — exposed on port 8081
- **api** (Python) on both `frontend` and `backend` networks
- **redis** on the `backend` network only

### Validate the compose file

```sh {"terminalRows":"8"}
cd examples/compose-demo && docker compose config
```

### Networks before starting

```sh {"terminalRows":"6"}
docker network ls
```

### Start all services

```sh {"terminalRows":"10"}
cd examples/compose-demo && docker compose up -d --build --wait
```

The `--wait` flag blocks until health checks pass, so the API is ready before you test it.

### Inspect bridge networks

```sh {"terminalRows":"5"}
docker network ls --filter name=compose-demo
```

```sh {"terminalRows":"2"}
docker network inspect compose-demo_frontend --format '{{.Driver}}: {{range .Containers}}{{.Name}} {{end}}'
```

The driver should be `bridge`. Connected containers appear by name.

### Test the web front-end

```sh {"terminalRows":"5"}
curl -s localhost:8081
```

### Test API through nginx proxy

The web container reaches the API at `http://api:5000` via Docker's internal DNS — no host port needed for the API.

```sh {"terminalRows":"2"}
curl -s localhost:8081/api/health
```

Run this a few times — the `redis_hits` counter should increment, proving the API can reach Redis on the `backend` network.

### List compose services

```sh {"terminalRows":"5"}
cd examples/compose-demo && docker compose ps
```

### Tear down compose stack

> Run when finished with this module.

```sh {"terminalRows":"6"}
cd examples/compose-demo && docker compose down --volumes --remove-orphans
```

---

## Module 6: Final Cleanup

Remove any leftover workshop resources. Skip cells that already succeeded above.

```sh {"terminalRows":"4"}
docker rm -f hello 2>/dev/null || true
docker compose -f examples/compose-demo/docker-compose.yml down --volumes --remove-orphans 2>/dev/null || true
```

```sh {"terminalRows":"4"}
docker rmi hello-docker:1.0 hello-docker:committed 2>/dev/null || true
docker rmi compose-demo-web compose-demo-api 2>/dev/null || true
```

```sh {"terminalRows":"4"}
echo "Remaining workshop containers:" && docker ps -a --filter name=hello --filter name=compose-demo --format '{{.Names}}' | grep -E 'hello|compose-demo' || echo "(none)"
echo "Remaining workshop images:" && docker images --format '{{.Repository}}:{{.Tag}}' | grep -E 'hello-docker|compose-demo' || echo "(none)"
```

---

## Congratulations!

You covered:
1. **Building** an image from a Dockerfile
2. **Running** containers and **exec** into them
3. **Committing** container changes to a new image
4. **Managing** containers and images (`ps`, `stop`, `start`, `rm`, `rmi`, `image`)
5. **Docker Compose** with custom **bridge** networks and service discovery

**Challenge:** Modify `examples/hello-docker/app/index.html`, rebuild the image, and run a new container to see your changes live.
