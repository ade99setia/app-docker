# 🐳 Docker CLI Advanced Guide

Dokumentasi command **yang lebih kuat dibanding Docker Desktop GUI**
Fokus: debugging, build, kontrol, backup, jaringan, cleanup, registry.

---

# 🕵️ Monitoring & Debugging

| Kebutuhan       | Command                                                                                      |
| --------------- | -------------------------------------------------------------------------------------------- |
| Log realtime    | `docker logs -f --tail 100 nama_container`                                                   |
| Masuk container | `docker exec -it nama_container /bin/sh`                                                     |
| CPU & RAM live  | `docker stats`                                                                               |
| Event docker    | `docker system events`                                                                       |
| Table rapi      | `docker ps -a --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"`              |
| IP container    | `docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' nama_container` |

Contoh:

```bash
docker logs -f --tail 100 app_undangan
```

---

# 🏗️ Build Image & Versioning

| Kebutuhan       | Command                                                                                      |
| --------------- | -------------------------------------------------------------------------------------------- |
| Build multi tag | `docker build -t repo:v1 -t repo:latest .`                                                   |
| Build no cache  | `docker build --no-cache -t repo:latest .`                                                   |
| Build secret    | `docker build --secret id=api_token,src=./rahasia.txt -t repo:latest .`                      |
| Tag ulang       | `docker tag ghcr.io/ade99setia/idn_solo_app:latest ghcr.io/ade99setia/idn_solo_app:v1.0.0`   |
| History layer   | `docker history repo:latest`                                                                 |

Contoh:

```bash
docker build -t ghcr.io/ade99setia/undangan_pernikahan:v5.2.4 -t ghcr.io/ade99setia/undangan_pernikahan:latest .
```

---

# 🛑 Kendali Container

| Kebutuhan      | Command                                                   |
| -------------- | --------------------------------------------------------- |
| Run background | `docker run -d --name app -p 8080:80 image`               |
| Rename         | `docker rename lama baru`                                 |
| Hapus paksa    | `docker rm -f nama_container`                             |
| Stop by filter | `docker stop $(docker ps -a -q --filter="name=undangan")` |

---

# 📦 Transfer File & Backup

| Kebutuhan           | Command                                |
| ------------------- | -------------------------------------- |
| Copy ke container   | `docker cp file container:/path`       |
| Copy dari container | `docker cp container:/path file`       |
| Save image          | `docker save -o backup.tar image`      |
| Load image          | `docker load -i backup.tar`            |
| Export container    | `docker export container > sistem.tar` |

---

# 🐙 Docker Compose

| Kebutuhan             | Command                              |
| --------------------- | ------------------------------------ |
| Rebuild & run         | `docker compose up -d --build`       |
| Stop & remove         | `docker compose down`                |
| Hapus termasuk volume | `docker compose down -v`             |
| Scale service         | `docker compose up -d --scale web=3` |

---

# 🌐 Network & Volume

| Kebutuhan       | Command                                                 |
| --------------- | ------------------------------------------------------- |
| Create network  | `docker network create jaringan_undangan`               |
| Connect network | `docker network connect jaringan_undangan app_undangan` |
| Inspect volume  | `docker volume inspect nama_volume`                     |

---

# 🧹 Cleanup & Disk

| Kebutuhan             | Command                  |
| --------------------- | ------------------------ |
| Disk usage            | `docker system df -v`    |
| Remove dangling image | `docker image prune -f`  |
| Full cleanup          | `docker system prune -a` |

⚠️ Aman untuk volume (tidak menghapus database)

---

# 🌍 Registry & Collaboration

| Kebutuhan     | Command                                                         |
| ------------- | --------------------------------------------------------------- |
| Login GHCR    | `echo "TOKEN" \| docker login ghcr.io -u user --password-stdin` |
| Push all tags | `docker push repo --all-tags`                                   |

Contoh:

```bash
echo "TOKEN_GITHUB_KAMU" | docker login ghcr.io -u ade99setia --password-stdin
```

---

# ⚡ Cheat Sheet Paling Sering Dipakai

| Tujuan          | Command                        |
| --------------- | ------------------------------ |
| Log realtime    | `docker logs -f container`     |
| Masuk container | `docker exec -it container sh` |
| CPU RAM         | `docker stats`                 |
| Rebuild compose | `docker compose up -d --build` |
| Cleanup         | `docker system prune -a`       |
| Copy file       | `docker cp`                    |
| Disk usage      | `docker system df -v`          |
| IP container    | `docker inspect`               |

---

# 🧠 Workflow Debug Cepat

```bash
docker ps
docker logs -f container
docker exec -it container sh
docker stats
docker inspect container
```

---

# 🚨 Emergency Cleanup

```bash
docker compose down
docker system prune -a
docker volume ls
```

---

# ✅ Catatan

* CLI lebih cepat dari GUI
* CLI bisa automation script
* CLI bisa remote SSH
* CLI bisa advanced debugging
* CLI bisa backup offline
