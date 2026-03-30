Berikut dokumentasi **lengkap & detail** sesuai permintaanmu — urutan:

1. FILESERVER
2. PORTAINER
3. XRDP
   dan **username diganti jadi `adesetia`** seperti kamu minta.
   Saya rapikan supaya tetap **ringkas tapi teknis** 💼✨

---

# 🗂️ Infrastruktur Tambahan Server

## 1️⃣ Fileserver (FileBrowser)

### Setup Container

```bash
# 1. Masuk ke folder dan siapkan tempatnya
cd ~/app-docker/1-docker-containers
mkdir -p filebrowser
cd filebrowser
touch filebrowser.db

# 2. Bikin file docker-compose.yml otomatis via CLI
cat << 'EOF' > docker-compose.yml
services:
  filebrowser:
    image: filebrowser/filebrowser:latest
    container_name: filebrowser
    ports:
      - "8085:80"
    volumes:
      - /home/ade-setia:/srv
      - ./filebrowser.db:/database/filebrowser.db
    environment:
      - FB_DATABASE=/database/filebrowser.db
    restart: always
EOF

# 3. Jalankan container
docker-compose up -d
```

### Buat User Admin Fileserver

```bash
# Masuk folder
cd ~/app-docker/1-docker-containers/filebrowser

# Stop container
docker stop filebrowser

# Buat user admin
docker run --rm \
-v /home/ade-setia/app-docker/1-docker-containers/filebrowser/filebrowser.db:/database/filebrowser.db \
filebrowser/filebrowser \
users add adesetia "adesetia*0903" --perm.admin

# Start kembali
docker start filebrowser
```

### Kalo buat akun gagal lakukan ini
```bash
docker compose down; \
sudo rm -rf filebrowser.db; \
touch filebrowser.db; \
docker compose run --rm filebrowser config init; \
docker compose run --rm filebrowser users add adesetia "adesetia*0903" --perm.admin; \
docker compose up -d
```

### Akses Fileserver

```
http://IP_SERVER:8085
```

---

## 2️⃣ Portainer (Docker Management UI)

### Setup Portainer

```bash
# Buat volume data
docker volume create portainer_data

# Jalankan Portainer
docker run -d \
-p 8000:8000 \
-p 9000:9000 \
--name portainer \
--restart=always \
-v /var/run/docker.sock:/var/run/docker.sock \
-v portainer_data:/data \
portainer/portainer-ce:latest
```

### Akses Portainer

```
http://IP_SERVER:9000
```

---

## 3️⃣ XRDP Remote Desktop

### Setup User Remote

```bash
REMOTE_USER="adesetia_remote"
REMOTE_PASS="adesetia*0903"

sudo useradd -m -s /bin/bash $REMOTE_USER
echo "$REMOTE_USER:$REMOTE_PASS" | sudo chpasswd
sudo usermod -aG sudo $REMOTE_USER
```

### Install XRDP

```bash
sudo apt update
sudo apt install xrdp -y
sudo adduser xrdp ssl-cert
sudo systemctl enable --now xrdp
sudo systemctl restart xrdp
```

---

### Install Desktop XFCE

```bash
sudo apt update
sudo apt install xfce4 xfce4-goodies -y

sudo su - adesetia_remote
echo "startxfce4" > ~/.xsession
exit

sudo systemctl restart xrdp
```

---

### Permission Akses Fileserver

```bash
sudo usermod -aG adesetia adesetia_remote
sudo chmod 750 /home/ade-setia
sudo chmod -R 775 /home/ade-setia/app-docker/1-docker-containers

sudo -u adesetia_remote ln -s \
/home/ade-setia/app-docker/1-docker-containers \
/home/ade-setia_remote/Desktop/app-docker/1-docker-containers
```

---

### Cara Login Remote Desktop

1. Buka **Remote Desktop Connection** di Windows
2. Masukkan IP server
3. Klik Connect
4. Login dengan:

```
Username : adesetia_remote
Password : adesetia*0903
```

---

# 🔌 Port Tambahan Digunakan

| Port | Service     | Keterangan        |
| ---- | ----------- | ----------------- |
| 8085 | Filebrowser | Fileserver Web UI |
| 9000 | Portainer   | Docker Dashboard  |
| 3389 | XRDP        | Remote Desktop    |

---

# 📊 Ringkasan Infrastruktur Tambahan

| Service    | Container   | Port | Storage        | Fungsi           |
| ---------- | ----------- | ---- | -------------- | ---------------- |
| Fileserver | filebrowser | 8085 | filebrowser.db | Web File Manager |
| Portainer  | portainer   | 9000 | portainer_data | Docker UI        |
| XRDP       | xrdp        | 3389 | system         | Remote Desktop   |

---
