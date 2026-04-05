
---

# 🚀 DOKUMENTASI: Setup Auto-Deploy (VS Code SFTP + SSH Key)

**Tujuan:** Menghubungkan VS Code di laptop lokal (Windows) ke server Dev (Kubuntu) dan server Prod (Rumahweb) agar setiap kali file di-Save (`Ctrl + S`), kode otomatis terkirim tanpa harus memasukkan *password* dan tanpa perlu Git Commit di tengah jalan.

## 🔒 TAHAP 1: Membuat SSH Key ("Kunci Master") di Laptop
*Tahap ini hanya perlu dilakukan **SATU KALI SEUMUR HIDUP** di laptop Windows Anda.*

1. Buka **PowerShell** atau Terminal bawaan di VS Code.
2. Jalankan perintah ini untuk membuat Kunci Master:
   ```bash
   ssh-keygen -t rsa -b 4096
   ```
3. Saat muncul pertanyaan `Enter file in which to save the key...`, **Tekan Enter** (biarkan *default*).
4. Saat muncul pertanyaan `Enter passphrase...`, **Tekan Enter** (kosongkan agar tidak dimintai password).
5. Saat muncul `Enter same passphrase again`, **Tekan Enter** lagi.
6. **Hasil:** Laptop Anda sekarang memiliki kunci rahasia di folder `C:\Users\asus_\.ssh\id_rsa`.

---

## 🔑 TAHAP 2: Memasang "Gembok" (Public Key) ke Server Target
*Tujuannya agar server mengenali laptop kita dan mengizinkan masuk tanpa password di kemudian hari. Lakukan tahap ini di **PowerShell**.*

### A. Untuk Server Kubuntu (Development)
Jalankan perintah ini:
```powershell
Get-Content ~/.ssh/id_rsa.pub | ssh ade-setia@10.159.76.115 "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```
*(Ketikkan password user Kubuntu Anda ketika diminta. Ingat: ketikan password tidak akan muncul di layar, langsung tekan Enter).*

### B. Untuk Server Rumahweb (Production)
Jalankan perintah ini:
```powershell
Get-Content ~/.ssh/id_rsa.pub | ssh idnq7835@juwana.iixcp.rumahweb.net -p 2223 "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```
*(Ketikkan password cPanel Rumahweb Anda ketika diminta. Proses ini menggantikan fungsi login manual).*

---

## ⚙️ TAHAP 3: Konfigurasi Auto-Upload (SFTP) di VS Code
*Tahap ini dilakukan di setiap project yang ada di dalam VS Code.*

1. Buka project Anda di VS Code.
2. Masuk ke menu **Extensions** (`Ctrl + Shift + X`).
3. Cari dan install extension **SFTP** (Pastikan *author*-nya adalah **Natizyskunk**).
4. Tekan **`Ctrl + Shift + P`**, ketik `SFTP: Config`, lalu Enter.
5. VS Code akan membuat file `sftp.json` di dalam folder `.vscode`. 
6. Isi file tersebut sesuai dengan server tujuan Anda:

### Template `sftp.json` untuk Kubuntu Dev:
```json
{
    "name": "Kubuntu Dev Server",
    "host": "10.159.76.115",
    "protocol": "sftp",
    "port": 22,
    "username": "ade-setia",
    "privateKeyPath": "C:/Users/asus_/.ssh/id_rsa",
    "remotePath": "/home/ade-setia/Development/NAMA_FOLDER_PROJECT_DISINI",
    "uploadOnSave": true,
    "useTempFile": false,
    "openSsh": false,
    "syncOption": {
        "delete": true,
        "skipCreate": false,
        "update": false
    },
    "ignore": [
        "**/.vscode/**",
        "**/.git/**",
        "**/.DS_Store",
        "**/node_modules/**",
        "**/vendor/**",
        "**/*.bat",
        "**/*.zip"
    ]
}
```

### Template `sftp.json` untuk Rumahweb Prod:
```json
{
    "name": "Rumahweb Prod",
    "host": "juwana.iixcp.rumahweb.net",
    "protocol": "sftp",
    "port": 2223,
    "username": "idnq7835",
    "privateKeyPath": "C:/Users/asus_/.ssh/id_rsa",
    "remotePath": "/home/idnq7835/NAMA_FOLDER_PROJECT_DISINI",
    "uploadOnSave": true,
    "useTempFile": false,
    "openSsh": false,
    "ignore": [
        "**/.vscode/**",
        "**/.git/**",
        "**/.DS_Store",
        "**/node_modules/**",
        "**/vendor/**",
        "**/*.bat",
        "**/*.zip"
    ]
}
```
*(Jangan lupa ganti `NAMA_FOLDER_PROJECT_DISINI` dengan folder yang sesuai di server).*

---

## 💻 TAHAP 4: Cara Penggunaan Sehari-hari (Workflow)

* **Auto Upload:** Buka file apa saja, edit, lalu tekan **`Ctrl + S`**. Perhatikan di pojok kiri bawah VS Code, akan muncul tulisan *SFTP: Uploading* yang menandakan file sedang dikirim ke server.
* **Upload Paksa (Satu Folder/File):** Klik kanan pada nama file atau folder di sebelah kiri VS Code, lalu pilih **SFTP: Upload**.
* **Tarik Data dari Server (Download):** Jika ada perubahan langsung di server dan ingin disamakan ke laptop, klik kanan pada file/folder, pilih **SFTP: Download**.
* **Ngoding Jarak Jauh (Beda Jaringan):** Jika sedang tidak satu Wi-Fi dengan Kubuntu, file akan gagal terupload saat di-Save. Tidak masalah, kode tetap aman di laptop. Saat kembali ke jaringan yang sama, cukup klik kanan folder project -> **SFTP: Upload** untuk sinkronisasi massal. (Atau gunakan IP Tailscale di `sftp.json` agar terhubung dari mana saja).