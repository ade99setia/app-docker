# 🗺️ Infrastruktur Docker Server

## 📌 Alokasi Port

| Port | Service | Project             | Keterangan       |
| ---- | ------- | ------------------- | ---------------- |
| 8081 | Web     | BDN Karanganyar     | Laravel + Nginx  |
| 8082 | Web     | Undangan Pernikahan | CI4 + Nginx      |
| 8083 | Web     | Web Portofolio      | Static Container |
| 3306 | MySQL   | BDN Karanganyar     | Default DB       |
| 3307 | MySQL   | Undangan Pernikahan | Remote DB        |

| Next Web | Next DB |
| -------- | ------- |
| 8084     | 3308    |

---

## 📦 Detail Infrastruktur

| Project             | Stack                                      | Container                                                                                   | Image                                                              | Web  | DB   | Network                         | Volume                                                             | Tunnel |
| ------------------- | ------------------------------------------ | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ | ---- | ---- | ------------------------------- | ------------------------------------------------------------------ | ------ |
| BDN Karanganyar     | Laravel + PHP-FPM + Nginx + MySQL          | bdn_karanganyar_app<br>bdn_karanganyar_web<br>bdn_karanganyar_db                            | ghcr.io/...<br>nginx:alpine<br>mysql:8.0                           | 8081 | 3306 | app_network_bdn_karanganyar     | public_app<br>storage_app<br>db_data                               | ❌      |
| Undangan Pernikahan | CI4 + PHP-FPM + Nginx + MySQL + Cloudflare | undangan_pernikahan_app<br>undangan_pernikahan_web<br>undangan_pernikahan_db<br>cloudflared | ghcr.io/...<br>nginx:alpine<br>mysql:8.0<br>cloudflare/cloudflared | 8082 | 3307 | app_network_undangan_pernikahan | uploads_data<br>private_data<br>logs_data<br>db_data<br>public_app | ✅      |
| Web Portofolio      | Static + Nginx + Cloudflare Tunnel         | web_portofolio_container<br>cloudflared_portofolio                                          | build local<br>cloudflare/cloudflared                              | 8083 | -    | portfolio_network               | -                                                                  | ✅      |

---

## 🕸️ Network Isolation

| Project             | Network                         | Isolated |
| ------------------- | ------------------------------- | -------- |
| BDN Karanganyar     | app_network_bdn_karanganyar     | ✅        |
| Undangan Pernikahan | app_network_undangan_pernikahan | ✅        |
| Web Portofolio      | portfolio_network               | ✅        |

---

## 📊 Ringkasan

| Project             | Stack   | Web  | DB   | Tunnel |
| ------------------- | ------- | ---- | ---- | ------ |
| BDN Karanganyar     | Laravel | 8081 | 3306 | ❌ bdn.ade-setiawan.my.id |
| Undangan Pernikahan | CI4     | 8082 | 3307 | ✅ invite.ade-setiawan.my.id |
| Web Portofolio      | Static  | 8083 | -    | ✅ ade-setiawan.my.id|

---

## 🛠️ Standar Project Baru

| Komponen         | Nilai            |
| ---------------- | ---------------- |
| Web Port         | 8084             |
| DB Port          | 3308             |
| Prefix Container | project4_*       |
| Network          | project4_network |
| Volume           | project4_*       |
