# 🗺️ Infrastruktur Docker Server

## 📌 Alokasi Port

| Port | Service | Project             | Keterangan       |
| ---- | ------- | ------------------- | ---------------- |
| 8081 | Web     | BDN Karanganyar     | Laravel + Nginx  |
| 8082 | Web     | Undangan Pernikahan | CI4 + Nginx      |
| 8083 | Web     | Web Portofolio      | Static Container |
| 8084 | Web     | IDN Solo            | Laravel + Nginx  |
| 3306 | MySQL   | BDN Karanganyar     | Default DB       |
| 3307 | MySQL   | Undangan Pernikahan | Remote DB        |
| 3308 | MySQL   | IDN Solo            | Dedicated MySQL  |

---

## 📦 Detail Infrastruktur

| Project             | Stack                                              | Container                                                                                   | Image                                                              | Web  | DB   | Network                                    | Volume                                                             | Tunnel |
| ------------------- | -------------------------------------------------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ | ---- | ---- | ------------------------------------------ | ------------------------------------------------------------------ | ------ |
| BDN Karanganyar     | Laravel + PHP-FPM + Nginx + MySQL                  | bdn_karanganyar_app<br>bdn_karanganyar_web<br>bdn_karanganyar_db                            | ghcr.io/...<br>nginx:alpine<br>mysql:8.0                           | 8081 | 3306 | app_network_bdn_karanganyar                | public_app<br>storage_app<br>db_data                               | ❌      |
| Undangan Pernikahan | CI4 + PHP-FPM + Nginx + MySQL + Cloudflare         | undangan_pernikahan_app<br>undangan_pernikahan_web<br>undangan_pernikahan_db<br>cloudflared | ghcr.io/...<br>nginx:alpine<br>mysql:8.0<br>cloudflare/cloudflared | 8082 | 3307 | app_network_undangan_pernikahan            | uploads_data<br>private_data<br>logs_data<br>db_data<br>public_app | ✅      |
| Web Portofolio      | Static + Nginx + Cloudflare Tunnel                 | web_portofolio_container<br>cloudflared_portofolio                                          | build local<br>cloudflare/cloudflared                              | 8083 | -    | portfolio_network                          | -                                                                  | ✅      |
| IDN Solo            | Laravel + PHP-FPM + Nginx + MySQL + Shared Network | idn_solo_app<br>idn_solo_web<br>idn_solo_db                                                 | ghcr.io/...<br>nginx:alpine<br>mysql:8.0                           | 8084 | 3308 | app_network_idn_solo<br>shared_web_network | public_app<br>storage_app<br>db_data                               | ❌      |

---

## 🕸️ Network Isolation

| Project             | Network                         | Shared               | Isolated |
| ------------------- | ------------------------------- | -------------------- | -------- |
| BDN Karanganyar     | app_network_bdn_karanganyar     | ✅ shared_web_network | ✅        |
| Undangan Pernikahan | app_network_undangan_pernikahan | ✅ shared_web_network | ✅        |
| Web Portofolio      | portfolio_network               | ✅ shared_web_network | ✅        |
| IDN Solo            | app_network_idn_solo            | ✅ shared_web_network | ✅        |

---

## 📊 Ringkasan

| Project             | Stack   | Web  | DB   | Tunnel                      |
| ------------------- | ------- | ---- | ---- | --------------------------- |
| BDN Karanganyar     | Laravel | 8081 | 3306 | ❌ bdn.ade-setiawan.my.id    |
| Undangan Pernikahan | CI4     | 8082 | 3307 | ✅ invite.ade-setiawan.my.id |
| Web Portofolio      | Static  | 8083 | -    | ✅ ade-setiawan.my.id        |
| IDN Solo            | Laravel | 8084 | 3308 | ✅ idn.ade-setiawan.my.id    |

---

## ⚠️ Port Status

| Port | Status | Digunakan Oleh      |
| ---- | ------ | ------------------- |
| 8081 | Used   | BDN Karanganyar     |
| 8082 | Used   | Undangan Pernikahan |
| 8083 | Used   | Web Portofolio      |
| 8084 | Used   | IDN Solo            |
| 3306 | Used   | BDN Karanganyar     |
| 3307 | Used   | Undangan Pernikahan |
| 3308 | Used   | IDN Solo            |

---

## 🛠️ Standar Project Baru (Update)

| Komponen         | Nilai            |
| ---------------- | ---------------- |
| Web Port         | 8085             |
| DB Port          | 3309             |
| Prefix Container | project5_*       |
| Network          | project5_network |
| Volume           | project5_*       |

---

## 🧠 Catatan

* Port 8084 sudah dipakai `idn_solo_web`
* Port 3308 sudah dipakai `idn_solo_db`
* IDN Solo menggunakan `shared_web_network`
* Semua project tetap isolated network masing-masing
* Tidak ada konflik port antar container
