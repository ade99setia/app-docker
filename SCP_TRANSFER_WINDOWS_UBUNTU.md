# 📄 Dokumentasi SCP — Transfer File Windows ↔ Ubuntu Server

Digunakan untuk transfer file antara **Laptop Windows** dan **Server Ubuntu** menggunakan `scp` (Secure Copy).

---

# 🧠 Aturan Dasar SCP

| Aturan               | Keterangan                         |
| -------------------- | ---------------------------------- |
| Jalankan dari        | Terminal laptop (PowerShell / CMD) |
| Jangan jalankan dari | Terminal SSH server                |
| Sintaks dasar        | `scp sumber tujuan`                |
| Copy folder          | gunakan `-r`                       |
| Separator server     | gunakan `:` setelah IP             |

---

# 🔼 Upload (Windows → Server)

## Upload 1 File

```bash id="8s3z5u"
scp "D:\3-ProjectWebsite\project-bdn-karanganyar\.env" idnsolo@100.110.141.44:~/server-hosting/bdn_karanganyar/
```

| Bagian | Keterangan    |
| ------ | ------------- |
| Sumber | File Windows  |
| Tujuan | Folder server |
| Hasil  | File terkirim |

---

## Upload 1 Folder

Gunakan `-r`

```bash id="f0pwlv"
scp -r "D:\3-ProjectWebsite\app-docker\whatsapp-gateway" idnsolo@100.110.141.44:~/server-hosting/
```

| Behavior         | Hasil           |
| ---------------- | --------------- |
| Folder tidak ada | otomatis dibuat |
| Isi folder       | ikut tersalin   |
| Recursive        | aktif           |

---

# 🔽 Download (Server → Windows)

## Download 1 File

```bash id="a6oz3j"
scp idnsolo@100.110.141.44:~/server-hosting/backup_bdn_karanganyar.sql "D:\Backup_Database\"
```

| Bagian | Keterangan     |
| ------ | -------------- |
| Sumber | Server Ubuntu  |
| Tujuan | Laptop Windows |
| Hasil  | File ditarik   |

---

## Download 1 Folder

```bash id="g9u7i3"
scp -r idnsolo@100.110.141.44:~/server-hosting/bdn_karanganyar/storage "D:\3-ProjectWebsite\Backup_Storage\"
```

| Behavior        | Hasil         |
| --------------- | ------------- |
| Recursive       | aktif         |
| Semua file      | ikut          |
| Struktur folder | dipertahankan |

---

# 🧭 Panduan Path

## Windows Path

| Format       | Contoh                 |
| ------------ | ---------------------- |
| Dengan spasi | `"D:\Proyek Baru\app"` |
| Folder aktif | `.`                    |
| Drive        | `D:\`                  |

Contoh download ke folder aktif:

```bash id="ifz8bd"
scp idnsolo@100.110.141.44:~/file.txt .
```

---

## Ubuntu Path

| Path             | Keterangan        |
| ---------------- | ----------------- |
| `~/`             | Home user         |
| `/home/user/`    | Absolute home     |
| `/var/www/html/` | Folder web server |
| `.`              | folder aktif      |

---

# 📊 Contoh Pola Umum

## Upload

```id="jj31gq"
scp sumber_lokal user@ip_server:tujuan_server
```

## Download

```id="g7jdfz"
scp user@ip_server:sumber_server tujuan_lokal
```

---

# 🧪 Contoh Nyata

| Kebutuhan        | Command                         |
| ---------------- | ------------------------------- |
| Upload .env      | `scp ".env" user@ip:~/project/` |
| Upload folder    | `scp -r app user@ip:~/`         |
| Download backup  | `scp user@ip:~/backup.sql .`    |
| Download storage | `scp -r user@ip:~/storage .`    |

---

# ⚠️ Kesalahan Umum

| Error             | Penyebab               |
| ----------------- | ---------------------- |
| Permission denied | user salah             |
| No such file      | path salah             |
| Command not found | tidak di laptop        |
| SCP stuck         | koneksi SSH bermasalah |
| Missing colon     | lupa `:` setelah IP    |

---

# 🟢 Tips Praktis

* Gunakan `~/` untuk area aman
* Gunakan tanda kutip jika ada spasi
* Gunakan `-r` untuk folder
* Gunakan `.` untuk folder aktif
* Gunakan IP tailscale jika private

---

# 🚀 Ringkasan

| Operasi         | Sintaks                          |
| --------------- | -------------------------------- |
| Upload file     | `scp file user@server:path`      |
| Upload folder   | `scp -r folder user@server:path` |
| Download file   | `scp user@server:file path`      |
| Download folder | `scp -r user@server:folder path` |

---

# ✅ Status

* Transfer aman (SSH encrypted)
* Bisa Windows ↔ Linux
* Mendukung folder recursive
* Tidak perlu FTP
---
---


# 📄 Navigasi & Eksplorasi Server Ubuntu (SSH)

Semua perintah dijalankan **di dalam terminal SSH server**

```
idnsolo@idn-solo:~$
```

---

# 👁️ Melihat Isi Folder (ls)

| Command    | Fungsi                | Kapan Dipakai    |
| ---------- | --------------------- | ---------------- |
| `ls`       | list biasa            | cek cepat        |
| `ls -l`    | detail file           | lihat permission |
| `ls -a`    | tampilkan hidden file | cek `.env`       |
| `ls -la` ⭐ | detail + hidden       | paling sering    |
| `ls -lh`   | ukuran readable       | cek file besar   |

Contoh:

```bash
ls -la
```

---

# 👣 Navigasi Folder (cd)

| Command      | Fungsi                    |
| ------------ | ------------------------- |
| `pwd`        | lihat lokasi sekarang     |
| `cd folder/` | masuk folder              |
| `cd ..`      | naik 1 tingkat            |
| `cd ../../`  | naik 2 tingkat            |
| `cd ~`       | kembali ke home           |
| `cd /`       | ke root sistem            |
| `cd -`       | kembali folder sebelumnya |

Contoh:

```bash
cd server-hosting/
cd bdn_karanganyar/
```

---

# 🔍 Mencari File

Cari file dari folder saat ini

```bash
find . -name "database.sqlite"
```

| Bagian  | Arti             |
| ------- | ---------------- |
| `find`  | command cari     |
| `.`     | mulai dari sini  |
| `-name` | berdasarkan nama |

---

# 💽 Cek Penyimpanan Server

```bash
df -h
```

| Kolom | Arti         |
| ----- | ------------ |
| Size  | total disk   |
| Used  | terpakai     |
| Avail | sisa         |
| Use%  | persen penuh |

Fokus pada baris:

```
/dev/root
atau
/
```

---

# 📦 Cek Ukuran Folder

```bash
du -sh storage/
```

| Flag | Arti           |
| ---- | -------------- |
| `-s` | total saja     |
| `-h` | human readable |

Contoh lain:

```bash
du -sh *
```

(lihat ukuran semua folder)

---

# ⚡ Command Cepat (Cheatsheet)

| Kebutuhan       | Command               |
| --------------- | --------------------- |
| Lokasi sekarang | `pwd`                 |
| List detail     | `ls -la`              |
| Masuk folder    | `cd folder`           |
| Mundur          | `cd ..`               |
| Home            | `cd ~`                |
| Cari file       | `find . -name "file"` |
| Sisa disk       | `df -h`               |
| Ukuran folder   | `du -sh folder/`      |

---

# 🧠 Workflow Umum Administrator

```bash
pwd
ls -la
cd server-hosting
ls -la
du -sh *
df -h
```

---

# ⭐ Paling Sering Dipakai

| Command  | Fungsi           |
| -------- | ---------------- |
| `ls -la` | lihat isi folder |
| `cd`     | pindah folder    |
| `pwd`    | cek lokasi       |
| `du -sh` | cek ukuran       |
| `df -h`  | cek disk         |
| `find`   | cari file        |

---

# ✅ Tips

* gunakan `ls -la` hampir selalu
* gunakan `cd ~` jika tersesat
* gunakan `du -sh *` untuk cari folder besar
* gunakan `df -h` sebelum disk penuh
* gunakan `find` jika file hilang
