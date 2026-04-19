Tentu, ini adalah dokumentasi ringkas untuk prosedur **Internet Connection Sharing (ICS)** pada Kubuntu melalui terminal SSH yang baru saja kita lakukan. Dokumentasi ini bisa Anda simpan untuk keperluan *sysadmin* di masa mendatang.

---

## Dokumentasi: Berbagi Koneksi Internet (Sharing) via LAN di Kubuntu
**Skenario**: PC (Host) memiliki internet dari interface lain (Wi-Fi/USB) dan ingin membagikannya ke Laptop (Client) melalui kabel LAN menggunakan SSH.

### 1. Identifikasi Interface LAN
Langkah pertama adalah mencari nama perangkat keras (interface) kabel LAN yang terhubung ke perangkat client.
```bash
nmcli device
```
* **Hasil**: Ditemukan interface `enp0s31f6` dengan status `connecting` atau `unavailable`.
* **Profil Koneksi**: Biasanya bernama "Wired connection 1".

### 2. Konfigurasi Metode Sharing
Mengubah protokol IPv4 dari mode DHCP client (mencari IP) menjadi mode **Shared** (bertindak sebagai server/gateway).
```bash
sudo nmcli connection modify "Wired connection 1" ipv4.method shared
```
> **Catatan**: Perintah ini secara otomatis mengaktifkan `IP Forwarding` di kernel dan mengatur aturan `NAT (MASQUERADE)` pada iptables/nftables secara otomatis oleh NetworkManager.

### 3. Aktivasi Koneksi
Restart atau aktifkan profil agar perubahan diterapkan.
```bash
sudo nmcli connection up "Wired connection 1"
```

### 4. Verifikasi Hasil di Sisi PC (Host)
Pastikan interface telah memiliki alamat IP statis default dari NetworkManager (biasanya di segmen `10.42.x.x`).
```bash
ip addr show enp0s31f6
```
**Output Sukses**:
`inet 10.42.0.1/24 brd 10.42.0.255 scope global ...`

### 5. Konfigurasi di Sisi Laptop (Client)
* **Pengaturan**: Setel LAN/Ethernet ke mode **DHCP (Automatic)**.
* **Hasil**: Laptop akan menerima IP otomatis (misal: `10.42.0.50`) dengan Gateway `10.42.0.1`.

---

### Troubleshooting Tambahan
Jika Laptop terhubung namun tidak bisa akses internet, cek aturan Firewall (UFW) di PC Kubuntu:

* **Izinkan Traffic Routing**:
    ```bash
    sudo ufw route allow in enp0s31f6
    sudo ufw route allow out enp0s31f6
    ```
* **Cek Perangkat yang Terhubung (ARP)**:
    Untuk melihat apakah Laptop sudah terdeteksi oleh PC:
    ```bash
    arp -a | grep enp0s31f6
    ```

---
**Status**: Berhasil diaplikasikan pada interface `enp0s31f6`. Laptop kini memiliki akses internet yang sama dengan PC.