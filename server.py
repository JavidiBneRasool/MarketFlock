# Mini API Server - Enables admin button on website
from http.server import HTTPServer, BaseHTTPRequestHandler
import subprocess, os, json
from datetime import datetime

PROJECT = os.path.dirname(os.path.abspath(__file__))

class FlockHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/run-flock":
            try:
                now = datetime.now().isoformat()
                print(f"{now}: Flock triggered via admin button")
                
                result = subprocess.run(
                    ["python", f"{PROJECT}/run_flock.py"],
                    capture_output=True, text=True, cwd=PROJECT, timeout=180
                )
                
                response = {
                    "success": True,
                    "message": "Flock complete",
                    "time": now
                }
                self.send_response(200)
            except subprocess.TimeoutExpired:
                response = {"success": False, "error": "Timeout"}
                self.send_response(500)
            except Exception as e:
                response = {"success": False, "error": str(e)}
                self.send_response(500)
        else:
            response = {"name": "NewsHour Flock API", "version": "1.0"}
            self.send_response(200)
        
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
    
    def log_message(self, format, *args):
        pass  # Silent

if __name__ == "__main__":
    port = 8765
    print(f"🐑 Flock API Server")
    print(f"   Port: {port}")
    print(f"   Test: curl http://localhost:{port}/api/run-flock")
    print(f"   Keep this running for admin button to work")
    HTTPServer(("0.0.0.0", port), FlockHandler).serve_forever()
