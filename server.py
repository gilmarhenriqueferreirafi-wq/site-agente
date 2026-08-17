"""
Servidor HTTP simples pra servir a interface (index.html) no Codespace.
Uso: python server.py
Depois é só abrir a porta 8000 encaminhada pelo Codespace.
"""

import http.server
import socketserver

PORT = 8000


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # libera CORS, caso a interface precise buscar recursos externos
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()


if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Servindo em http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor encerrado.")
