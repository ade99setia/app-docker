
---

# 🗺️ Infrastruktur Docker Server

## 📌 Alokasi Port

| Port | Service  | Project             | Keterangan            |
| ---- | -------- | ------------------- | --------------------- |
| 8080 | Web      | Evolution API       | WhatsApp Gateway API  |
| 8081 | Web      | BDN Karanganyar     | Laravel + Nginx       |
| 8082 | Web      | Undangan Pernikahan | CI4 + Nginx           |
| 8083 | Web      | Web Portofolio      | Static Container      |
| 8084 | Web      | IDN Solo            | Laravel + Nginx       |
| 8085 | Web      | Fileserver          | Filebrowser           |
| 8086 | Web      | Registry UI         | Docker Registry UI    |
| 8087 | Web      | DB Manager          | CloudBeaver           |
| 8088 | Web      | Face Scan Webhook   | Python Realtime Relay |
| 8089 | Web      | Face Scan Camera    | Python VIID Forwarder |
| 9000 | Web      | Portainer           | Docker Dashboard      |
| 5000 | System   | Private Registry    | Docker Image Registry |
| 3389 | System   | XRDP                | Remote Desktop        |
| 3306 | MySQL    | BDN Karanganyar     | Default DB            |
| 3307 | MySQL    | Undangan Pernikahan | Remote DB             |
| 3308 | MySQL    | IDN Solo            | Dedicated MySQL       |
| 5432 | Postgres | Evolution API       | PostgreSQL Database   |
| 6379 | Redis    | Evolution API       | Cache & Queue         |

---

## 📦 Detail Infrastruktur

| Project             | Stack                                              | Container                                                                                   | Image                                                                  | Web  | DB   | Network                                    | Volume                                                             | Tunnel |
| ------------------- | -------------------------------------------------- | ------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- | ---- | ---- | ------------------------------------------ | ------------------------------------------------------------------ | ------ |
| **Evolution API**   | Node.js + WhatsApp API + Redis + PostgreSQL        | evolution_api<br>evolution_redis<br>evolution_db                                            | evoapicloud/evolution-api:latest<br>redis:latest<br>postgres:15-alpine | 8080 | 5432 | evolution-net<br>shared_web_network        | evolution_instances<br>evolution_redis<br>postgres_data            | ❌      |
| BDN Karanganyar     | Laravel + PHP-FPM + Nginx + MySQL                  | bdn_karanganyar_app<br>bdn_karanganyar_web<br>bdn_karanganyar_db                            | ghcr.io/...<br>nginx:alpine<br>mysql:8.0                               | 8081 | 3306 | app_network_bdn_karanganyar<br>shared_web_network                | public_app<br>storage_app<br>db_data                               | ❌      |
| Undangan Pernikahan | CI4 + PHP-FPM + Nginx + MySQL + Cloudflare         | undangan_pernikahan_app<br>undangan_pernikahan_web<br>undangan_pernikahan_db<br>cloudflared | ghcr.io/...<br>nginx:alpine<br>mysql:8.0<br>cloudflare/cloudflared     | 8082 | 3307 | app_network_undangan_pernikahan<br>shared_web_network            | uploads_data<br>private_data<br>logs_data<br>db_data<br>public_app | ✅      |
| Web Portofolio      | Static + Nginx + Cloudflare Tunnel                 | web_portofolio_container<br>cloudflared_portofolio                                          | build local<br>cloudflare/cloudflared                                  | 8083 | -    | portfolio_network<br>shared_web_network                          | -                                                                  | ✅      |
| IDN Solo            | Laravel + PHP-FPM + Nginx + MySQL + Shared Network | idn_solo_app<br>idn_solo_web<br>idn_solo_db                                                 | ghcr.io/...<br>nginx:alpine<br>mysql:8.0                               | 8084 | 3308 | app_network_idn_solo<br>shared_web_network | public_app<br>storage_app<br>db_data                               | ❌      |
| Face Scan Webhook   | Python HTTP Receiver + Relay                        | face-scan-webhook-realtime<br>face-scan-webhook-polling                                     | build local<br>python:3.11-slim                                        | 8088 | -    | default                                    | last_checkin_time.txt                                              | ❌      |
| Face Scan Camera    | Python VIID Forwarder                               | face-scan-camera-forwarder                                                                  | build local<br>python:3.11-slim                                        | 8089 | -    | default                                    | -                                                                  | ❌      |
| Fileserver          | Filebrowser + Docker                               | filebrowser                                                                                 | filebrowser/filebrowser:latest                                         | 8085 | -    | default                                    | filebrowser.db                                                     | ❌      |
| DB Manager          | CloudBeaver (Database UI)                          | cloudbeaver_db_manager                                                                      | dbeaver/cloudbeaver:latest                                             | 8087 | -    | shared_web_network                         | cloudbeaver_data                                                   | ❌      |
| Portainer           | Docker Management UI                               | portainer                                                                                   | portainer/portainer-ce:latest                                          | 9000 | -    | default                                    | portainer_data                                                     | ❌      |
| Private Registry    | Docker Registry + Registry UI                      | private_registry<br>registry_ui                                                             | registry:2<br>joxit/docker-registry-ui:latest                          | 8086 | -    | default                                    | registry_data                                                      | ❌      |
| XRDP                | Remote Desktop XFCE                                | system service                                                                              | system                                                                 | 3389 | -    | system                                     | system                                                             | ❌      |

---

# Shared Network for Cloudflare Tunnel

```bash
# Hanya dijalankan sekali saja
docker network create shared_web_network

# Auto Service to User
sudo loginctl enable-linger $USER
loginctl show-user $USER | grep Linger
```

---

## 🕸️ Network Isolation

| Project             | Network                         | Shared               | Isolated |
| ------------------- | ------------------------------- | -------------------- | -------- |
| Evolution API       | evolution-net                   | ✅ shared_web_network | ✅        |
| BDN Karanganyar     | app_network_bdn_karanganyar     | ✅ shared_web_network | ✅        |
| Undangan Pernikahan | app_network_undangan_pernikahan | ✅ shared_web_network | ✅        |
| Web Portofolio      | portfolio_network               | ✅ shared_web_network | ✅        |
| IDN Solo            | app_network_idn_solo            | ✅ shared_web_network | ✅        |
| DB Manager          | shared_web_network              | ✅ shared_web_network | ❌        |
| Fileserver          | default                         | ❌                    | ❌        |
| Portainer           | default                         | ❌                    | ❌        |
| Private Registry    | default                         | ❌                    | ❌        |

---

## 📊 Ringkasan

| Project             | Stack           | Web  | DB   | Tunnel |
| ------------------- | --------------- | ---- | ---- | ------ |
| Evolution API       | WhatsApp API    | 8080 | 5432 | ❌      |
| BDN Karanganyar     | Laravel         | 8081 | 3306 | ❌      |
| Undangan Pernikahan | CI4             | 8082 | 3307 | ✅      |
| Web Portofolio      | Static          | 8083 | -    | ✅      |
| IDN Solo            | Laravel         | 8084 | 3308 | ✅      |
| Face Scan Webhook   | Python Relay    | 8088 | -    | ❌      |
| Face Scan Camera    | Python Forwarder| 8089 | -    | ❌      |
| Fileserver          | Filebrowser     | 8085 | -    | ❌      |
| DB Manager          | CloudBeaver     | 8087 | -    | ❌      |
| Private Registry    | Docker Registry | 8086 | -    | ❌      |
| Portainer           | Docker UI       | 9000 | -    | ❌      |
| XRDP                | XFCE            | 3389 | -    | ❌      |

---

## ⚠️ Port Status

| Port | Status | Digunakan Oleh       |
| ---- | ------ | -------------------- |
| 8080 | Used   | Evolution API        |
| 8081 | Used   | BDN Karanganyar      |
| 8082 | Used   | Undangan Pernikahan  |
| 8083 | Used   | Web Portofolio       |
| 8084 | Used   | IDN Solo             |
| 8085 | Used   | Fileserver           |
| 8086 | Used   | Registry UI          |
| 8087 | Used   | CloudBeaver          |
| 8088 | Used   | Face Scan Webhook    |
| 8089 | Used   | Face Scan Camera     |
| 9000 | Used   | Portainer            |
| 5000 | Used   | Private Registry     |
| 3389 | Used   | XRDP                 |
| 3306 | Used   | BDN Karanganyar      |
| 3307 | Used   | Undangan Pernikahan  |
| 3308 | Used   | IDN Solo             |
| 5432 | Used   | Evolution PostgreSQL |
| 6379 | Used   | Redis Evolution      |

---

## 🛠️ Standar Project Baru (Update)

| Komponen         | Nilai            |
| ---------------- | ---------------- |
| Web Port         | 8090             |
| DB Port          | 3309             |
| Prefix Container | project5_*       |
| Network          | project5_network |
| Volume           | project5_*       |

---

## 🧠 Catatan

* Port 8080 digunakan untuk **Evolution API (WhatsApp Gateway)**
* Port 8088 digunakan untuk **Face Scan Webhook Realtime** (IoT polling/realtime dari device)
* Port 8089 digunakan untuk **Face Scan Camera Forwarder** (VIID webhook receiver → forward PersonID ke idnsolo.com)
* Evolution API menggunakan **PostgreSQL (5432)** dan **Redis (6379)** untuk performa optimal
* Network `evolution-net` untuk isolasi internal service
* Tetap terhubung ke `shared_web_network` untuk integrasi dengan service lain
* Volume:

  * `evolution_instances` → session WhatsApp
  * `evolution_redis` → cache Redis
  * `postgres_data` → database PostgreSQL
* CloudBeaver bisa digunakan untuk mengakses PostgreSQL Evolution
* Semua service tetap terisolasi dengan network masing-masing
* Tidak ada konflik port
* Private Registry tetap digunakan untuk image lokal (`localhost:5000`)

---