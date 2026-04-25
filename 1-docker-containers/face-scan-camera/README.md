
---

# 📄 Dokumentasi API Server: VIID Face Recognition Camera

## 1. Deskripsi Umum
Sistem ini adalah server *backend* ringan berbasis Python (Flask) yang berfungsi sebagai jembatan (API) untuk menerima, mencatat, dan memproses data dari kamera pengenal wajah (*Face Recognition CCTV*) yang menggunakan protokol **VIID / HTTP**. 

Server ini bertugas untuk:
1. Memberikan respons agar kamera mengenali server sebagai *host* yang valid.
2. Menjaga koneksi kamera agar tetap berstatus *Online*.
3. Menerima data *scan* wajah beserta waktu kejadian (*timestamp*).
4. Mengekstrak gambar wajah (format Base64) dari *payload* JSON dan menyimpannya sebagai file fisik (`.jpg`).
5. Menyimpan riwayat aktivitas (*log*) secara utuh untuk keperluan *debugging* atau integrasi lanjutan ke *database*.

---

## 2. Persyaratan Sistem (Prerequisites)
Sebelum menjalankan *server*, pastikan PC/Server sudah terinstal Python 3.x dan *library* Flask.
Jalankan perintah berikut pada terminal/CMD:
```bash
pip install flask
```

---

## 3. Konfigurasi
* **Port Server:** `3000` (dapat diubah pada baris `app.run(port=3000)`).
* **Host:** `0.0.0.0` (Dapat diakses oleh seluruh *device* di jaringan lokal yang sama).
* **Penyimpanan Log:** `all_logs.json` (File akan otomatis terbuat di direktori utama).
* **Penyimpanan Foto:** Folder `captured_images/` (Akan otomatis terbuat jika belum ada).

---

## 4. Daftar Endpoint API (Routes)

### A. Registrasi Perangkat (Device Registration)
* **URL:** `/VIID/System/Register`
* **Method:** `POST`
* **Fungsi:** Titik masuk pertama bagi kamera. Saat kamera pertama kali dinyalakan atau di-*restart*, kamera akan menembak *endpoint* ini untuk mendaftarkan `DeviceID` miliknya. Server wajib merespons dengan *StatusCode* 0 (Success) agar proses berlanjut.

### B. Pemeliharaan Koneksi (Keepalive / Heartbeat)
* **URL:** `/VIID/System/Keepalive`
* **Method:** `POST`
* **Fungsi:** Kamera akan menembak *endpoint* ini secara berkala (misal: setiap 5-10 detik) untuk memastikan *server* masih hidup. Jika *server* tidak merespons, kamera akan berstatus *Offline* dan berhenti mengirim data wajah.

### C. Penerimaan Data Wajah (Face Recognition Data)
* **URL:** `/VIID/Extend/ExtendFaceRecognition` atau `/VIID/Face/Pass`
* **Method:** `POST`
* **Fungsi:** *Endpoint* utama. Ketika ada seseorang terdeteksi/melakukan *scan* di depan kamera, data (ID Pekerja, Waktu, dan Foto Base64) akan dikirim ke sini.
* **Proses Internal:**
    1. Mencetak JSON ke *console* (teks Base64 disembunyikan agar rapi).
    2. Menyimpan JSON asli ke `all_logs.json`.
    3. Mengubah teks Base64 menjadi file gambar `.jpg` dan menyimpannya di folder `captured_images/`.

### D. *Fallback* (Catch-All Route)
* **URL:** `/*` (Semua *path* yang tidak terdaftar)
* **Method:** `GET`, `POST`
* **Fungsi:** Menangkap *request* "nyasar" dari kamera yang mungkin menggunakan versi VIID berbeda atau menembak *endpoint* selain yang didefinisikan di atas. Berguna untuk *debugging*.

---

## 5. Cara Menjalankan Server

1. Buka Terminal atau *Command Prompt* (CMD) di direktori tempat file `server.py` berada.
2. Jalankan perintah:
   ```bash
   python server.py
   ```
3. Akan muncul tampilan di *console* seperti berikut:
   ```text
   ========================================
   🚀 SERVER MONITORING AKTIF
   📁 Foto akan disimpan di: C:\path\to\your\folder\captured_images
   ========================================
   ```

---

## 6. Pengaturan di Sisi Kamera (Web UI)
Pastikan pengaturan pada web panel administrasi kamera (biasanya diakses via IP Kamera di *browser*) sudah dikonfigurasi sebagai berikut:
* **Protocol:** VIID / HTTP
* **Server IP / Domain:** `IP_ADDRESS_KOMPUTER_KAMU` (contoh: `192.168.1.100`)
* **Server Port:** `3000`
* **Upload Face Image:** Enable / Checklist (agar kamera mengirim foto hasil *scan*).

---

## 7. Penjelasan Fitur *Helper* (Internal)
* **`parse_data()`**: *Parser* pintar yang bisa membaca format `application/json`, `application/x-www-form-urlencoded`, maupun teks mentah (*raw data*). Menghindari *error* jika kamera mengirim *header* yang tidak standar.
* **`mask_long_strings(data)`**: Filter untuk mengganti *string* yang sangat panjang (lebih dari 500 karakter) menjadi teks `<BASE64_DATA_LENGTH_xxx>`. Fitur ini mencegah terminal menjadi *lag* atau macet saat mencetak *log* JSON yang memuat foto.
* **`extract_and_save_images(data)`**: Secara otomatis memindai seluruh bagian JSON untuk mencari pola teks gambar (Base64) dan mengubahnya menjadi file gambar dengan format penamaan yang rapi: `face_TAHUNBULANTANGGAL_JAMMENITDETIK_index.jpg`.