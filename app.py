import http.server
import socketserver
import webbrowser
import os
import sys

# Set the port
PORT = 8000

# Ensure we are serving from the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

Handler = http.server.SimpleHTTPRequestHandler

try:
    # Custom handler to suppress BrokenPipeError
    class QuietHandler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, format, *args):
            # Suppress logging for favicon.ico 404s if it still happens (optional)
            pass

    class QuietServer(socketserver.TCPServer):
        def handle_error(self, request, client_address):
            # Suppress BrokenPipeError and ConnectionResetError
            exc_type, exc_value, _ = sys.exc_info()
            if issubclass(exc_type, (BrokenPipeError, ConnectionResetError)):
                return
            super().handle_error(request, client_address)

    with QuietServer(("", PORT), Handler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        # Open the browser
        webbrowser.open(f"http://localhost:{PORT}")
        # Keep the server running
        httpd.serve_forever()
except OSError as e:
    if e.errno == 98:
        print(f"Port {PORT} is already in use. Please try a different port or stop the other process.")
    else:
        raise
except KeyboardInterrupt:
    print("\nServer stopped.")
