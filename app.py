from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

HOST = "0.0.0.0"
PORT = 8080
DATA_DIR = Path("/data")
SECRET_FILE = Path("/run/secrets/banner_msg")

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
            return
            
        visits = "sin contador"
        try:
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            visits_file = DATA_DIR / "visits.txt"
            count = int(visits_file.read_text().strip()) if visits_file.exists() else 0
            count += 1
            visits_file.write_text(str(count))
            visits = str(count)
        except Exception:
            pass
            
        secret_msg = ""
        if SECRET_FILE.exists():
            secret_msg = SECRET_FILE.read_text(encoding="utf-8").strip()
            
        html = f"""
        <html><body>
        <h1>Portal EcoVerde Antioquia</h1>
        <p>Servicio web listo para Docker en producción.</p>
        <p>Visitas persistidas: {visits}</p>
        <p>Mensaje secreto cargado: {secret_msg or "no definido"}</p>
        </body></html>
        """
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

HTTPServer((HOST, PORT), Handler).serve_forever()