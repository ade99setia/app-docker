
---

# 📖 Dokumentasi Konfigurasi Jaringan & Troubleshooting Server (Ubuntu)

**Konteks Masalah Sebelumnya:** Server kehilangan koneksi internet dan akses SSH via Tailscale terputus karena kesalahan penentuan IP Static dan *Gateway* pada koneksi WiFi (Hotspot HP), serta bentrok prioritas (*Metric*) dengan koneksi kabel LAN.

**Temuan Baru:** Dari hasil `ip route` terakhir, terungkap bahwa Hotspot "Galaxy A53 5G" Anda menggunakan jaringan dengan rentang `10.63.161.x`, bukan `10.159.x.x`. 
* **Gateway HP Anda:** `10.63.161.15`
* **IP DHCP yang didapat:** `10.63.161.115`

---

## 🛠️ Tahap 1: Membersihkan Konfigurasi Lama (Reset)
Jika jaringan mulai kacau, langkah pertama adalah menghapus konfigurasi yang error agar kembali bersih.

```bash
# 1. Hapus profil koneksi WiFi yang error di NetworkManager
sudo nmcli connection delete "Galaxy A53 5G"

# 2. Hapus file konfigurasi Netplan yang dibuat manual (jika ada)
sudo rm /etc/netplan/90-NM-dbee3704-95d2-4f8a-a7bb-2fcec6a35653.yaml

# 3. Terapkan konfigurasi Netplan yang bersih
sudo netplan apply
```

---

## 📡 Tahap 2: Mendapatkan Konfigurasi Asli (DHCP Discovery)
Jangan langsung menebak IP Static saat menggunakan Hotspot HP, karena HP sering merotasi *subnet*. Biarkan sistem meminta IP otomatis (DHCP) terlebih dahulu untuk "mengintip" jaringannya.

```bash
# 1. Hubungkan ke WiFi secara otomatis (DHCP)
sudo nmcli device wifi connect "Galaxy A53 5G" password "mulaidari2020"

# 2. Cek Gateway dan IP yang diberikan oleh HP
ip route
```
*(Catat IP dari `default via ... dev wlxc...`. Pada kasus ini adalah `10.63.161.15`)*

---

## 📌 Tahap 3: Mengatur IP Static & Prioritas Koneksi (Metric)
Setelah mengetahui struktur jaringan yang benar (`10.63.161.x`), kita ubah koneksi tersebut menjadi Static IP secara aman menggunakan `nmcli`. 

Kita juga mengatur **Metric menjadi 50** agar WiFi diprioritaskan untuk internet dibandingkan kabel LAN (yang memiliki metric 100).

```bash
# GUNAKAN INI UNTUK MENJALANKAN SEKALIGUS SEMUANYA 1 - 5
sudo nmcli connection modify "Galaxy A53 5G" ipv4.method manual ipv4.addresses "10.63.161.115/24" ipv4.gateway "10.63.161.15" ipv4.dns "8.8.8.8,1.1.1.1" ipv4.route-metric 50

# 1. Ubah metode menjadi manual (Static)
sudo nmcli connection modify "Galaxy A53 5G" ipv4.method manual

# 2. Pasang IP Static yang aman (berada di satu keluarga dengan gateway)
sudo nmcli connection modify "Galaxy A53 5G" ipv4.addresses "10.63.161.115/24"

# 3. Pasang Gateway (sesuai temuan dari DHCP)
sudo nmcli connection modify "Galaxy A53 5G" ipv4.gateway "10.63.161.15"

# 4. Pasang DNS Google & Cloudflare agar bisa browsing
sudo nmcli connection modify "Galaxy A53 5G" ipv4.dns "8.8.8.8,1.1.1.1"

# 5. Pasang prioritas Metric (Angka lebih kecil = Prioritas utama)
sudo nmcli connection modify "Galaxy A53 5G" ipv4.route-metric 50

# 6. Restart koneksi untuk menerapkan perubahan
sudo nmcli connection up "Galaxy A53 5G"
```

---

## 🚨 Tahap 4: Panduan Darurat Jika Terkunci (Bypass Access)
Jika terjadi salah konfigurasi lagi yang mengakibatkan SSH (Tailscale/LAN) putus total, gunakan **Jalur Penambatan USB (USB Tethering)**.

1.  Colokkan HP ke PC Server menggunakan kabel USB.
2.  Di HP, aktifkan **Penambatan USB / USB Tethering**.
3.  Buka aplikasi Terminal di HP Android (misal: Termux).
4.  Cek IP PC Server yang baru saja diberikan oleh HP melalui kabel USB dengan perintah:
    ```bash
    ip neigh
    # atau
    arp -a
    ```
5.  Masuk ke server menggunakan IP yang tertera `REACHABLE` tersebut:
    ```bash
    ssh ade-setia@<IP_DARI_TERMUX>
    ```
6.  Setelah masuk, matikan WiFi yang *crash* agar jalur normal terbuka kembali:
    ```bash
    sudo nmcli connection down "Galaxy A53 5G"
    ```

---

## 🔍 Tahap 5: "Cheat Sheet" Diagnosa Jaringan
Jika koneksi internet mati, ikuti 3 langkah investigasi ini secara berurutan:

### 1. Cek Interface Jaringan (Apakah Mendapat IP?)
**Perintah:** `ip a`
* Pastikan interface `wlx...` (WiFi) atau `enx...` (Kabel) memiliki status `UP`.
* Pastikan terdapat baris `inet` (contoh: `inet 10.63.161.115`). Jika tidak ada, berarti koneksi fisik/password WiFi bermasalah.

### 2. Cek Jalur Lalu Lintas (Siapa Prioritasnya?)
**Perintah:** `ip route`
* Perhatikan baris yang dimulai dengan kata `default`.
* Jika ada lebih dari satu `default`, **cek angka `metric`**. Angka terkecil adalah jalur yang dipakai sistem. Jika jalur tersebut mati, maka seluruh koneksi internet server ikut mati.

### 3. Tes Ping Bertahap (Lokalisasi Putus Jalur)
Lakukan Ping dari yang terdekat ke yang terjauh:
1.  **Ping Gateway (Router/HP):** `ping 10.63.161.15`
    * *Jika RTO/Gagal:* Masalah ada di konfigurasi WiFi server atau Router mati.
2.  **Ping Server Luar:** `ping 8.8.8.8`
    * *Jika RTO/Gagal (tapi Gateway sukses):* Router/HP tidak punya kuota internet atau diblokir provider.
3.  **Ping Nama Domain:** `ping google.com`
    * *Jika RTO/Gagal (tapi 8.8.8.8 sukses):* Murni masalah konfigurasi DNS di server. Tambahkan `8.8.8.8` pada pengaturan koneksi.

---