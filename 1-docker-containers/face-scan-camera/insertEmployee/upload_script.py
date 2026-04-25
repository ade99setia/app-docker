import pandas as pd
import requests
import os
import json

# --- KONFIGURASI PERANGKAT ---
TARGET_IP = "192.168.1.200"
USER_LOGIN = "admin"
PASS_LOGIN = "Ande*0903"

# --- KONFIGURASI FILE ---
EXCEL_FILE = "data_students.xlsx"
PHOTO_SUBFOLDER = "student_photos"

class DeviceBot:
    def __init__(self, ip, username, password):
        self.base_url = f"http://{ip}/cgi-bin/vs_cgi_v2"
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.token = None

    def login(self):
        """Otomatis mendapatkan token sesuai standar perangkat Anda"""
        print(f"--- Mencoba login ke {TARGET_IP} ---")
        
        # Payload login menggunakan 'pass' (sesuai DevTools)
        login_data = {
            "user": self.username, 
            "pass": self.password
        }
        
        try:
            # Mengirim sebagai form-data (application/x-www-form-urlencoded)
            response = self.session.post(
                f"{self.base_url}?act=login", 
                data=login_data, 
                timeout=10
            )
            
            # Cek token di dalam Cookie
            if "token" in self.session.cookies:
                self.token = self.session.cookies["token"]
                print(f"Login Berhasil! Token: {self.token}")
                return True
            
            # Cek token di dalam Response Body
            try:
                res_json = response.json()
                if "token" in res_json:
                    self.token = res_json["token"]
                    print("Login Berhasil! (Token dari JSON)")
                    return True
            except:
                pass
                
            print(f"Gagal login. Response: {response.text}")
            return False
        except Exception as e:
            print(f"Error Koneksi Login: {e}")
            return False

    def process_person(self, p_id, p_name, p_group, photo_path):
        """Langkah 1: Upload Foto (Binary), Langkah 2: Set Data (JSON)"""
        headers = {
            'Cookie': f'token={self.token}',
            'x-access-token': self.token,
            'User-Agent': 'Mozilla/5.0'
        }

        try:
            # --- STEP 1: UPLOAD FOTO (BINARY) ---
            with open(photo_path, 'rb') as f:
                img_binary = f.read()
            
            headers_photo = headers.copy()
            headers_photo['Content-Type'] = 'application/octet-stream'
            
            resp_img = self.session.post(
                f"{self.base_url}?act=face_upload", 
                data=img_binary, 
                headers=headers_photo,
                timeout=20
            )

            if resp_img.status_code == 200:
                # --- STEP 2: SET DATA PERSON (JSON) ---
                # Payload persis sesuai temuan di DevTools Anda
                payload_info = {
                    "person_id": str(p_id),
                    "person_name": p_name,
                    "person_group": p_group
                }
                
                headers_json = headers.copy()
                headers_json['Content-Type'] = 'application/json'
                
                resp_info = self.session.post(
                    f"{self.base_url}?act=cfg_face_set", 
                    json=payload_info, 
                    headers=headers_json,
                    timeout=10
                )
                
                if resp_info.status_code == 200:
                    return True, resp_info.text
            
            return False, f"Upload Foto Gagal (Status: {resp_img.status_code})"
        except Exception as e:
            return False, str(e)

def run():
    # Inisialisasi Bot
    bot = DeviceBot(TARGET_IP, USER_LOGIN, PASS_LOGIN)
    
    # Validasi File Excel
    if not os.path.exists(EXCEL_FILE):
        print(f"Error: File {EXCEL_FILE} tidak ditemukan!")
        return

    # Jalankan Login & Proses
    if bot.login():
        try:
            df = pd.read_excel(EXCEL_FILE)
        except Exception as e:
            print(f"Error membaca Excel: {e}")
            return
        
        print(f"Ditemukan {len(df)} baris data. Memulai upload...")
        print("-" * 50)

        for index, row in df.iterrows():
            # Mengambil data sesuai header kolom Excel Anda
            p_id = row['person_id']
            p_name = row['person_name']
            p_group = row['person_group']
            p_photo = row['photo_filename']
            
            photo_path = os.path.join(PHOTO_SUBFOLDER, str(p_photo))

            print(f"[{index+1}/{len(df)}] Mengirim {p_name}...", end=" ", flush=True)
            
            if not os.path.exists(photo_path):
                print(f"FAILED (Foto {p_photo} tidak ditemukan)")
                continue

            success, msg = bot.process_person(p_id, p_name, p_group, photo_path)
            if success:
                print("SUCCESS")
            else:
                print(f"FAILED ({msg})")
        
        print("-" * 50)
        print("Proses Selesai.")

if __name__ == "__main__":
    run()