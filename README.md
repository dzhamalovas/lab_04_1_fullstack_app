# Lab 4.1 — Fullstack Application (Kubernetes)

## 📌 Описание

Полнофункциональное трехзвенное приложение, развернутое в Kubernetes.

Архитектура:
Frontend → Backend → Database

* Frontend: Streamlit
* Backend: FastAPI
* Database: PostgreSQL
* Контейнеризация: Docker
* Оркестрация: Kubernetes

---

## ⚙️ Функциональность

* Просмотр каталога товаров
* Поиск и фильтрация по категории
* Добавление товаров в корзину
* Удаление товаров из корзины
* Оформление заказа
* Автоматическое обновление остатков товаров

---

## 🧩 Архитектура взаимодействия

* Frontend обращается к Backend через `backend-service`
* Backend взаимодействует с PostgreSQL через `postgres-service`

---

## 🚀 Запуск проекта

### 1. Сборка Docker-образов

```bash
docker build -t my-backend ./src/backend
docker build -t my-frontend ./src/frontend
```

### 2. Импорт образов в MicroK8s

```bash
docker save my-backend > backend.tar
docker save my-frontend > frontend.tar

microk8s ctr image import backend.tar
microk8s ctr image import frontend.tar
```

### 3. Развертывание в Kubernetes

```bash
kubectl apply -f k8s/fullstack.yaml
```

### 4. Проверка

```bash
kubectl get pods
```

### 5. Доступ к приложению

```
http://localhost:30081
```

---

## 🔄 CI/CD

В проекте настроен CI pipeline (GitHub Actions / GitLab CI):

Проверяется:

* зависимости backend (FastAPI, SQLAlchemy)
* зависимости frontend (Streamlit)
* корректность Kubernetes YAML

Pipeline запускается автоматически при push в репозиторий.

---

## 📂 Структура проекта

```
src/
  backend/
  frontend/
k8s/
.github/
.gitlab-ci.yml
README.md
```
