"""Bounded, single-user loopback laboratory. Not a production server."""
from __future__ import annotations
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlsplit
from .labs import chapters, run_lab
from .util import canonical, integer

WEB=Path(__file__).with_name("web")
ASSETS={"/":("index.html","text/html; charset=utf-8"),"/app.js":("app.js","text/javascript; charset=utf-8"),
        "/style.css":("style.css","text/css; charset=utf-8")}


class Handler(BaseHTTPRequestHandler):
    server_version="NeuroWeave/1.0"
    def log_message(self, *args) -> None:
        pass  # Do not log request bodies or user data.

    def _host_ok(self) -> bool:
        return self.headers.get("Host") in {f"127.0.0.1:{self.server.server_port}", f"localhost:{self.server.server_port}"}

    def _reply(self, code: int, body: bytes, content_type: str="application/json") -> None:
        self.send_response(code)
        self.send_header("Content-Type",content_type)
        self.send_header("Content-Length",str(len(body)))
        self.send_header("X-Content-Type-Options","nosniff")
        self.send_header("Referrer-Policy","no-referrer")
        self.send_header("Cache-Control","no-store")
        self.send_header("Content-Security-Policy","default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; img-src 'self'; frame-ancestors 'none'; base-uri 'none'")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, code: int, obj: dict | list) -> None:
        self._reply(code,canonical(obj).encode())

    def setup(self) -> None:
        super().setup()
        self.connection.settimeout(10)

    def do_GET(self) -> None:
        if not self._host_ok():
            return self._json(403,{"error":"Loopback Host required"})
        path=urlsplit(self.path).path
        if path=="/api/chapters":
            return self._json(200,chapters())
        if path=="/api/health":
            return self._json(200,{"status":"ok","version":"1.0.0","external_actuation":False})
        if path in ASSETS:
            name,kind=ASSETS[path]
            return self._reply(200,(WEB/name).read_bytes(),kind)
        self._json(404,{"error":"Unknown route"})

    def do_POST(self) -> None:
        if not self._host_ok():
            return self._json(403,{"error":"Loopback Host required"})
        origins={f"http://127.0.0.1:{self.server.server_port}",f"http://localhost:{self.server.server_port}"}
        # Browser requests require same-origin; explicit local CLI clients can omit Origin.
        if self.headers.get("Origin") is not None and self.headers.get("Origin") not in origins:
            return self._json(403,{"error":"Cross-origin request denied"})
        if self.headers.get("Sec-Fetch-Site") in {"cross-site","same-site"}:
            return self._json(403,{"error":"Only same-origin browser requests accepted"})
        if urlsplit(self.path).path != "/api/run":
            return self._json(404,{"error":"Unknown route"})
        if self.headers.get("Transfer-Encoding"):
            return self._json(400,{"error":"Chunked requests are not supported"})
        if self.headers.get("Content-Type","").split(";")[0] != "application/json":
            return self._json(415,{"error":"application/json required"})
        try:
            size=int(self.headers.get("Content-Length","0"))
            if not 0<size<=16384:
                return self._json(413,{"error":"Request must contain 1 to 16384 bytes"})
            def bad_number(value): raise ValueError("Nonfinite number")
            data=json.loads(self.rfile.read(size),parse_constant=bad_number)
            if not isinstance(data,dict) or set(data)-{"id","seed","parameters"}:
                raise ValueError("Only id, seed and parameters fields are accepted")
            result=run_lab(data.get("id"),data.get("seed",17),data.get("parameters",{}))
            self._json(200,result)
        except (ValueError,TypeError,KeyError,OverflowError) as exc:
            self._json(400,{"error":str(exc)})


def make_server(port: int=8765) -> HTTPServer:
    integer(port,"port",0,65535)
    return HTTPServer(("127.0.0.1",port),Handler)


def serve(port: int=8765) -> None:
    server=make_server(port)
    print(f"NeuroWeave local laboratory: http://127.0.0.1:{server.server_port}")
    print("Local synthetic research only. Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
