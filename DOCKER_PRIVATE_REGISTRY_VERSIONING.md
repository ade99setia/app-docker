# 🐳 Docker Private Registry + Semantic Versioning Guide

Dokumentasi ini menjelaskan:

* private registry sendiri
* semantic versioning (SemVer)
* push image dari laptop ke server
* multi versi deployment
* 1 domain = 1 versi
* rollback cepat
* multi domain deployment

---

# 🧱 Arsitektur

```
Laptop Build → Push → Private Registry → Server Pull → Docker Compose
```

Contoh:

```
v1.0.0 → production
v1.1.0 → beta
v1.1.1 → dev
```

---

# 🔢 Semantic Versioning (SemVer)

Format:

```
vMAJOR.MINOR.PATCH
```

| Bagian | Contoh | Kapan Naik      |
| ------ | ------ | --------------- |
| MAJOR  | v2.0.0 | breaking change |
| MINOR  | v1.1.0 | fitur baru      |
| PATCH  | v1.0.1 | bug fix         |

Contoh urutan:

```
v1.0.0 → release pertama
v1.0.1 → bug fix
v1.1.0 → fitur baru
v1.1.1 → hotfix
v2.0.0 → perubahan besar
```

---

# 🚀 Setup Private Registry (Server)

```bash
mkdir -p ~/server-hosting/registry
cd ~/server-hosting/registry
```

`docker-compose.yml`

```yaml
services:
  registry:
    image: registry:2
    container_name: private_registry
    ports:
      - "5000:5000"
    restart: always
    volumes:
      - ./data:/var/lib/registry
```

Jalankan:

```bash
docker compose up -d
```

Registry aktif:

```
http://SERVER_IP:5000
```

# ⚠️ Tambahkan Insecure Registry (Server)

Edit file konfigurasi docker
```bash
sudo nano /etc/docker/daemon.json
```
Docker Engine
```json
"insecure-registries": [
  "100.110.141.44:5000"
]
```
Restart Docker
```bash
sudo systemctl restart docker
```
---

# ⚠️ Tambahkan Insecure Registry (Laptop)

Docker Desktop → Docker Engine

```json
"insecure-registries": [
  "100.110.141.44:5000"
]
```

Restart Docker

---

# 🏗️ Build Image (SemVer)

```bash
docker build -t idn_solo_app:v1.0.0 .
docker build -t idn_solo_app:v1.1.0 .
docker build -t idn_solo_app:v1.1.1 .
```

---

# 🏷️ Tag ke Registry

```bash
docker tag idn_solo_app:v1.0.0 100.110.141.44:5000/idn_solo_app:v1.0.0
docker tag idn_solo_app:v1.1.0 100.110.141.44:5000/idn_solo_app:v1.1.0
docker tag idn_solo_app:v1.1.1 100.110.141.44:5000/idn_solo_app:v1.1.1
```

---

# 📤 Push Image

```bash
docker push 100.110.141.44:5000/idn_solo_app:v1.0.0
docker push 100.110.141.44:5000/idn_solo_app:v1.1.0
docker push 100.110.141.44:5000/idn_solo_app:v1.1.1
```

---

# 🌐 Mapping Domain → Versi

| Domain             | Versi  |
| ------------------ | ------ |
| idnsolo.my.id      | v1.0.0 |
| beta.idnsolo.my.id | v1.1.0 |
| dev.idnsolo.my.id  | v1.1.1 |

---

# 📥 Docker Compose per Versi

Production

```yaml
image: 100.110.141.44:5000/idn_solo_app:v1.0.0
ports:
  - "8084:80"
```

Beta

```yaml
image: 100.110.141.44:5000/idn_solo_app:v1.1.0
ports:
  - "8085:80"
```

---

# 🔄 Update Versi

```bash
docker pull 100.110.141.44:5000/idn_solo_app:v1.1.0
docker compose up -d
```

---

# ⏪ Rollback Cepat

Ganti versi:

```
v1.1.0 → v1.0.0
```

Lalu:

```bash
docker compose up -d
```

---

# 🧠 Workflow Deployment Aman

```
build v1.2.0
push registry
deploy beta
testing
switch production
```

---

# 📊 Strategy Versioning

| Tag    | Fungsi                      |
| ------ | --------------------------- |
| v1.0.0 | production stable           |
| v1.1.0 | fitur baru                  |
| v1.1.1 | hotfix                      |
| latest | optional (alias production) |

---

# 🔎 Cek Image di Registry

```bash
curl http://100.110.141.44:5000/v2/_catalog
```

---

# 🧹 Cleanup Image Lama

```bash
docker image prune -a
```

---

# 🚀 Full Workflow

Laptop:

```bash
# 1. Build image di lokal (beri tag versi spesifik)
docker build -t idn_solo_app:v1.2.0 .

# 2. Beri tag untuk Registry Pribadi (Versi Spesifik)
docker tag idn_solo_app:v1.2.0 100.110.141.44:5000/idn_solo_app:v1.2.0

# 3. Beri tag untuk Registry Pribadi (Sebagai Latest)
docker tag idn_solo_app:v1.2.0 100.110.141.44:5000/idn_solo_app:latest

# 4. Push keduanya ke server
docker push 100.110.141.44:5000/idn_solo_app:v1.2.0
docker push 100.110.141.44:5000/idn_solo_app:latest
```

Server:

```bash
# 1. Tarik image terbaru dari registry lokalmu
docker pull 100.110.141.44:5000/idn_solo_app:latest

# 2. Update container (Docker akan mendeteksi perubahan image)
docker compose up -d
```

---

# 🎯 Hasil

* multi versi app
* multi domain
* rollback cepat
* update tanpa downtime
* staging environment
* deployment profesional