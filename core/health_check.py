"""
Простой HTTP server для Render healthcheck.
Слушает на порту 5000 и предоставляет endpoint для проверки здоровья сервиса.
Работает параллельно со scheduler'ом.
"""

import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import threading
from datetime import datetime

logger = logging.getLogger(__name__)


class HealthCheckHandler(BaseHTTPRequestHandler):
    """Handler для healthcheck запросов."""
    
    def do_GET(self):
        """Обработка GET запросов."""
        if self.path == "/health" or self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            
            health_status = {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "service": "Promotion Hub Scheduler",
            }
            self.wfile.write(json.dumps(health_status).encode())
        else:
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not found"}).encode())
    
    def log_message(self, format, *args):
        """Suppress HTTP server logs."""
        pass


def start_health_check_server(port=5000):
    """
    Запустить HTTP server для healthcheck на отдельном потоке.
    
    Args:
        port: Port для слушания (default 5000)
    """
    try:
        server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
        server_thread = threading.Thread(target=server.serve_forever, daemon=True)
        server_thread.start()
        logger.info(f"✅ Health check server started on port {port}")
        return server
    except Exception as e:
        logger.error(f"❌ Failed to start health check server: {e}")
        return None
