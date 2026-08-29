"""Disposable HTTP/HTTPS probe for observing the original Futurama client.

This is an archaeology tool, not the replacement game server. It records the
request exactly as received and returns a deliberately simple, configurable
response so protocol hypotheses can be tested one at a time.
"""

from __future__ import annotations

import argparse
import base64
import gzip
import json
import ssl
import sys
import threading
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import BinaryIO


DEFAULT_RESPONSE = b'{"error":"futurama_preservation_probe"}\n'


class RequestRecorder:
    def __init__(self, stream: BinaryIO | None = None) -> None:
        self._stream = stream
        self._lock = threading.Lock()

    def record(self, event: dict[str, object]) -> None:
        encoded = (json.dumps(event, sort_keys=True) + "\n").encode("utf-8")
        with self._lock:
            sys.stdout.buffer.write(encoded)
            sys.stdout.buffer.flush()
            if self._stream is not None:
                self._stream.write(encoded)
                self._stream.flush()


def make_handler(
    recorder: RequestRecorder,
    response_body: bytes = DEFAULT_RESPONSE,
    response_status: int = 503,
    response_content_type: str = "application/json; charset=utf-8",
    response_headers: tuple[tuple[str, str], ...] = (),
) -> type[BaseHTTPRequestHandler]:
    class ProbeHandler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def _handle(self) -> None:
            content_length = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(content_length) if content_length else b""
            try:
                body_text: str | None = body.decode("utf-8")
            except UnicodeDecodeError:
                body_text = None

            recorder.record(
                {
                    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                    "client": self.client_address[0],
                    "method": self.command,
                    "path": self.path,
                    "headers": list(self.headers.items()),
                    "body_length": len(body),
                    "body_utf8": body_text,
                    "body_base64": base64.b64encode(body).decode("ascii"),
                }
            )

            self.send_response(response_status)
            self.send_header("Content-Type", response_content_type)
            self.send_header("Content-Length", str(len(response_body)))
            self.send_header("Connection", "close")
            self.send_header("X-Futurama-Preservation-Probe", "1")
            for name, value in response_headers:
                self.send_header(name, value)
            self.end_headers()
            self.wfile.write(response_body)

        do_GET = _handle
        do_POST = _handle
        do_PUT = _handle
        do_DELETE = _handle
        do_PATCH = _handle

        def log_message(self, format: str, *args: object) -> None:
            return

    return ProbeHandler


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cert",
        type=Path,
        help="PEM certificate. When omitted, the probe serves plain HTTP.",
    )
    parser.add_argument(
        "--key",
        type=Path,
        help="PEM private key. Required when --cert is supplied.",
    )
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=8443, type=int)
    parser.add_argument("--log", type=Path)
    parser.add_argument("--response-file", type=Path)
    parser.add_argument(
        "--gzip-response",
        action="store_true",
        help="gzip the response body and add Content-Encoding: gzip",
    )
    parser.add_argument(
        "--response-header",
        action="append",
        default=[],
        metavar="NAME:VALUE",
        help="additional response header; may be repeated",
    )
    parser.add_argument("--status", default=503, type=int)
    parser.add_argument(
        "--content-type", default="application/json; charset=utf-8"
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if bool(args.cert) != bool(args.key):
        raise SystemExit("--cert and --key must be supplied together")
    response_body = (
        args.response_file.read_bytes() if args.response_file else DEFAULT_RESPONSE
    )
    response_headers: list[tuple[str, str]] = []
    for raw_header in args.response_header:
        if ":" not in raw_header:
            raise SystemExit(f"invalid --response-header: {raw_header!r}")
        name, value = raw_header.split(":", 1)
        response_headers.append((name.strip(), value.strip()))
    if args.gzip_response:
        response_body = gzip.compress(response_body)
        response_headers.append(("Content-Encoding", "gzip"))
    log_stream = args.log.open("ab") if args.log else None
    recorder = RequestRecorder(log_stream)
    handler = make_handler(
        recorder,
        response_body=response_body,
        response_status=args.status,
        response_content_type=args.content_type,
        response_headers=tuple(response_headers),
    )
    server = ThreadingHTTPServer((args.host, args.port), handler)

    scheme = "http"
    if args.cert is not None:
        tls = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        tls.load_cert_chain(args.cert, args.key)
        server.socket = tls.wrap_socket(server.socket, server_side=True)
        scheme = "https"

    print(
        f"Futurama client probe listening on {scheme}://{args.host}:{args.port}",
        flush=True,
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        if log_stream is not None:
            log_stream.close()


if __name__ == "__main__":
    main()
