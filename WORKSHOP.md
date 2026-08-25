---
shell: bash
terminalRows: 15
---

# Docker Basics Interactive Workshop

Welcome! This notebook walks through Docker fundamentals step by step. Open this file in VS Code with the [Runme extension](https://marketplace.visualstudio.com/items?itemName=stateful.runme) installed, then click **Run** (▶) on each cell in order.

**Estimated time:** 30–45 minutes

---

## Module 0: Prerequisites

Make sure Docker Engine and the Runme VS Code extension are installed before continuing.

### Verify Docker

```sh {"name":"docker-version","interactive":"false","closeTerminalOnSuccess":"false"}
docker --version
```

```sh {"name":"docker-info","interactive":"false","closeTerminalOnSuccess":"false"}
docker info --format '{{.ServerVersion}}' 2>/dev/null || docker info | head -5
```

---

## Module 1: Creating an Image

A **Dockerfile** describes how to build an image. The `docker build` command reads that file and produces a tagged image you can run as containers.

Inspect the example project at `examples/hello-docker/` — it uses nginx to serve a simple HTML page.

### Build the image

```sh {"name":"build-hello-image","cwd":"examples/hello-docker","interactive":"false","closeTerminalOnSuccess":"false"}
docker build -t hello-docker:1.0 .
```

The `-t` flag **tags** the image with a name (`hello-docker`) and version (`1.0`). Docker caches each instruction as a **layer** to speed up rebuilds.

### List the new image

```sh {"name":"list-hello-image","interactive":"false","closeTerminalOnSuccess":"false"}
docker images hello-docker
```

You should see `hello-docker` with tag `1.0`, along with its image ID and size.

---

## Module 2: Docker Run and Exec

`docker run` creates and starts a container from an image. `docker exec` runs a command inside an already-running container.

### Start a container in the background

```sh {"name":"run-hello-container","interactive":"false","closeTerminalOnSuccess":"false"}
docker run -d --name hello -p 8080:80 hello-docker:1.0
```

- `-d` runs detached (in the background)
- `--name hello` gives the container a friendly name
- `-p 8080:80` maps host port 8080 to container port 80

### List running containers

```sh {"name":"docker-ps","interactive":"false","closeTerminalOnSuccess":"false"}
docker ps
```

```sh {"name":"docker-ps-all","interactive":"false","closeTerminalOnSuccess":"false"}
docker ps -a
```

`docker ps` shows only **running** containers. Add `-a` to include stopped ones.

### Verify the app is reachable

```sh {"name":"curl-hello-app","interactive":"false","closeTerminalOnSuccess":"false"}
curl -s localhost:8080
```

### Exec a command (non-interactive)

```sh {"name":"exec-cat-html","interactive":"false","closeTerminalOnSuccess":"false"}
docker exec hello cat /usr/share/nginx/html/index.html
```

`docker exec` runs a single command inside the container without opening a full shell.

### Exec an interactive shell

```sh {"name":"exec-interactive-shell","interactive":"true","closeTerminalOnSuccess":"false"}
docker exec -it hello sh
```

This opens an interactive shell inside the container. Try running `hostname` or `ls /usr/share/nginx/html`, then type `exit` to leave.

### View container logs

```sh {"name":"docker-logs-hello","interactive":"false","closeTerminalOnSuccess":"false"}
docker logs hello
```

---

## Module 3: Commit an Image

`docker commit` saves a container's current filesystem state as a **new image**. This is useful for learning, but in production you should prefer updating the Dockerfile and rebuilding.

### Create a marker file inside the container

```sh {"name":"commit-create-marker","interactive":"false","closeTerminalOnSuccess":"false"}
docker exec hello sh -c 'echo "committed-layer" > /tmp/marker'
```

### Commit the container as a new image

```sh {"name":"docker-commit","interactive":"false","closeTerminalOnSuccess":"false"}
docker commit hello hello-docker:committed
```

### Compare images

```sh {"name":"compare-images","interactive":"false","closeTerminalOnSuccess":"false"}
docker images hello-docker
```

You should now see both `1.0` and `committed` tags.

### Prove the change persisted

```sh {"name":"verify-committed-image","interactive":"false","closeTerminalOnSuccess":"false"}
docker run --rm hello-docker:committed cat /tmp/marker
```

The marker file exists in the committed image even though it was never in the original Dockerfile.

---

## Module 4: Container and Image Management

These commands manage the lifecycle of containers and images.

### Stop and start a container

```sh {"name":"docker-stop-hello","interactive":"false","closeTerminalOnSuccess":"false"}
docker stop hello
```

```sh {"name":"docker-ps-after-stop","interactive":"false","closeTerminalOnSuccess":"false"}
docker ps -a --filter name=hello
```

The container still exists but its status is **Exited**.

```sh {"name":"docker-start-hello","interactive":"false","closeTerminalOnSuccess":"false"}
docker start hello
```

```sh {"name":"docker-ps-after-start","interactive":"false","closeTerminalOnSuccess":"false"}
docker ps --filter name=hello
```

### Remove the container

> Run this cell when you are ready — it permanently removes the `hello` container.

```sh {"name":"docker-rm-hello","interactive":"false","closeTerminalOnSuccess":"false","excludeFromRunAll":"true"}
docker rm -f hello
```

`-f` forces removal even if the container is still running.

### Remove an image

> Run after the container is removed.

```sh {"name":"docker-rmi-hello","interactive":"false","closeTerminalOnSuccess":"false","excludeFromRunAll":"true"}
docker rmi hello-docker:1.0
```

You cannot remove an image that is still in use by a container.

### List images (alternative command)

```sh {"name":"docker-image-ls","interactive":"false","closeTerminalOnSuccess":"false"}
docker image ls hello-docker
```

`docker image ls` is equivalent to `docker images`.

### Prune unused images (optional)

> This removes dangling (untagged) images. Safe to skip if you have none.

```sh {"name":"docker-image-prune","interactive":"false","closeTerminalOnSuccess":"false","excludeFromRunAll":"true"}
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

```sh {"name":"compose-config","cwd":"examples/compose-demo","interactive":"false","closeTerminalOnSuccess":"false"}
docker compose config
```

### Networks before starting

```sh {"name":"network-ls-before","interactive":"false","closeTerminalOnSuccess":"false"}
docker network ls
```

### Start all services

```sh {"name":"compose-up","cwd":"examples/compose-demo","interactive":"false","closeTerminalOnSuccess":"false"}
docker compose up -d --build --wait
```

The `--wait` flag blocks until health checks pass, so the API is ready before you test it.

### Inspect bridge networks

```sh {"name":"network-ls-after","interactive":"false","closeTerminalOnSuccess":"false"}
docker network ls --filter name=compose-demo
```

```sh {"name":"network-inspect-frontend","interactive":"false","closeTerminalOnSuccess":"false"}
docker network inspect compose-demo_frontend --format '{{.Driver}}: {{range .Containers}}{{.Name}} {{end}}'
```

The driver should be `bridge`. Connected containers appear by name.

### Test the web front-end

```sh {"name":"curl-compose-web","interactive":"false","closeTerminalOnSuccess":"false"}
curl -s localhost:8081
```

### Test API through nginx proxy

The web container reaches the API at `http://api:5000` via Docker's internal DNS — no host port needed for the API.

```sh {"name":"curl-compose-api-health","interactive":"false","closeTerminalOnSuccess":"false"}
curl -s localhost:8081/api/health
```

Run this a few times — the `redis_hits` counter should increment, proving the API can reach Redis on the `backend` network.

### List compose services

```sh {"name":"compose-ps","cwd":"examples/compose-demo","interactive":"false","closeTerminalOnSuccess":"false"}
docker compose ps
```

### Tear down compose stack

> Run when finished with this module.

```sh {"name":"compose-down","cwd":"examples/compose-demo","interactive":"false","closeTerminalOnSuccess":"false","excludeFromRunAll":"true"}
docker compose down --volumes --remove-orphans
```

---

## Module 6: Final Cleanup

Remove any leftover workshop resources. Skip cells that already succeeded above.

```sh {"name":"cleanup-containers","interactive":"false","closeTerminalOnSuccess":"false","excludeFromRunAll":"true"}
docker rm -f hello 2>/dev/null || true
docker compose -f examples/compose-demo/docker-compose.yml down --volumes --remove-orphans 2>/dev/null || true
```

```sh {"name":"cleanup-images","interactive":"false","closeTerminalOnSuccess":"false","excludeFromRunAll":"true"}
docker rmi hello-docker:1.0 hello-docker:committed 2>/dev/null || true
docker rmi compose-demo-web compose-demo-api 2>/dev/null || true
```

```sh {"name":"cleanup-verify","interactive":"false","closeTerminalOnSuccess":"false","excludeFromRunAll":"true"}
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
