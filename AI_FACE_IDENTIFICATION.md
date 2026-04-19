Tentu, Bro! Ini rangkuman dokumentasi lengkap dari awal (perbaikan database Filebrowser) sampai ke tahap integrasi **AI Face Recognition** ke PC Kubuntu lo. Catatan ini sangat penting buat lo simpan sebagai panduan *troubleshooting* ke depannya.

---

## 📑 Dokumentasi Integrasi Server & AI Face Recognition

### 1. Perbaikan Database Filebrowser (Docker)
**Masalah:** Muncul error `is a directory` saat mencoba menambah user ke Filebrowser karena kesalahan *path* dan *mounting*.
* **Penyebab:** Docker otomatis membuat folder jika file yang di-*mount* tidak ditemukan di *current directory*.
* **Solusi:**
    1. Masuk ke direktori asli database: `cd /idnsolo/server-hosting/filebrowser/`.
    2. Hapus folder sampah: `sudo rm -rf filebrowser.db`.
    3. Jalankan perintah `docker run` tanpa argumen `/filebrowser` tambahan di depan `-d`.

---

### 2. Pengaturan IP Static PC Kubuntu
**Konteks:** Mengunci IP PC agar tidak berubah (Dinamis/DHCP) sehingga perangkat AI selalu bisa menemukan server.
* **Interface:** `wlo1` (WiFi)
* **Koneksi:** "Server"
* **Konfigurasi Locked:**
    * **IP PC:** `192.168.51.250`
    * **Gateway:** `192.168.51.254`
* **Perintah Utama:**
    ```bash
    sudo nmcli connection modify "Server" ipv4.method manual ipv4.addresses 192.168.51.250/24 ipv4.gateway 192.168.51.254 ipv4.dns "1.1.1.1,8.8.8.8"
    sudo nmcli connection up "Server"
    ```

---

### 3. Konfigurasi AI Face Recognition (Hanvon/HY-Access)
**Konteks:** Mengalihkan pengiriman data dari Cloud Pabrikan (`iot.park.hy-access.com`) ke PC Lokal.

#### A. Penyesuaian Alamat di Perangkat:
* **Server URL:** `http://192.168.51.250:18080/zxzl/door-reg`
* **Server IP:** `192.168.51.250`
* **Port:** `18080`

#### B. Pengaturan Firewall (PC Kubuntu):
Membuka "pintu" agar data dari perangkat bisa masuk ke sistem.
```bash
sudo ufw allow 18080/tcp
```

#### C. Pengujian Jalur Data (Listener):
Menggunakan `netcat` untuk memastikan data sampai di PC.
```bash
# nc akan menampilkan data mentah (JSON) yang dikirim perangkat
nc -l -k -p 18080
```

---

### 4. Analisis Data Masuk (Log Temuan)
Dari hasil `nc` tadi, perangkat mengirimkan data **Heartbeat** setiap 20 detik:
* **Format:** JSON
* **Struktur:** `{"device_id":"G013524JZXDD784", "product_key":"uniwin", "time":"1776147927"}`
* **Status:** Koneksi **Stabil**. Perangkat sudah mengenali PC Kubuntu lo sebagai server tujuan.

---

### 5. Rekomendasi Langkah Berikutnya
Karena `nc` hanya bisa melihat data tapi tidak bisa memberikan respon balik ke perangkat:
1.  **Gunakan Python Script:** Jalankan server HTTP sederhana (seperti contoh sebelumnya) untuk memberikan respon `200 OK`. Ini penting agar perangkat tidak menganggap pengiriman gagal.
2.  **Tes Scan Wajah:** Lakukan scan wajah saat `nc` atau script Python berjalan untuk melihat struktur data *record* (absensi) yang lengkap.

---

**Catatan Tambahan:**
Jika sewaktu-waktu perangkat gagal menghubungi domain asli, tambahkan *DNS bypass* di PC lo:
`echo "192.168.51.250 iot.park.hy-access.com" | sudo tee -a /etc/hosts`

Dokumentasi ini sudah cukup lengkap untuk tahap pondasi. Ada bagian spesifik yang mau lo tambahin lagi?