# 🌐 SOP Pemasangan Domain Asli (Cloudflare Tunnel)

Panduan menghubungkan project Docker lokal ke Internet tanpa buka port Router/Firewall.

---

## 🛠️ TAHAP 1: INSTALASI & OTENTIKASI (Hanya 1x Per Server)

Pastikan aplikasi Docker sudah berjalan dengan normal (misal: `localhost:8081` sudah bisa diakses).

### 1. Download & Install Cloudflared

```bash
curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared.deb
```

### 2. Login ke Akun Cloudflare

```bash
cloudflared tunnel login
```

**Catatan:**  
Akan muncul link panjang di terminal. Copy link tersebut, buka di browser PC/HP kamu, lalu login ke akun Cloudflare dan pilih domain yang ingin dipakai.

---

## 🚇 TAHAP 2: PEMBUATAN TUNNEL INDUK (Hanya 1x Per Server)

### 1. Buat Tunnel

Kita buat satu "Pipa" utama untuk server ini (misal kita beri nama `my-first-server`):

```bash
cloudflared tunnel create my-first-server
```

**WAJIB CATAT:**  
Salin ID Tunnel kombinasi angka & huruf yang muncul setelah perintah ini!

### 2. Amankan File Kredensial

Ganti `<MASUKKAN-ID-TUNNEL-DI-SINI>` dengan ID yang kamu dapat:

```bash
sudo mkdir -p /etc/cloudflared
sudo cp ~/.cloudflared/<MASUKKAN-ID-TUNNEL-DI-SINI>.json /etc/cloudflared/
```

---

## 🌍 TAHAP 3: MENYAMBUNGKAN PROJECT KE DOMAIN

**Skenario:**  
Kita akan menyambungkan project `project_adzkiya` (port 8081) ke subdomain `adzkiya.com`.

### 1. Buat Rute DNS di Cloudflare

```bash
cloudflared tunnel route dns my-first-server adzkiya.com
```

### 2. Atur Rute Lalu Lintas (Routing)

Edit file konfigurasi:

```bash
sudo nano /etc/cloudflared/config.yml
```

Isi dengan:

```yaml
tunnel: <MASUKKAN-ID-TUNNEL-DI-SINI>
credentials-file: /etc/cloudflared/<MASUKKAN-ID-TUNNEL-DI-SINI>.json

ingress:
  # --------------------------------------------------
  # PROJECT 1: BDN Karanganyar (Laravel)
  # --------------------------------------------------
  - hostname: adzkiya.com
    service: http://localhost:8081

  # (Project lain bisa ditambahkan di sini)

  # --------------------------------------------------
  # RUTE PENUTUP (WAJIB ADA)
  # --------------------------------------------------
  - service: http_status:404
```

Simpan:
- Tekan `Ctrl + X`
- Ketik `Y`
- Tekan `Enter`

---

## 🚀 TAHAP 4: AKTIFKAN TUNNEL SECARA PERMANEN (Auto-Start)

```bash
sudo cloudflared service install
sudo systemctl start cloudflared
sudo systemctl status cloudflared
```

---

## ✅ SELESAI

Sekarang buka browser dan akses:

```
https://adzkiya.com
```

Website kamu sudah online ke seluruh dunia dengan SSL/HTTPS otomatis dari Cloudflare 🎉
