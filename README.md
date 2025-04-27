# Project Title
FastAPI Backend + Next.js Frontend + MongoDB

---

## 🚀 Getting Started

### 1. Clone Project
```bash
git clone <your-repository-url>
cd <project-folder>
```

### 2. Run Application
```bash
make up
```
➔ This will start:
- Frontend (Next.js) at [http://localhost:3000](http://localhost:3000)
- Backend (FastAPI) at [http://localhost:8000](http://localhost:8000)
- MongoDB at [localhost:27017](localhost:27017)

---

## 🛠 Project Structure

```bash
project-root/
│
├── client/                     # Next.js Frontend
├── server/                     # FastAPI Backend
│
├── docker-compose.yml          # Main Docker Compose (FE + BE)
├── docker-compose.mongo.yml    # MongoDB Compose
├── docker-compose.override.yml # Dev volumes mount
│
├── Dockerfile-client           # Dockerfile for frontend
├── Dockerfile-server           # Dockerfile for backend
│
├── Makefile                    # Simplify docker-compose commands
└── README.md                   # This file
```

---

## ⚡ Development

| Command | Description |
|:--------|:------------|
| `make up` | Start all services (FE + BE + MongoDB) |
| `make up-build` | Build then start |
| `make down` | Stop all services |
| `make build` | Rebuild services |
| `make logs` | View realtime logs |
| `make prune` | Clean unused docker volumes |

---

## 📦 Production (Suggestion)

In production, you should:
- Use production-ready builds:
  - Frontend: `npm run build` and serve.
  - Backend: run `uvicorn` without `--reload`.
- Use environment variables for database connections.

Example production docker-compose file can be added separately.

---

## 🛡 Notes
- `docker-compose.override.yml` is auto-applied in development.
- Hot-reload is enabled for both frontend and backend.
- `node_modules` are excluded from bind mount to prevent issues.

---

## 📬 Contact

- Project Maintainer: [Minh Phúc](mailto:dev.minhphuc@gmail.com)

---
```

---
| Hot reload chuẩn chỉnh | ✅ |
| Makefile để quản lý lệnh nhanh | ✅ |
| README.md đẹp, chuyên nghiệp | ✅ |

---
