# 🚀 Cloud Todo Microservices Platform

## 📌 Overview

This project is a **containerized microservices platform** built using Docker and Docker Compose.

It demonstrates:

* Microservices architecture (Flask APIs)
* Reverse proxy with Nginx
* PostgreSQL database (persistent)
* Redis caching
* Monitoring (Prometheus / Grafana)
* CI/CD pipeline with GitHub Actions
* Scalability using Docker Compose

---

## 🏗️ Architecture

```
User → Nginx → Flask Services → PostgreSQL
                         ↘ Redis
```

* **Nginx**: Reverse proxy & load balancer
* **Flask Apps**: Microservices (Task API)
* **PostgreSQL**: Persistent database
* **Redis**: Cache layer
* **Monitoring**: Prometheus / Grafana

---

## ⚙️ Features

* ✅ Task management API (CRUD)
* ✅ Dockerized services
* ✅ Persistent storage with volumes
* ✅ Redis caching
* ✅ Load balancing
* ✅ Monitoring dashboard
* ✅ CI/CD pipeline

---

## 📦 Tech Stack

* Python (Flask)
* Docker & Docker Compose
* PostgreSQL
* Redis
* Nginx
* GitHub Actions

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/your-username/cloud-todo-microservices.git
cd cloud-todo-microservices
```

### 2. Run the project

```bash
docker-compose up --build
```

### 3. Access the app

```
http://localhost
```

---

## 🔌 API Endpoints

| Method | Endpoint    | Description   |
| ------ | ----------- | ------------- |
| GET    | /tasks      | Get all tasks |
| POST   | /tasks      | Create task   |
| DELETE | /tasks/{id} | Delete task   |

---

## 🧪 Scaling

```bash
docker-compose up --scale app1=3
```

---

## 📊 Monitoring

* Prometheus: `http://localhost:9090`
* Grafana: `http://localhost:3000`

---

## 🔐 Environment Variables

Create a `.env` file:

```
POSTGRES_DB=tasks
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin
```

---

## 🛠️ CI/CD

Pipeline includes:

* Build Docker image
* Push to Docker Hub
* Deploy using Docker Compose

---

## 📁 Project Structure

See `/services`, `/nginx`, `/monitoring`, `/docs`

---

## 📄 License

MIT License

---

## 👨‍💻 Author

* Your Name
