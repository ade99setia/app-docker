Siap! Mode Pro diaktifkan. Ini adalah dokumentasi "jalur mulus" (tanpa drama *routing conflict*) yang sudah dirapikan. Cocok untuk Anda simpan sebagai panduan instalasi di *server* atau PC *deployment* IDN di masa mendatang.

---

# Dokumentasi: Setup Wi-Fi Hotspot (USB Tenda U2 / AIC8800) via USB Tethering di Kubuntu

**Skenario**: PC (Host) mendapatkan koneksi internet dari Smartphone melalui **USB Tethering**, lalu menyebarkan kembali internet tersebut secara nirkabel sebagai **Wi-Fi Hotspot** menggunakan USB Wi-Fi Adapter Tenda U2 (Chipset AIC8800).

## Tahap 1: Instalasi Driver & Firmware (Chipset AIC8800)
Secara *default*, chipset AIC8800 tidak memiliki driver bawaan di kernel Linux standar dan terdeteksi sebagai perangkat *storage*. Diperlukan kompilasi manual.

### 1. Persiapan Build Tools & Source Code
Pastikan PC sudah memiliki paket untuk melakukan kompilasi kernel:
```bash
sudo apt update
sudo apt install build-essential linux-headers-$(uname -r) git dkms -y
```

Clone repositori driver AIC8800 (menggunakan repositori `lynx610`):
```bash
git clone https://github.com/lynx610/aic8800.git aic8800dc-main
```

### 2. Copy Firmware ke Sistem
Sistem membutuhkan file `.bin` untuk berkomunikasi dengan *hardware*.
```bash
sudo mkdir -p /lib/firmware/aic8800DC
sudo cp ~/aic8800dc-main/fw/aic8800DC/* /lib/firmware/aic8800DC/
```

### 3. Kompilasi dan Instalasi Modul Kernel
Proses kompilasi dilakukan pada dua modul utama: `aic_load_fw` (firmware loader) dan `aic8800_fdrv` (driver jaringan).

**Modul Firmware Loader:**
```bash
cd ~/aic8800dc-main/drivers/aic8800/aic_load_fw
make clean && make -j$(nproc)
sudo make install
```

**Modul Driver Utama:**
```bash
cd ~/aic8800dc-main/drivers/aic8800/aic8800_fdrv
make clean && make -j$(nproc)
sudo make install
```

### 4. Aktivasi Modul
Daftarkan modul ke sistem dan aktifkan secara langsung:
```bash
sudo depmod -a
sudo modprobe aic_load_fw
sudo modprobe aic8800_fdrv
```

Untuk memverifikasi apakah perangkat sudah dikenali sebagai *Network Interface*:
```bash
nmcli device
```
*(Akan muncul interface Wi-Fi baru dengan status `disconnected`, misalnya `wlxc83a35032118`)*.

---

## Tahap 2: Konfigurasi Routing & Isolasi Internet
Untuk mencegah *Multiple Default Gateways* (Kondisi di mana Linux bingung memilih jalur internet karena Wi-Fi mencoba bertindak sebagai *client*), jalur internet harus diisolasi ke USB Tethering.

### 1. Identifikasi Sumber Internet Utama
Colokkan USB dari Smartphone, aktifkan USB Tethering, dan pastikan ia menjadi satu-satunya sumber internet:
```bash
ip route | grep default
```
*(Contoh output yang benar: `default via 10.228.198.7 dev enxfeb1a9f33b0b ...`)*

### 2. Putuskan Koneksi Wi-Fi Klien (Jika Otomatis Terhubung)
Hapus profil jaringan jika Wi-Fi sempat terhubung secara otomatis ke *Access Point* lain (misal: "Galaxy A53 5G"):
```bash
sudo nmcli device disconnect wlxc83a35032118
sudo nmcli connection delete "Nama-SSID-Yang-Nyangkut"
```

---

## Tahap 3: Aktivasi Wi-Fi Hotspot (Shared Mode)
Setelah sumber internet bersih (hanya dari USB Tethering) dan interface Wi-Fi menganggur, ubah Wi-Fi menjadi pemancar.

### 1. Buat Jaringan Hotspot
Jalankan perintah pembuatan *Access Point* menggunakan `nmcli`. (Ganti `ifname` dengan nama interface yang didapat pada Tahap 1).
```bash
sudo nmcli device wifi hotspot ssid "Adzkiya-Hotspot-Kubuntu" password "Kapasitas123!" ifname wlxc83a35032118
```

### 2. Aktifkan Autoconnect (Opsional)
Agar *hotspot* langsung memancar saat PC dinyalakan ulang:
```bash
sudo nmcli connection modify Hotspot connection.autoconnect yes
```

---

## Tahap 4: Monitoring dan Verifikasi

* **Melihat Status Interface:**
  ```bash
  nmcli device
  ```
  *(Interface `wlxc83...` harus berstatus `connected` dengan keterangan profil `Hotspot`).*

* **Melihat Perangkat/Klien yang Numpang Hotspot:**
  Untuk mengecek alamat IP perangkat yang sedang terhubung ke Hotspot kita (membaca *ARP Table*):
  ```bash
  ip neigh show dev wlxc83a35032118
  ```

* **Melihat Password Wi-Fi (Jika Lupa):**
  ```bash
  nmcli dev wifi show-password
  ```


------------------------------------------------------------------------------------

### 1. Masalah "Priority" (Metric)
Saat Anda mematikan USB Tethering, Linux kehilangan rute internet utama. Begitu Anda nyalakan lagi, Linux seringkali **bingung** karena ada dua interface lain yang statusnya "Connected" (yaitu **LAN** dan **Hotspot**). 

Karena LAN dan Hotspot disetting sebagai "Shared", Linux kadang mencoba mencari internet lewat kabel LAN ke laptop atau lewat WiFi Tenda (padahal keduanya kan menunggu kiriman internet dari PC).

### 2. DNS Stuck
Kadang layanan `dnsmasq` (yang mengurus pembagian IP dan internet ke laptop/HP lain) masih "megang" konfigurasi yang lama. Saat USB dicolok lagi, dia tidak otomatis *refresh* jalurnya.

---

### Solusi Permanen: Set Prioritas (Metric)
Kita harus kasih tahu PC kalau **USB Tethering adalah bosnya**. Jalurnya harus diprioritaskan lebih tinggi (angka metric lebih kecil) daripada LAN atau Hotspot.

Jalankan perintah ini satu per satu:

1.  **Set USB HP jadi prioritas utama:**
    ```bash
    sudo nmcli connection modify "Wired connection 3" ipv4.route-metric 10
    ```

2.  **Set LAN jadi prioritas rendah:**
    ```bash
    sudo nmcli connection modify "Wired connection 1" ipv4.route-metric 100
    ```

3.  **Set Hotspot jadi prioritas paling rendah:**
    ```bash
    sudo nmcli connection modify "Hotspot" ipv4.route-metric 200
    ```

4.  **Terapkan perubahan:**
    ```bash
    sudo nmcli connection up "Wired connection 3"
    ```



### Mengapa ini membantu?
Dengan settingan di atas, meskipun USB HP dicabut-pasang, Linux akan selalu tahu: *"Kalau ada koneksi di Wired connection 3, pakai itu dulu buat internet. Jangan coba-coba lewat LAN atau Hotspot karena metric-nya lebih gede (prioritas rendah)."*

**Saran tambahan:**
Kalau dicolok-pasang terus internet tetap belum masuk, pastikan di HP Samsung Anda, mode **"USB Tethering"** sudah benar-benar menyala kembali. Kadang setelah putus, HP balik ke mode "Hanya mengisi daya".