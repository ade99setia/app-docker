"""
Face Scan Camera Forwarder (Debug Version)
==========================================
- Menerima webhook dari kamera VIID
- Debug raw payload & parsed payload
- Forward ke API
"""

import json
import os
import socket
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config_env import load_env_file

load_env_file()

# ── Konfigurasi ──────────────────────────────────────────────────────────────
LISTEN_HOST = os.getenv("LISTEN_HOST", "0.0.0.0")
LISTEN_PORT = int(os.getenv("LISTEN_PORT", "8089"))

FORWARD_WEBHOOK_URL = os.getenv(
    "FORWARD_WEBHOOK_URL",
    "https://idnsolo.com/api/iot/face-scan-camera/auth/3/lFFkMi04oXwuAETrQwVEbQBjMqNuY3hZuWXTD4YGa0d0ee7f",
)

WEBHOOK_TIMEOUT = (
    int(os.getenv("WEBHOOK_CONNECT_TIMEOUT", "5")),
    int(os.getenv("WEBHOOK_READ_TIMEOUT", "30")),
)

FINAL_ERROR_STATUS_CODES = {
    int(c.strip())
    for c in os.getenv("FINAL_ERROR_STATUS_CODES", "409,422").split(",")
    if c.strip()
}

# 🔥 DEBUG MODE
DEBUG = os.getenv("DEBUG", "true").lower() == "true"


# ── Helper Debug Print ───────────────────────────────────────────────────────
def debug_print(title: str, data):
    if not DEBUG:
        return
    print(f"\n===== {title} =====")
    if isinstance(data, (dict, list)):
        print(json.dumps(data, indent=2))
    else:
        print(data)
    print("=" * 40)


# ── HTTP Session dengan retry ────────────────────────────────────────────────
def _build_session() -> requests.Session:
    retry = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=(502, 503, 504),
        allowed_methods=frozenset({"POST"}),
        raise_on_status=False,
    )
    session = requests.Session()
    session.headers.update({"User-Agent": "face-scan-camera-forwarder/1.0"})
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


WEBHOOK_SESSION = _build_session()


# ── Ekstrak PersonID ─────────────────────────────────────────────────────────
def extract_persons(data: dict) -> list[dict]:
    persons = []

    try:
        recognition_list = data.get("PersonRecognitionResultListObject", {})
        objects = recognition_list.get("PersonRecognitionObject", [])

        if isinstance(objects, dict):
            objects = [objects]

        for obj in objects:
            person_id = obj.get("PersonID", "").strip()
            if not person_id or person_id == "-1":
                continue

            persons.append(
                {
                    "person_id": person_id,
                    "name": obj.get("Name", ""),
                    "group_id": obj.get("GroupID", ""),
                    "device_id": obj.get("DeviceID", ""),
                    "similarity": obj.get("Similarity", ""),
                    "recognition_time": obj.get("RecognitionTime", ""),
                }
            )
    except Exception as exc:
        print(f"[WARN] Gagal ekstrak persons: {exc}")

    return persons


# ── Forward ke API ───────────────────────────────────────────────────────────
def forward_to_webhook(persons: list[dict]) -> None:
    if not persons:
        return

    debug_print("PAYLOAD KE API", persons)

    try:
        resp = WEBHOOK_SESSION.post(
            FORWARD_WEBHOOK_URL,
            json=persons,
            timeout=WEBHOOK_TIMEOUT,
        )
        resp.raise_for_status()
        print(f"[OK] Forward {len(persons)} person(s) → status {resp.status_code}")
    except requests.RequestException as exc:
        resp = getattr(exc, "response", None)
        status = resp.status_code if resp is not None else "N/A"

        if resp is not None and resp.status_code in FINAL_ERROR_STATUS_CODES:
            print(f"[SKIP] Status {status} dianggap final, tidak retry.")
        else:
            print(f"[ERROR] Gagal forward: {exc}")


# ── HTTP Handler ─────────────────────────────────────────────────────────────
class CameraWebhookHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass  # disable default log

    def _read_body(self) -> dict | None:
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length) if length > 0 else b""

        if not raw:
            return None

        # 🔥 RAW BODY STRING
        debug_print("RAW BODY (STRING)", raw.decode("utf-8", errors="replace"))

        try:
            parsed = json.loads(raw.decode("utf-8", errors="replace"))
            debug_print("PARSED JSON", parsed)
            return parsed
        except json.JSONDecodeError:
            print("[ERROR] JSON tidak valid")
            return None

    def _respond(self, status: int, body: dict) -> None:
        payload = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/VIID+JSON;charset=utf8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_POST(self):
        path = self.path.rstrip("/")
        data = self._read_body() or {}

        ts = time.strftime("%H:%M:%S")
        print(f"\n[{ts}] POST {path} dari {self.client_address[0]}")

        # Register / Keepalive
        if path in ("/VIID/System/Register", "/VIID/System/Keepalive"):
            device_id = (
                data.get("RegisterObject", {}).get("DeviceID")
                or data.get("KeepaliveObject", {}).get("DeviceID")
                or "unknown"
            )

            print(f"  → Device register/keepalive: {device_id}")

            self._respond(
                200,
                {
                    "ResponseStatusObject": {
                        "RequestURL": path,
                        "StatusCode": 0,
                        "StatusString": "success",
                        "ID": device_id,
                    }
                },
            )
            return

        # Face recognition
        if path in (
            "/VIID/Extend/ExtendFaceRecognition",
            "/VIID/Face/Pass",
        ):
            persons = extract_persons(data)

            if persons:
                ids = [p["person_id"] for p in persons]
                print(f"  → PersonID terdeteksi: {ids}")
                forward_to_webhook(persons)
            else:
                print("  → Tidak ada PersonID valid")

            self._respond(
                200,
                {
                    "ResponseStatusObject": {
                        "RequestURL": path,
                        "StatusCode": 0,
                        "StatusString": "success",
                    }
                },
            )
            return

        # Catch-all
        print("  → Path tidak dikenal")
        self._respond(200, {"RetCode": 0, "StatusString": "captured"})

    def do_GET(self):
        self._respond(200, {"status": "face-scan-camera-forwarder running"})


# ── Main ─────────────────────────────────────────────────────────────────────
def get_local_ips() -> list[str]:
    """Ambil semua IP lokal yang aktif di mesin ini."""
    ips = []
    try:
        # Cara paling portable: buka UDP dummy, lihat IP yang dipakai
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            ips.append(s.getsockname()[0])
    except Exception:
        pass

    # Fallback: hostname resolution
    try:
        hostname = socket.gethostname()
        for info in socket.getaddrinfo(hostname, None):
            ip = info[4][0]
            if ip not in ips and not ip.startswith("127.") and ":" not in ip:
                ips.append(ip)
    except Exception:
        pass

    return ips if ips else ["<tidak terdeteksi>"]


def is_running_in_docker() -> bool:
    """Deteksi apakah script berjalan di dalam Docker container."""
    return (
        os.path.exists("/.dockerenv")
        or os.environ.get("container") == "docker"
    )


def main() -> None:
    server = HTTPServer((LISTEN_HOST, LISTEN_PORT), CameraWebhookHandler)

    local_ips = get_local_ips()
    in_docker = is_running_in_docker()

    print("=" * 55)
    print("  Face Scan Camera Forwarder")
    print("=" * 55)
    print(f"  Mode    : {'🐳 Docker (network_mode: host)' if in_docker else '🐍 Python langsung'}")
    print(f"  Listen  : http://0.0.0.0:{LISTEN_PORT}")
    print(f"  Forward : {FORWARD_WEBHOOK_URL}")
    print(f"  Debug   : {DEBUG}")
    print("-" * 55)
    print("  📡 Pasang IP berikut di pengaturan kamera (IoT):")
    for ip in local_ips:
        print(f"     Server IP   : {ip}")
        print(f"     Server Port : {LISTEN_PORT}")
        print(f"     Upload Path : /VIID/Extend/ExtendFaceRecognition")
    if in_docker:
        print()
        print("  ℹ️  Docker: IP di atas adalah IP host (karena network_mode: host)")
        print("     Kamera di LAN bisa langsung menjangkau port ini.")
    print("=" * 55)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer dihentikan.")


if __name__ == "__main__":
    main()