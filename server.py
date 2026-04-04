"""
StoryForge - Gamebook Engine Server
A data-driven Fighting Fantasy-style gamebook engine.
Serves the client and adventure JSON files over HTTP.
All game state is managed client-side.
"""

import http.server
import json
import os
import threading

HTTP_PORT = 8765
ADVENTURES_DIR = os.path.join(os.path.dirname(__file__), "adventures")


class StoryForgeHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self._serve_file("index.html", "text/html")
        elif self.path == "/api/adventures":
            self._serve_adventure_list()
        elif self.path.startswith("/api/adventures/"):
            adventure_id = self.path[len("/api/adventures/"):]
            self._serve_adventure(adventure_id)
        else:
            rel = self.path.lstrip("/").split("?")[0]
            if rel and ".." not in rel:
                ext = os.path.splitext(rel)[1].lower()
                ct = {
                    ".json":        "application/json",
                    ".js":          "application/javascript",
                    ".png":         "image/png",
                    ".svg":         "image/svg+xml",
                    ".webmanifest": "application/manifest+json",
                    ".html":        "text/html",
                }.get(ext, "application/octet-stream")
                self._serve_file(rel, ct)
            else:
                self.send_error(404, "Not Found")

    def _serve_file(self, filename, content_type):
        filepath = os.path.join(os.path.dirname(__file__), filename)
        try:
            with open(filepath, "rb") as f:
                data = f.read()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", len(data))
            self.end_headers()
            self.wfile.write(data)
        except FileNotFoundError:
            self.send_error(404, f"{filename} not found")

    def _serve_adventure_list(self):
        adventures = []
        if os.path.isdir(ADVENTURES_DIR):
            for filename in sorted(os.listdir(ADVENTURES_DIR)):
                if filename.endswith(".json"):
                    adventure_id = filename[:-5]
                    filepath = os.path.join(ADVENTURES_DIR, filename)
                    try:
                        with open(filepath, "r", encoding="utf-8") as f:
                            data = json.load(f)
                        adventures.append({
                            "id": adventure_id,
                            "title": data.get("title", adventure_id),
                            "author": data.get("author", "Unknown"),
                            "introduction": data.get("introduction", "")
                        })
                    except (json.JSONDecodeError, OSError):
                        pass  # Skip malformed files

        self._send_json(adventures)

    def _serve_adventure(self, adventure_id):
        # Sanitise: only allow alphanumeric, hyphens, underscores
        if not all(c.isalnum() or c in "-_" for c in adventure_id):
            self.send_error(400, "Invalid adventure id")
            return
        filepath = os.path.join(ADVENTURES_DIR, f"{adventure_id}.json")
        if not os.path.isfile(filepath):
            self.send_error(404, "Adventure not found")
            return
        try:
            with open(filepath, "rb") as f:
                data = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", len(data))
            self.end_headers()
            self.wfile.write(data)
        except OSError:
            self.send_error(500, "Failed to read adventure")

    def _send_json(self, obj):
        data = json.dumps(obj).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(data))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, format, *args):
        pass  # Suppress request logging


class StoryForgeServer(http.server.ThreadingHTTPServer):
    allow_reuse_address = True


def main():
    server = StoryForgeServer(("0.0.0.0", HTTP_PORT), StoryForgeHandler)

    print("=" * 50)
    print("  STORYFORGE - Gamebook Engine")
    print("=" * 50)
    print(f"  Open: http://localhost:{HTTP_PORT}")
    print(f"  Adventures: {ADVENTURES_DIR}")
    print("  Press Ctrl+C to stop")
    print("=" * 50)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")


if __name__ == "__main__":
    main()
