from flask import Flask, request, jsonify
import json
import os
import socket
import base64
import time
import re
from datetime import datetime

app = Flask(__name__)

# --- KONFIGURASI ---
LOG_FILE = "all_logs.json"
IMAGE_DIR = "captured_images"

# Pastikan folder penyimpanan gambar ada
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

# ===============================
# 🛠️ FUNGSI HELPER
# ===============================

def save_log(data):
    """Menyimpan log ke file JSON."""
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            json.dump([], f)

    with open(LOG_FILE, "r+", encoding="utf-8") as f:
        try:
            old = json.load(f)
        except:
            old = []
        old.append(data)
        f.seek(0)
        json.dump(old, f, indent=2, ensure_ascii=False)

def parse_data():
    """Mengambil data request dari berbagai format (JSON, Form, Raw)."""
    try:
        if request.is_json:
            return request.get_json()
        elif request.form:
            return request.form.to_dict()
        else:
            return json.loads(request.data)
    except:
        return {"raw": request.data.decode(errors="ignore")}

def mask_long_strings(data):
    """Menyembunyikan string panjang (Base64) agar tidak memenuhi console."""
    if isinstance(data, dict):
        return {k: mask_long_strings(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [mask_long_strings(v) for v in data]
    elif isinstance(data, str) and len(data) > 500:
        return f"<BASE64_DATA_LENGTH_{len(data)}>"
    return data

def extract_and_save_images(data):
    """Mencari string Base64 dalam data dan menyimpannya sebagai file .jpg"""
    try:
        data_str = json.dumps(data)
        # Mencari string yang terlihat seperti Base64 panjang (biasanya gambar)
        base64_strings = re.findall(r'"([A-Za-z0-9+/]{1000,}={0,2})"', data_str)
        
        saved_files = []
        for i, b64_str in enumerate(base64_strings):
            img_data = base64.b64decode(b64_str)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"face_{timestamp}_{i}.jpg"
            filepath = os.path.join(IMAGE_DIR, filename)
            
            with open(filepath, "wb") as f:
                f.write(img_data)
            saved_files.append(filename)
            print(f"✅ Gambar disimpan: {filepath}")
        return saved_files
    except Exception as e:
        print(f"❌ Gagal ekstrak gambar: {e}")
        return []

# ===============================
# 🌐 MIDDLEWARE
# ===============================

@app.before_request
def log_incoming_request():
    print(f"\n{'='*40}")
    print(f"🌐 [{datetime.now().strftime('%H:%M:%S')}] {request.method} -> {request.path}")
    print(f"📡 IP: {request.remote_addr}")

# ===============================
# 🚀 ROUTE VIID (STANDAR PROTOKOL)
# ===============================

@app.route('/VIID/System/Register', methods=['POST'])
def viid_register():
    data = parse_data()
    device_id = data.get("RegisterObject", {}).get("DeviceID", "unknown")
    
    save_log({"type": "REGISTER", "time": str(datetime.now()), "data": data})
    print(f"🔥 Register Device: {device_id}")

    res = jsonify({
        "ResponseStatusObject": {
            "RequestURL": "/VIID/System/Register",
            "StatusCode": 0,
            "StatusString": "success",
            "ID": device_id
        }
    })
    res.headers['Content-Type'] = 'application/VIID+JSON;charset=utf8'
    return res

@app.route('/VIID/System/Keepalive', methods=['POST'])
def viid_keepalive():
    data = parse_data()
    device_id = data.get("KeepaliveObject", {}).get("DeviceID", "unknown")
    
    res = jsonify({
        "ResponseStatusObject": {
            "RequestURL": "/VIID/System/Keepalive",
            "StatusCode": 0,
            "StatusString": "success",
            "ID": device_id
        }
    })
    res.headers['Content-Type'] = 'application/VIID+JSON;charset=utf8'
    return res

@app.route('/VIID/Extend/ExtendFaceRecognition', methods=['POST'])
@app.route('/VIID/Face/Pass', methods=['POST'])
def viid_face_data():
    data = parse_data()
    
    # Cetak versi bersih ke console
    print("📸 Data Wajah Diterima!")
    print(json.dumps(mask_long_strings(data), indent=2))

    # Simpan log asli & ekstrak gambar ke folder
    save_log({"type": "FACE_DATA", "time": str(datetime.now()), "data": data})
    extract_and_save_images(data)

    res = jsonify({
        "ResponseStatusObject": {
            "RequestURL": request.path,
            "StatusCode": 0,
            "StatusString": "success"
        }
    })
    res.headers['Content-Type'] = 'application/VIID+JSON;charset=utf8'
    return res

# ===============================
# ⚠️ CATCH ALL (FALLBACK)
# ===============================

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    data = parse_data()
    save_log({"type": "UNKNOWN_PATH", "path": path, "time": str(datetime.now()), "data": data})
    
    print(f"🚨 Path tidak terdaftar: /{path}")
    return jsonify({"RetCode": 0, "StatusString": "captured"}), 200

# ===============================
# 🚀 RUN SERVER
# ===============================

def get_local_ips() -> list[str]:
    """Ambil semua IP lokal yang aktif di mesin ini."""
    ips = []
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            ips.append(s.getsockname()[0])
    except Exception:
        pass

    try:
        hostname = socket.gethostname()
        for info in socket.getaddrinfo(hostname, None):
            ip = info[4][0]
            if ip not in ips and not ip.startswith("127.") and ":" not in ip:
                ips.append(ip)
    except Exception:
        pass

    return ips if ips else ["<tidak terdeteksi>"]


if __name__ == "__main__":
    PORT = 3000
    local_ips = get_local_ips()

    print("\n" + "=" * 55)
    print("  🚀 SERVER MONITORING AKTIF")
    print("=" * 55)
    print(f"  📁 Foto disimpan di : {os.path.abspath(IMAGE_DIR)}")
    print(f"  🌐 Listen           : http://0.0.0.0:{PORT}")
    print("-" * 55)
    print("  📡 Pasang IP berikut di pengaturan kamera (IoT):")
    for ip in local_ips:
        print(f"     Server IP   : {ip}")
        print(f"     Server Port : {PORT}")
        print(f"     Upload Path : /VIID/Extend/ExtendFaceRecognition")
    print("=" * 55 + "\n")

    app.run(host="0.0.0.0", port=PORT, debug=False)