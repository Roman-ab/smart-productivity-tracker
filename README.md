A full-stack backend system built with **FastAPI, PostgreSQL, Redis, Docker, NGINX, and GitHub Actions CI/CD**, deployed on AWS EC2.

---

## 📌 Tech Stack

- ⚡ FastAPI (Python backend)
- 🐘 PostgreSQL (database)
- 🔴 Redis (caching layer)
- 🐳 Docker + Docker Compose
- 🌐 NGINX (reverse proxy)
- ☁️ AWS EC2 (deployment)
- 🔁 GitHub Actions (CI/CD pipeline)

---

## 🧠 System Architecture

Client → NGINX → FastAPI → PostgreSQL + Redis

---

## ⚙️ Setup Instructions

### Clone Repo
```bash
git clone https://github.com/<your-username>/smart-productivity-tracker.git
cd smart-productivity-tracker
```

### Run
```bash
docker compose up --build -d
```

---

## 🐘 PostgreSQL Access

```bash
docker exec -it postgres_db psql -U postgres
```

Commands:
\l  - list DBs
\c productivity_db
\dt
SELECT * FROM users;
SELECT * FROM tasks;
```

---

## 🔴 Redis Access

```bash
docker exec -it redis_cache redis-cli
```

Commands:
PING
KEYS *
GET user:<username>
```

---

## 📜 Logs

```bash
docker logs -f backend
docker logs -f postgres_db
docker logs -f redis_cache
```

---

## 💾 Backup

```bash
docker exec postgres_db pg_dump -U postgres productivity_db > backup.sql
```

---

## 📦 Volumes

```bash
docker volume ls
docker volume inspect <volume_name>
```

---

## 🐳 Containers

```bash
docker ps
docker exec -it backend bash
docker exec -it postgres_db bash
```

---

## 🔐 CI/CD

GitHub Actions:
Push → Build → Deploy to AWS via SSH

---

## 🌐 Deployment

```bash
docker compose up -d
```

---

## 🛠 Troubleshooting

```bash
docker compose down
docker compose up --build -d
sudo lsof -i :8000
```

---

## 👨‍💻 Author
Abhay Gupta
