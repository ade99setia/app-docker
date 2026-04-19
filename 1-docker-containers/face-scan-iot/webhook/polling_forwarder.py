import os
import socket
import sqlite3
import tempfile
import time
from threading import Lock
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config_env import load_env_file


load_env_file()


DEVICE_IP = os.getenv("DEVICE_IP", "10.143.25.66")
WEBHOOK_URL = os.getenv(
    "FORWARD_WEBHOOK_URL",
    "https://idnsolo.com/api/iot/face-scan/auth/3/lFFkMi04oXwuAETrQwVEbQBjMqNuY3hZuWXTD4YGa0d0ee7f",
)
PASSWORD = os.getenv("DEVICE_PASSWORD", "Ande*0903")
INTERVAL = int(os.getenv("POLL_INTERVAL_SECONDS", "300"))
LAST_SYNC_FILE = os.getenv("LAST_SYNC_FILE", "last_checkin_time.txt")
DEVICE_CONNECT_TIMEOUT = int(os.getenv("DEVICE_CONNECT_TIMEOUT", "3"))
DEVICE_READ_TIMEOUT = int(os.getenv("DEVICE_READ_TIMEOUT", "20"))
DEVICE_RETRIES = int(os.getenv("DEVICE_RETRIES", "2"))
DEVICE_RETRY_BACKOFF = int(os.getenv("DEVICE_RETRY_BACKOFF", "2"))
SUCCESS_ONLY = os.getenv("SUCCESS_ONLY", "true").strip().lower() not in {"0", "false", "no"}
SUCCESS_FIELD_CANDIDATES = [
    field.strip()
    for field in os.getenv(
        "SUCCESS_FIELD_CANDIDATES",
        "status,result,check_result,check_status,verify_result,verify_status,match_result,match_status,auth_result,auth_status,face_result,face_status,recognition_result,recognition_status",
    ).split(",")
    if field.strip()
]
SUCCESS_VALUES = {
    value.strip().lower()
    for value in os.getenv("SUCCESS_VALUES", "1,true,success,ok,pass,passed,valid,matched").split(",")
    if value.strip()
}
FAILURE_VALUES = {
    value.strip().lower()
    for value in os.getenv("FAILURE_VALUES", "0,false,failed,fail,error,ng,invalid,unmatched,unknown").split(",")
    if value.strip()
}
FINAL_ERROR_STATUS_CODES = {
    int(code.strip())
    for code in os.getenv("FINAL_ERROR_STATUS_CODES", "409,422").split(",")
    if code.strip()
}
WEBHOOK_TIMEOUT = (5, 30)
DEVICE_TIMEOUT = (DEVICE_CONNECT_TIMEOUT, DEVICE_READ_TIMEOUT)
SCRIPT_DIR = Path(__file__).resolve().parent
LAST_SYNC_PATH = SCRIPT_DIR / LAST_SYNC_FILE
SYNC_LOCK = Lock()


def create_session() -> requests.Session:
    retry = Retry(
        total=DEVICE_RETRIES,
        connect=DEVICE_RETRIES,
        read=DEVICE_RETRIES,
        backoff_factor=1,
        status_forcelist=(502, 503, 504),
        allowed_methods=frozenset({"GET", "POST"}),
        raise_on_status=False,
    )

    session = requests.Session()
    session.headers.update({"User-Agent": "face-scan-polling-forwarder/1.0", "Connection": "keep-alive"})
    adapter = HTTPAdapter(max_retries=retry, pool_connections=4, pool_maxsize=4)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


DEVICE_SESSION = create_session()
WEBHOOK_SESSION = requests.Session()
WEBHOOK_SESSION.headers.update({"User-Agent": "face-scan-polling-forwarder/1.0", "Connection": "keep-alive"})


def get_last_synced_time() -> int:
    if LAST_SYNC_PATH.exists():
        with LAST_SYNC_PATH.open("r", encoding="utf-8") as file_handle:
            content = file_handle.read().strip()
            return int(content) if content else 0
    return 0


def save_last_synced_time(timestamp: int) -> None:
    with LAST_SYNC_PATH.open("w", encoding="utf-8") as file_handle:
        file_handle.write(str(timestamp))


def normalize_status_value(value) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value).strip().lower()


def is_successful_record(record: dict) -> bool:
    if not SUCCESS_ONLY:
        return True

    for field_name in SUCCESS_FIELD_CANDIDATES:
        if field_name not in record:
            continue

        normalized_value = normalize_status_value(record.get(field_name))
        if normalized_value in SUCCESS_VALUES:
            return True
        if normalized_value in FAILURE_VALUES:
            return False

    return True


def is_device_reachable() -> bool:
    try:
        with socket.create_connection((DEVICE_IP, 80), timeout=DEVICE_CONNECT_TIMEOUT):
            return True
    except OSError:
        return False


def parse_checkin_db(db_file: str, last_time: int, log_errors: bool = True) -> list[dict]:
    new_records = []
    try:
        connection = sqlite3.connect(db_file)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        query = "SELECT * FROM checkin WHERE check_in_time > ? AND userid != '-1' ORDER BY check_in_time ASC"
        cursor.execute(query, (last_time,))
        for row in cursor.fetchall():
            record = dict(row)
            if is_successful_record(record):
                new_records.append(record)
        connection.close()
    except Exception as error:
        if log_errors:
            print(f"Error parsing SQLite: {error}")
    return new_records


def export_log_database(log_errors: bool = True) -> str | None:
    if not is_device_reachable():
        if log_errors:
            print(f"Device {DEVICE_IP} tidak bisa dijangkau. Lewati siklus ini.")
        return None

    for attempt in range(1, DEVICE_RETRIES + 2):
        try:
            response = DEVICE_SESSION.post(
                f"http://{DEVICE_IP}/exportLogFile",
                json={"password": PASSWORD, "type": 1},
                timeout=DEVICE_TIMEOUT,
            )
            response.raise_for_status()

            payload = response.json()
            db_url = payload.get("url")
            if not db_url:
                print("Response exportLogFile tidak mengandung URL database.")
                return None

            if db_url.startswith("/"):
                return f"http://{DEVICE_IP}{db_url}"

            return db_url.replace(f"http://{DEVICE_IP}", f"http://{DEVICE_IP}")
        except (requests.RequestException, ValueError) as error:
            if log_errors:
                print(f"Export attempt {attempt} gagal: {error}")
            if attempt <= DEVICE_RETRIES:
                time.sleep(DEVICE_RETRY_BACKOFF * attempt)

    return None


def download_db_file(db_url: str, log_errors: bool = True) -> Path | None:
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db", dir=SCRIPT_DIR)
    temp_path = Path(temp_file.name)
    temp_file.close()

    try:
        with DEVICE_SESSION.get(db_url, timeout=DEVICE_TIMEOUT, stream=True) as response:
            response.raise_for_status()
            with temp_path.open("wb") as output_file:
                for chunk in response.iter_content(chunk_size=1024 * 64):
                    if chunk:
                        output_file.write(chunk)
        return temp_path
    except requests.RequestException as error:
        if log_errors:
            print(f"Gagal download database export: {error}")
        if temp_path.exists():
            temp_path.unlink()
        return None


def send_to_webhook(new_data: list[dict], log_errors: bool = True) -> tuple[bool, bool, str]:
    try:
        response = WEBHOOK_SESSION.post(WEBHOOK_URL, json=new_data, timeout=WEBHOOK_TIMEOUT)
        response.raise_for_status()
        return True, True, f"status {response.status_code}"
    except requests.RequestException as error:
        if log_errors:
            print(f"Webhook error: {error}")
        response = getattr(error, "response", None)
        if response is not None and response.status_code in FINAL_ERROR_STATUS_CODES:
            return False, True, f"status {response.status_code} dianggap final"
        return False, False, str(error)


def fetch_and_process(
    log_start: bool = True,
    log_no_data: bool = True,
    log_cycle_summary: bool = True,
    log_errors: bool = True,
    log_success: bool = True,
) -> dict:
    if not SYNC_LOCK.acquire(blocking=False):
        return {
            "status": "busy",
            "message": "sinkronisasi sedang berjalan",
            "records_count": 0,
        }

    cycle_started_at = time.time()
    last_time = get_last_synced_time()
    if log_start:
        print(f"[{time.ctime()}] Checking for new data (Last: {last_time})...")

    temp_db_path = None

    try:
        db_url = export_log_database(log_errors=log_errors)
        if not db_url:
            return {
                "status": "skipped",
                "message": "export url tidak tersedia atau device tidak dapat dijangkau",
                "records_count": 0,
            }

        temp_db_path = download_db_file(db_url, log_errors=log_errors)
        if not temp_db_path:
            return {
                "status": "error",
                "message": "gagal mengunduh database export dari device",
                "records_count": 0,
            }

        new_data = parse_checkin_db(str(temp_db_path), last_time, log_errors=log_errors)

        if not new_data:
            if log_no_data:
                print("No new valid records found.")
            return {
                "status": "ok",
                "message": "tidak ada data baru yang valid",
                "records_count": 0,
            }

        if log_success:
            print(f"Found {len(new_data)} valid records. Sending to Webhook...")
        is_success, should_advance_checkpoint, webhook_message = send_to_webhook(new_data, log_errors=log_errors)
        if is_success:
            if log_success:
                print("Success: Data synced.")
            save_last_synced_time(new_data[-1]["check_in_time"])
            return {
                "status": "ok",
                "message": "data berhasil disinkronkan",
                "records_count": len(new_data),
            }

        if should_advance_checkpoint:
            if log_errors:
                print("Webhook response dianggap final. Checkpoint tetap dimajukan agar data tidak dikirim ulang.")
            save_last_synced_time(new_data[-1]["check_in_time"])
            return {
                "status": "ignored",
                "message": f"data tidak dikirim ulang karena {webhook_message}",
                "records_count": len(new_data),
            }

        return {
            "status": "error",
            "message": f"gagal mengirim data ke webhook tujuan: {webhook_message}",
            "records_count": len(new_data),
        }
    except Exception as error:
        if log_errors:
            print(f"System Error: {error}")
        return {
            "status": "error",
            "message": str(error),
            "records_count": 0,
        }
    finally:
        if temp_db_path and temp_db_path.exists():
            temp_db_path.unlink()

        if log_cycle_summary:
            elapsed = time.time() - cycle_started_at
            print(f"Cycle finished in {elapsed:.1f}s")

        SYNC_LOCK.release()


def main() -> None:
    if not LAST_SYNC_PATH.exists():
        save_last_synced_time(0)

    while True:
        fetch_and_process()
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()