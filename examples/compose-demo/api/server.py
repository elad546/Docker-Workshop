import os
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer

import redis

REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
REDIS_PORT = int(os.environ.get("REDIS_PORT", "6379"))


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/health":
            self.send_response(404)
            self.end_headers()
            return

        try:
            client = redis.Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                decode_responses=True,
                socket_connect_timeout=3,
            )
            client.ping()
            hits = client.incr("health_checks")
            body = f'{{"status":"ok","hostname":"{socket.gethostname()}","redis_hits":{hits}}}'
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(body.encode())
        except redis.RedisError as exc:
            body = f'{{"status":"error","message":"{exc}"}}'
            self.send_response(503)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(body.encode())

    def log_message(self, format, *args):
        pass


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 5000), HealthHandler)
    print("API listening on port 5000")
    server.serve_forever()
