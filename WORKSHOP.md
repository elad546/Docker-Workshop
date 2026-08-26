---
runme:
  id: 01JWORKSHOPDOCKER2026
  version: v3
---

# Docker Basics Interactive Workshop

Welcome! This notebook walks through Docker fundamentals step by step.

**Estimated time:** 30–45 minutes

## Before you start (VS Code)

1. Open this repository in [VS Code](https://code.visualstudio.com/).
2. Install the [Runme extension](vscode:extension/stateful.runme) when prompted (Extensions panel → `Ctrl+Shift+X` → search **Runme**).
3. Open this file — VS Code renders it as a notebook.
4. Click **Run** (▶) on each cell, top to bottom.

Module 0 below installs Docker and fixes socket permissions if needed.

## Module 0: Prerequisites

Install Docker, verify it works, and fix permission errors if needed.

### Install Docker

```sh {"name":"00-install-docker","tag":"module-0","terminalRows":"8"}
sudo apt update && sudo apt install -y docker.io
```

```sh {"name":"00-start-docker","tag":"module-0","terminalRows":"3"}
sudo systemctl start docker && sudo systemctl enable docker
```

### Verify Docker

```sh {"name":"00-docker-version","tag":"module-0","terminalRows":"2"}
docker --version
```

```sh {"name":"00-docker-info","tag":"module-0","terminalRows":"6"}
docker info --format '{{.ServerVersion}}' 2>/dev/null || docker info | head -5
```

### Fix: permission denied

If the **docker info** cell above shows `permission denied while trying to connect to the docker API at unix:///var/run/docker.sock`:

```sh {"name":"00-fix-usermod","tag":"module-0","terminalRows":"6"}
sudo usermod -aG docker $USER
sudo apt install -y util-linux-extra
```

```sh {"name":"00-fix-sg-verify","tag":"module-0","terminalRows":"6"}
sg docker -c "docker info --format '{{.ServerVersion}}' 2>/dev/null || docker info | head -5"
```

Log out of Linux and log back in, reopen VS Code, then **re-run the docker info cell**.

## Module 1: Creating an Image

A **Dockerfile** describes how to build an image. Inspect `examples/hello-docker/` — nginx serving a simple HTML page.

### Build the image

```sh {"name":"01-build-image","tag":"module-1","terminalRows":"12"}
cd examples/hello-docker && docker build -t hello-docker:1.0 .
```

The `-t` flag tags the image. Docker caches each instruction as a **layer**.

### List the new image

```sh {"name":"01-list-image","tag":"module-1","terminalRows":"4"}
docker images hello-docker
```

## Module 2: Docker Run and Exec

`docker run` starts a container. `docker exec` runs a command inside it.

### Start a container

```sh {"name":"02-run-container","tag":"module-2","terminalRows":"2"}
docker run -d --name hello -p 8080:80 hello-docker:1.0
```

`-d` detached, `--name hello` names the container, `-p 8080:80` maps port 8080.

### List containers

```sh {"name":"02-docker-ps","tag":"module-2","terminalRows":"5"}
docker ps
```

```sh {"name":"02-docker-ps-all","tag":"module-2","terminalRows":"6"}
docker ps -a
```

### Verify the app

```sh {"name":"02-curl-app","tag":"module-2","terminalRows":"5"}
curl -s localhost:8080
```

### Exec (non-interactive)

```sh {"name":"02-exec-cat","tag":"module-2","terminalRows":"6"}
docker exec hello cat /usr/share/nginx/html/index.html
```

### Exec (interactive shell)

```sh {"name":"02-exec-shell","tag":"module-2","interactive":"true","terminalRows":"8"}
docker exec -it hello sh
```

Try `hostname` or `ls /usr/share/nginx/html`, then type `exit`.

### View logs

```sh {"name":"02-docker-logs","tag":"module-2","terminalRows":"6"}
docker logs hello
```

## Module 3: Commit an Image

`docker commit` saves a container's filesystem as a new image. Prefer rebuilding from a Dockerfile in production.

### Create a marker file

```sh {"name":"03-create-marker","tag":"module-3","terminalRows":"2"}
docker exec hello sh -c 'echo "committed-layer" > /tmp/marker'
```

### Commit the container

```sh {"name":"03-docker-commit","tag":"module-3","terminalRows":"2"}
docker commit hello hello-docker:committed
```

### Compare images

```sh {"name":"03-list-images","tag":"module-3","terminalRows":"5"}
docker images hello-docker
```

### Verify the committed image

```sh {"name":"03-verify-committed","tag":"module-3","terminalRows":"2"}
docker run --rm hello-docker:committed cat /tmp/marker
```

## Module 4: Container and Image Management

Manage container and image lifecycle with `stop`, `start`, `rm`, and `rmi`.

### Stop and start

```sh {"name":"04-docker-stop","tag":"module-4","terminalRows":"2"}
docker stop hello
```

```sh {"name":"04-ps-after-stop","tag":"module-4","terminalRows":"4"}
docker ps -a --filter name=hello
```

```sh {"name":"04-docker-start","tag":"module-4","terminalRows":"2"}
docker start hello
```

```sh {"name":"04-ps-after-start","tag":"module-4","terminalRows":"4"}
docker ps --filter name=hello
```

### Remove the container

Run when ready — permanently removes `hello`.

```sh {"name":"04-docker-rm","tag":"module-4","terminalRows":"2"}
docker rm -f hello
```

### Remove an image

Run after the container is removed.

```sh {"name":"04-docker-rmi","tag":"module-4","terminalRows":"2"}
docker rmi hello-docker:1.0
```

### List images

```sh {"name":"04-image-ls","tag":"module-4","terminalRows":"4"}
docker image ls hello-docker
```

### Prune unused images (optional)

```sh {"name":"04-image-prune","tag":"module-4","terminalRows":"3"}
docker image prune -f
```

## Module 5: Docker Compose with Bridge Networks

Multi-container apps with custom **bridge** networks and DNS-based service discovery.

Inspect `examples/compose-demo/`: **web** (port 8081), **api**, **redis** on `frontend` / `backend` networks.

### Validate compose file

```sh {"name":"05-compose-config","tag":"module-5","terminalRows":"8"}
cd examples/compose-demo && docker compose config
```

### Networks before starting

```sh {"name":"05-network-ls-before","tag":"module-5","terminalRows":"6"}
docker network ls
```

### Start all services

```sh {"name":"05-compose-up","tag":"module-5","terminalRows":"10"}
cd examples/compose-demo && docker compose up -d --build --wait
```

### Inspect bridge networks

```sh {"name":"05-network-ls-after","tag":"module-5","terminalRows":"5"}
docker network ls --filter name=compose-demo
```

```sh {"name":"05-network-inspect","tag":"module-5","terminalRows":"2"}
docker network inspect compose-demo_frontend --format '{{.Driver}}: {{range .Containers}}{{.Name}} {{end}}'
```

### Test the web front-end

```sh {"name":"05-curl-web","tag":"module-5","terminalRows":"5"}
curl -s localhost:8081
```

### Test API through nginx proxy

```sh {"name":"05-curl-api","tag":"module-5","terminalRows":"2"}
curl -s localhost:8081/api/health
```

Run a few times — `redis_hits` should increment.

### List compose services

```sh {"name":"05-compose-ps","tag":"module-5","terminalRows":"5"}
cd examples/compose-demo && docker compose ps
```

### Tear down compose stack

```sh {"name":"05-compose-down","tag":"module-5","terminalRows":"6"}
cd examples/compose-demo && docker compose down --volumes --remove-orphans
```

## Module 6: Final Cleanup

Remove leftover workshop containers and images.

```sh {"name":"06-cleanup-containers","tag":"module-6","terminalRows":"4"}
docker rm -f hello 2>/dev/null || true
docker compose -f examples/compose-demo/docker-compose.yml down --volumes --remove-orphans 2>/dev/null || true
```

```sh {"name":"06-cleanup-images","tag":"module-6","terminalRows":"4"}
docker rmi hello-docker:1.0 hello-docker:committed 2>/dev/null || true
docker rmi compose-demo-web compose-demo-api 2>/dev/null || true
```

```sh {"name":"06-cleanup-verify","tag":"module-6","terminalRows":"4"}
echo "Remaining workshop containers:" && docker ps -a --filter name=hello --filter name=compose-demo --format '{{.Names}}' | grep -E 'hello|compose-demo' || echo "(none)"
echo "Remaining workshop images:" && docker images --format '{{.Repository}}:{{.Tag}}' | grep -E 'hello-docker|compose-demo' || echo "(none)"
```

## Congratulations!

You covered building images, running containers, exec, commit, management commands, and Docker Compose with bridge networks.

**Challenge:** Modify `examples/hello-docker/app/index.html`, rebuild, and run a new container.
