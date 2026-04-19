import pandas as pd
import requests
import os
import base64
import json

# Konfigurasi Target
# TARGET_IP = "192.168.51.249"
TARGET_IP = "10.143.25.66"
URL_ENDPOINT = f"http://{TARGET_IP}/insertEmployee"
EXCEL_FILE = "data_students.xlsx"
PHOTO_SUBFOLDER = "student_photos"

# PASSWORD ANDA DARI SISTEM: "Ande*0903"
SISTEM_PASSWORD = "Ande*0903"

def get_base64_photo(photo_path):
    """Mengonversi file foto ke Data URI (Base64)"""
    try:
        with open(photo_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            return f"data:image/jpeg;base64,{encoded_string}"
    except Exception as e:
        print(f"Error encode base64: {e}")
        return None

def upload_personil():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    excel_path = os.path.join(script_dir, EXCEL_FILE)
    
    if not os.path.exists(excel_path):
        print(f"Error: File {EXCEL_FILE} tidak ditemukan!")
        return

    df = pd.read_excel(excel_path)
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0'
    }

    for index, row in df.iterrows():
        # Kolom Excel: name, ic_card, id_number, photo_filename
        name = str(row['name'])
        ic_card = str(row['ic_card'])
        id_number = str(row['id_number'])
        photo_filename = str(row['photo_filename']) 
        photo_full_path = os.path.join(script_dir, PHOTO_SUBFOLDER, photo_filename)
        
        print(f"[{index+1}] Mengirim: {name}...")

        base64_img = get_base64_photo(photo_full_path)
        
        if base64_img:
            # PAYLOAD FINAL SESUAI KEBUTUHAN PERANGKAT
            payload = {
                "name": name,
                "id_number": id_number,
                "access_card_number": ic_card,
                "password": SISTEM_PASSWORD, # <--- INI KUNCI UTAMANYA
                "role": 0,                   # Tetap angka
                "pass_date": "0",            # Tetap string "0"
                "pass_time": "0",            # Tetap string "0"
                "pic_large": base64_img
            }
            
            try:
                # Kirim sebagai JSON string
                response = requests.post(
                    URL_ENDPOINT, 
                    data=json.dumps(payload), 
                    headers=headers, 
                    timeout=30
                )
                
                # Debugging jika gagal lagi
                if response.status_code != 200:
                    print(f"  ❌ Gagal (Server Error {response.status_code})")
                    continue
                
                try:
                    result = response.json()
                    if result.get('code') == 200:
                        print(f"  ✅ Sukses diunggah ke perangkat!")
                    else:
                        print(f"  ❌ Gagal: {name} (Pesan: {result.get('msg', 'Error ' + str(result.get('code')))})")
                except:
                    print(f"  ❌ Response bukan JSON: {response.text}")
            
            except Exception as e:
                print(f"  ⚠️ Error Koneksi: {e}")
        else:
            print(f"  ❌ File foto tidak terbaca: {photo_full_path}")

if __name__ == "__main__":
    upload_personil()