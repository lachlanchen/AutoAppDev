#!/usr/bin/env python3
import argparse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import os


class NoCacheHandler(SimpleHTTPRequestHandler):
    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()


def main() -> None:
    parser = argparse.ArgumentParser(description="Serve the AutoAppDev PWA with no browser caching.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=5173, type=int)
    parser.add_argument("--directory", default=str(Path(__file__).resolve().parents[1] / "pwa"))
    args = parser.parse_args()

    os.chdir(args.directory)
    server = ThreadingHTTPServer((args.host, args.port), NoCacheHandler)
    print(f"Serving AutoAppDev PWA at http://{args.host}:{args.port} from {args.directory}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
