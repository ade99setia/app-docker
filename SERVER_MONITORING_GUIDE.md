# 📊 Server Monitoring & Security Guide

Panduan untuk memantau **performa, beban, keamanan, dan traffic server Ubuntu hosting Docker**

---

# 🚀 1. Beban Sistem & CPU

| Tujuan              | Command  | Keterangan   |
| ------------------- | -------- | ------------ |
| Monitoring realtime | `top`    | bawaan linux |
| Monitoring visual   | `htop`   | lebih rapi   |
| Load average        | `uptime` | 1,5,15 menit |

Install htop:

```bash
sudo apt install htop -y
```

Load average contoh:

```
load average: 0.15, 0.30, 0.25
```

Rule cepat:

| Load       | Kondisi  |
| ---------- | -------- |
| < CPU Core | Aman     |
| = CPU Core | Sibuk    |
| > CPU Core | Overload |

---

# 🌡️ 2. Suhu & Performa CPU

Install sensor:

```bash
sudo apt install lm-sensors -y
sudo sensors-detect
sensors
```

Install governor CPU:

```bash
sudo apt install cpufrequtils -y
```

Mode CPU:

| Mode        | Fungsi        |
| ----------- | ------------- |
| powersave   | hemat listrik |
| ondemand    | otomatis      |
| performance | maksimal      |

Set mode:

```bash
sudo cpufreq-set -r -g powersave
```

Cek status:

```bash
cpufreq-info
```

---

# 🧠 3. RAM & Storage

| Tujuan           | Command    |
| ---------------- | ---------- |
| Cek RAM          | `free -h`  |
| Cek disk         | `df -h`    |
| Cek folder besar | `du -sh *` |
| Storage visual   | `ncdu /`   |

Install ncdu:

```bash
sudo apt install ncdu -y
```

Interpretasi RAM:

| Field     | Arti         |
| --------- | ------------ |
| total     | total RAM    |
| used      | terpakai     |
| free      | kosong       |
| available | aman dipakai |

---

# 🌐 4. Traffic & Network

| Tujuan             | Command          |
| ------------------ | ---------------- |
| Port terbuka       | `sudo ss -tulnp` |
| Bandwidth realtime | `nload`          |
| IP koneksi aktif   | `sudo iftop`     |

Install tools:

```bash
sudo apt install nload -y
sudo apt install iftop -y
```

---

# 🕵️ 5. Keamanan Server

| Tujuan          | Command                          |
| --------------- | -------------------------------- |
| Status firewall | `sudo ufw status numbered`       |
| Login berhasil  | `last -a`                        |
| Brute force SSH | `sudo tail -f /var/log/auth.log` |

Jika banyak failed login → aktifkan fail2ban

---

# 🧩 6. Monitoring Docker

| Tujuan         | Command                    |
| -------------- | -------------------------- |
| CPU container  | `docker stats`             |
| List container | `docker ps`                |
| Logs realtime  | `docker logs -f container` |
| Inspect        | `docker inspect container` |

---

# 💽 7. Disk Usage Docker

| Tujuan            | Command                  |
| ----------------- | ------------------------ |
| Docker disk usage | `docker system df -v`    |
| Cleanup image     | `docker image prune -f`  |
| Cleanup full      | `docker system prune -a` |

---

# 🔎 8. Monitoring Process Berat

Cari proses makan CPU besar:

```bash
top
```

Sort CPU di htop:

```
Shift + P
```

Kill proses:

```bash
kill -9 PID
```

---

# 🚨 9. Tanda Server Bermasalah

| Gejala            | Penyebab    |
| ----------------- | ----------- |
| Website lambat    | CPU tinggi  |
| SSH delay         | RAM penuh   |
| Container restart | disk penuh  |
| MySQL mati        | OOM RAM     |
| nginx timeout     | load tinggi |

---

# ⚡ Quick Health Check

Jalankan berurutan:

```bash
uptime
free -h
df -h
docker stats
ss -tulnp
```

---

# 🧠 Workflow Monitoring Harian

```bash
htop
free -h
df -h
docker stats
sudo ufw status
last -a
```

---

# 🔐 Security Checklist

| Item                     | Status |
| ------------------------ | ------ |
| UFW aktif                | ✔      |
| SSH brute-force dicek    | ✔      |
| Port tidak perlu ditutup | ✔      |
| Disk tidak penuh         | ✔      |
| RAM cukup                | ✔      |
| CPU normal               | ✔      |

---

# 📊 Standar Aman Server Kecil

| Resource   | Aman           |
| ---------- | -------------- |
| CPU Load   | < 1.0 per core |
| RAM usage  | < 80%          |
| Disk usage | < 85%          |
| Temp CPU   | < 75°C         |
| Swap       | tidak aktif    |

---

# 🧪 Full Monitoring Command

```bash
uptime
htop
free -h
df -h
docker stats
ss -tulnp
sudo ufw status
last -a
```

---

# ✅ Tools Penting Terinstall

```bash
sudo apt install htop lm-sensors cpufrequtils nload iftop ncdu -y
```

---

# 🟢 Checklist Monitoring Mingguan

* cek disk
* cek RAM
* cek login SSH
* cek container restart
* cek load average
* cek suhu CPU
* cek port terbuka

---

# 🎯 Tujuan Monitoring

* mencegah crash server
* deteksi brute force
* deteksi DDoS
* optimasi performa
* kontrol resource
