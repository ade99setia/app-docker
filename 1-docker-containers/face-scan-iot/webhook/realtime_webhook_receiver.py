import json
import os
from threading import Lock
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from config_env import load_env_file
from polling_forwarder import fetch_and_process


load_env_file()


LISTEN_HOST = os.getenv("LISTEN_HOST", "0.0.0.0")
LISTEN_PORT = int(os.getenv("LISTEN_PORT", "8088"))
EXPECTED_PATH = os.getenv("EXPECTED_PATH", "/api/hf/hf01")
REALTIME_ACCESS_LOGS = os.getenv("REALTIME_ACCESS_LOGS", "false").strip().lower() in {"1", "true", "yes"}
REALTIME_TRIGGER_LOGS = os.getenv("REALTIME_TRIGGER_LOGS", "false").strip().lower() in {"1", "true", "yes"}
REALTIME_ERROR_LOGS = os.getenv("REALTIME_ERROR_LOGS", "true").strip().lower() in {"1", "true", "yes"}
REALTIME_SYNC_LOCK = Lock()


class FaceScanRealtimeHandler(BaseHTTPRequestHandler):
    server_version = "FaceScanRealtimeReceiver/1.0"

    def log_message(self, format, *args):
        if REALTIME_ACCESS_LOGS:
            print("[%s] %s" % (self.log_date_time_string(), format % args))

    def _write_json(self, status_code, payload):
        encoded = json.dumps(payload).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_POST(self):
        if self.path != EXPECTED_PATH:
            self._write_json(404, {"status": "error", "message": "path not found"})
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(content_length).decode("utf-8") if content_length else ""

        if REALTIME_TRIGGER_LOGS:
            print("--- REALTIME FACE SCAN INCOMING DATA ---")
            print(f"Path: {self.path}")
            print(f"Headers: {dict(self.headers)}")
            print(f"Raw Body: {raw_body}")

        try:
            incoming_payload = json.loads(raw_body) if raw_body else {}
        except json.JSONDecodeError as error:
            self._write_json(400, {"status": "error", "message": f"invalid json: {error}"})
            return

        if REALTIME_TRIGGER_LOGS:
            print(f"Trigger Payload: {incoming_payload}")

        sync_lock_acquired = False

        try:
            sync_lock_acquired = REALTIME_SYNC_LOCK.acquire(blocking=False)
            if not sync_lock_acquired:
                self._write_json(200, {"status": "busy", "message": "sinkronisasi sedang berjalan", "records_count": 0})
                return

            sync_result = fetch_and_process(
                log_start=False,
                log_no_data=False,
                log_cycle_summary=False,
                log_errors=REALTIME_ERROR_LOGS,
                log_success=True,
            )
            if sync_result.get("records_count", 0) > 0 or sync_result.get("status") not in {"ok", "ignored", "skipped", "busy"}:
                print(f"Sync result: {sync_result}")
            self._write_json(
                200,
                {
                    "status": sync_result.get("status", "ok"),
                    "message": sync_result.get("message", "trigger diproses"),
                    "records_count": sync_result.get("records_count", 0),
                },
            )
        except Exception as error:
            if REALTIME_ERROR_LOGS:
                print(f"Trigger handling error: {error}")
            self._write_json(502, {"status": "error", "message": str(error)})
        finally:
            if sync_lock_acquired:
                REALTIME_SYNC_LOCK.release()

    def do_GET(self):
        if self.path == "/health":
            self._write_json(
                200,
                {
                    "status": "ok",
                    "mode": "realtime",
                    "behavior": "trigger webhook lalu ambil database device dan kirim ke Laravel",
                    "expected_path": EXPECTED_PATH,
                },
            )
            return

        self._write_json(404, {"status": "error", "message": "path not found"})


def main():
    httpd = ThreadingHTTPServer((LISTEN_HOST, LISTEN_PORT), FaceScanRealtimeHandler)
    print(f"Realtime receiver listening on http://{LISTEN_HOST}:{LISTEN_PORT}{EXPECTED_PATH}")
    httpd.serve_forever()


if __name__ == "__main__":
    main()