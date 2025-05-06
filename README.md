# My Blog
FastAPI Backend + Next.js Frontend + MongoDB

---

## 🌟 What This Project Does
This project provides a full-stack web application template with the following features:

- **Frontend**: A modern, responsive user interface built with Next.js.
- **Backend**: A robust API server powered by FastAPI.
- **Database**: MongoDB for efficient and scalable data storage.

### Key Use Cases:
- Quickly set up a full-stack application with minimal configuration.
- Develop and test APIs with FastAPI's interactive documentation.
- Build and deploy modern web applications with Next.js.
- Seamlessly integrate with MongoDB for data persistence.

---

## 🚀 Getting Started

### 1. Clone Project
```bash
git clone https://github.com/TranMinhPhuc220420/my-blog.git
cd my-blog
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
