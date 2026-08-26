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

Module 0 below installs Docker (Engine, Buildx, and Compose), and fixes socket permissions if needed.

> Cells that use `sudo` run in **interactive** mode — enter your password when prompted.

## Module 0: Prerequisites

Install Docker, verify it works, and fix permission errors if needed.

### Install Docker

```sh {"name":"Install Docker packages","tag":"prerequisites","terminalRows":"8","interactive":"true"}
sudo apt update && sudo apt install -y docker.io docker-buildx
```

```sh {"name":"Install Compose v2 plugin","tag":"prerequisites","terminalRows":"6","interactive":"true"}
sudo apt install -y docker-compose-v2
sudo apt install -y docker-compose-plugin 2>/dev/null || true
```

```sh {"name":"Enable Docker service","tag":"prerequisites","terminalRows":"3","interactive":"true"}
sudo systemctl start docker && sudo systemctl enable docker
```

```sh {"name":"Verify Buildx","tag":"prerequisites","terminalRows":"2","interactive":"false"}
docker buildx version
```

### Install Compose plugin

Docker 29.x uses Compose **v2** as a CLI plugin — run `docker compose` (with a space), not the legacy `docker-compose` command. The cell above installs the Ubuntu package (`docker-compose-v2`) and, when available, Docker's official package (`docker-compose-plugin`). This cell verifies it works and applies a download fallback if the plugin is still missing.

```sh {"name":"Ensure Compose plugin","tag":"prerequisites","terminalRows":"10","interactive":"true"}
if ! docker compose version >/dev/null 2>&1; then
  sudo apt install -y docker-compose-v2 2>/dev/null || sudo apt install --reinstall -y docker-compose-v2
fi
if ! docker compose version >/dev/null 2>&1; then
  mkdir -p ~/.docker/cli-plugins
  curl -fsSL "https://github.com/docker/compose/releases/download/v2.40.3/docker-compose-linux-$(uname -m)" -o ~/.docker/cli-plugins/docker-compose
  chmod +x ~/.docker/cli-plugins/docker-compose
fi
docker compose version
```

### Verify Docker

```sh {"name":"Docker version","tag":"prerequisites","terminalRows":"2","interactive":"false"}
docker --version
```

```sh {"name":"Docker daemon info","tag":"prerequisites","terminalRows":"6","interactive":"false"}
docker info --format '{{.ServerVersion}}' 2>/dev/null || docker info | head -5
```

### Fix: permission denied

If the **Docker daemon info** cell shows `permission denied while trying to connect to the docker API at unix:///var/run/docker.sock`:

```sh {"name":"Fix docker socket permissions","tag":"prerequisites","terminalRows":"4","interactive":"true"}
sudo chown $USER /var/run/docker.sock
```

⬆️ **Re-run the Docker daemon info cell** — it should work immediately.

> **Optional (permanent fix):** Add your user to the `docker` group with `sudo usermod -aG docker $USER`, then log out and back in. After that you won't need the `chown` step above (until Docker restarts the socket).

### Fix: compose not found

If **Ensure Compose plugin** prints `docker: 'compose' is not a docker command`:

1. Re-run **Ensure Compose plugin** — the apt reinstall or download fallback should fix it.
2. Confirm with `docker compose version` (should show v2.x).
3. If you installed Docker from Docker's official apt repo instead of Ubuntu's `docker.io`, run: `sudo apt install -y docker-compose-plugin`, then re-run **Ensure Compose plugin**.

⬆️ **Do not skip this** — Module 5 requires `docker compose`.

## Module 1: Creating an Image

A **Dockerfile** describes how to build an image. Inspect `examples/hello-docker/`.

### Build the image

The `-t` flag tags the image. `--load` saves the image locally. Docker caches each instruction as a **layer**.

```sh {"name":"Set up Buildx builder","tag":"create-image","terminalRows":"3","interactive":"false"}
docker buildx create --use --name workshop-builder 2>/dev/null || docker buildx use workshop-builder
```

```sh {"name":"Build hello-docker image","tag":"create-image","terminalRows":"12","interactive":"false"}
cd examples/hello-docker && docker buildx build --load -t hello-docker:1.0 .
```

### List the new image

```sh {"name":"List hello-docker images","tag":"create-image","terminalRows":"4","interactive":"false"}
docker images hello-docker
```

## Module 2: Docker Run and Exec

`docker run` starts a container. `docker exec` runs a command inside it.

### Start a container

`-d` detached, `--name hello` names the container, `-p 8080:80` maps port 8080.

```sh {"name":"Run hello container","tag":"run-exec","terminalRows":"2","interactive":"false"}
docker run -d --name hello -p 8080:80 hello-docker:1.0
```

### List containers

```sh {"name":"List running containers","tag":"run-exec","terminalRows":"5","interactive":"false"}
docker ps
```

```sh {"name":"List all containers","tag":"run-exec","terminalRows":"6","interactive":"false"}
docker ps -a
```

### Verify the app

```sh {"name":"curl hello app","tag":"run-exec","terminalRows":"5","interactive":"false"}
curl -s localhost:8080
```

### Exec (non-interactive)

```sh {"name":"Exec cat index.html","tag":"run-exec","terminalRows":"6","interactive":"false"}
docker exec hello cat /usr/share/nginx/html/index.html
```

### Exec (interactive shell)

Try `hostname` or `ls /usr/share/nginx/html`, then type `exit`.

```sh {"name":"Exec interactive shell","tag":"run-exec","terminalRows":"8","interactive":"true"}
docker exec -it hello sh
```

### View logs

```sh {"name":"View container logs","tag":"run-exec","terminalRows":"6","interactive":"false"}
docker logs hello
```

<details>
<summary>Module 3: Commit an Image (optional)</summary>

`docker commit` saves a container filesystem as a new image.

### Create a marker file

```sh {"name":"Create marker file","tag":"commit","terminalRows":"2","interactive":"false"}
docker exec hello sh -c 'echo "committed-layer" > /tmp/marker'
```

### Commit the container

```sh {"name":"Commit container to image","tag":"commit","terminalRows":"2","interactive":"false"}
docker commit hello hello-docker:committed
```

### Compare images

```sh {"name":"List committed images","tag":"commit","terminalRows":"5","interactive":"false"}
docker images hello-docker
```

### Verify the committed image

```sh {"name":"Verify marker in image","tag":"commit","terminalRows":"2","interactive":"false"}
docker run --rm hello-docker:committed cat /tmp/marker
```

</details>

## Module 4: Container and Image Management

Manage lifecycle with `stop`, `start`, `rm`, and `rmi`.

### Stop and start

```sh {"name":"Stop hello container","tag":"manage","terminalRows":"2","interactive":"false"}
docker stop hello
```

```sh {"name":"List stopped container","tag":"manage","terminalRows":"4","interactive":"false"}
docker ps -a --filter name=hello
```

```sh {"name":"Start hello container","tag":"manage","terminalRows":"2","interactive":"false"}
docker start hello
```

```sh {"name":"List running hello","tag":"manage","terminalRows":"4","interactive":"false"}
docker ps --filter name=hello
```

### Remove the container

Run when ready — permanently removes `hello`.

```sh {"name":"Remove hello container","tag":"manage","terminalRows":"2","interactive":"false"}
docker rm -f hello
```

### Remove an image

Run after the container is removed.

```sh {"name":"Remove hello-docker 1.0","tag":"manage","terminalRows":"2","interactive":"false"}
docker rmi hello-docker:1.0
```

### List images

```sh {"name":"List hello-docker tags","tag":"manage","terminalRows":"4","interactive":"false"}
docker image ls hello-docker
```

### Prune unused images (optional)

```sh {"name":"Prune dangling images","tag":"manage","terminalRows":"3","interactive":"false"}
docker image prune -f
```

## Module 5: Docker Compose with Bridge Networks

Multi-container apps with **bridge** networks. Inspect `examples/compose-demo/`.

> Requires `docker compose version` to succeed (Module 0). Re-run **Ensure Compose plugin** if needed.

### Validate compose file

```sh {"name":"Validate compose config","tag":"compose","terminalRows":"8","interactive":"false"}
cd examples/compose-demo && docker compose config
```

### Networks before starting

```sh {"name":"List networks before","tag":"compose","terminalRows":"6","interactive":"false"}
docker network ls
```

### Start all services

```sh {"name":"Start compose stack","tag":"compose","terminalRows":"10","interactive":"false"}
cd examples/compose-demo && docker compose up -d --build --wait
```

### Inspect bridge networks

```sh {"name":"List compose networks","tag":"compose","terminalRows":"5","interactive":"false"}
docker network ls --filter name=compose-demo
```

```sh {"name":"Inspect frontend network","tag":"compose","terminalRows":"2","interactive":"false"}
docker network inspect compose-demo_frontend --format '{{.Driver}}: {{range .Containers}}{{.Name}} {{end}}'
```

### Test the web front-end

```sh {"name":"curl compose web","tag":"compose","terminalRows":"5","interactive":"false"}
curl -s localhost:8081
```

### Test API through nginx proxy

Run a few times — `redis_hits` should increment.

```sh {"name":"curl API health","tag":"compose","terminalRows":"2","interactive":"false"}
curl -s localhost:8081/api/health
```

### List compose services

```sh {"name":"List compose services","tag":"compose","terminalRows":"5","interactive":"false"}
cd examples/compose-demo && docker compose ps
```

### Tear down compose stack

```sh {"name":"Stop compose stack","tag":"compose","terminalRows":"6","interactive":"false"}
cd examples/compose-demo && docker compose down --volumes --remove-orphans
```

## Module 6: Final Cleanup

Remove leftover workshop containers and images.

### Cleanup

```sh {"name":"Remove workshop containers","tag":"cleanup","terminalRows":"4","interactive":"false"}
docker rm -f hello 2>/dev/null || true
docker compose -f examples/compose-demo/docker-compose.yml down --volumes --remove-orphans 2>/dev/null || true
```

```sh {"name":"Remove workshop images","tag":"cleanup","terminalRows":"4","interactive":"false"}
docker rmi hello-docker:1.0 hello-docker:committed 2>/dev/null || true
docker rmi compose-demo-web compose-demo-api 2>/dev/null || true
```

```sh {"name":"Verify cleanup","tag":"cleanup","terminalRows":"4","interactive":"false"}
echo "Remaining workshop containers:" && docker ps -a --filter name=hello --filter name=compose-demo --format '{{.Names}}' | grep -E 'hello|compose-demo' || echo "(none)"
echo "Remaining workshop images:" && docker images --format '{{.Repository}}:{{.Tag}}' | grep -E 'hello-docker|compose-demo' || echo "(none)"
```

## Congratulations!

You covered building images, running containers, exec, commit, management, and Docker Compose.

**Challenge:** Modify `examples/hello-docker/app/index.html`, rebuild, and run a new container.
