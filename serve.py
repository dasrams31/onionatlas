#!/usr/bin/env python3
"""OnionAtlas static server: HTTP/1.1 keep-alive + gzip for fast Tor delivery."""

import gzip
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
PORT = 18097

MIMES = {".html": "text/html; charset=utf-8",
         ".css": "text/css; charset=utf-8",
         ".js": "text/javascript; charset=utf-8",
         ".png": "image/png", ".jpg": "image/jpeg",
         ".svg": "image/svg+xml", ".ico": "image/x-icon"}


class Handler(BaseHTTPRequestHandler):
    server_version = "OnionAtlas/1.0"
    protocol_version = "HTTP/1.1"

    def do_GET(self):
        self.serve()

    def do_HEAD(self):
        self.serve()

    def serve(self):
        path = urlparse(self.path).path
        if path == "/":
            path = "/index.html"
        # prevent traversal
        fpath = os.path.normpath(os.path.join(BASE, path.lstrip("/")))
        if not fpath.startswith(BASE) or not os.path.isfile(fpath):
            self.send_response(404)
            self.send_header("Content-Length", "9")
            self.end_headers()
            self.wfile.write(b"not found")
            return
        ext = os.path.splitext(fpath)[1].lower()
        ctype = MIMES.get(ext, "application/octet-stream")
        with open(fpath, "rb") as f:
            data = f.read()
        enc = None
        if (ctype.startswith("text/") or "javascript" in ctype
                or "svg" in ctype) and len(data) >= 512 \
                and "gzip" in self.headers.get("Accept-Encoding", ""):
            data = gzip.compress(data, compresslevel=6)
            enc = "gzip"
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "public, max-age=3600")
        if enc:
            self.send_header("Content-Encoding", enc)
            self.send_header("Vary", "Accept-Encoding")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(data)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print("OnionAtlas on 127.0.0.1:%d" % PORT, flush=True)
    srv.serve_forever()
