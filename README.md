# MyCars 🚗

**MyCars** — каталог автомобилей, на которых я ездил за рулём.  
145 машин с описаниями, фотографиями и личными впечатлениями от вождения.

---

## Стек

- **Backend:** Django 4.2 + Django REST Framework
- **Frontend:** React 18 + Vite
- **База данных:** PostgreSQL 16
- **Инфраструктура:** Docker Compose (3 контейнера)

## Быстрый старт

```bash
docker compose up --build
```

После запуска:

- **Фронтенд:** http://localhost:3000
- **API:** http://localhost:8000/api/
- **Админка:** http://localhost:8000/admin/

## Локальная разработка

### Backend

```bash
cd my_cars
pip install -r ../requirements.txt
# Запустите PostgreSQL (или через docker compose up db)
python manage.py migrate
python manage.py load_cars
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## API

| Endpoint | Описание |
|----------|----------|
| `GET /api/cars/` | Список автомобилей (пагинация, фильтр `?mark=bmw`, поиск `?search=camry`) |
| `GET /api/cars/{slug}/` | Детали автомобиля |
| `GET /api/marks/` | Список марок |
| `GET /api/cars/stats/` | Статистика |

## Загрузка данных

Данные хранятся в **`my_cars/fixtures/cars.json`** (145 машин, марки, кузова).  
Фото — в **`my_cars/media/cars/`** (локально на диске, без внешних URL при отдаче).

### Docker (автоматически)

При `docker compose up` backend выполняет `import_cars` — читает fixture и привязывает фото с диска.

### Вручную

```bash
cd my_cars
python manage.py migrate
python manage.py import_cars              # импорт из fixtures/cars.json
python manage.py import_cars --force      # пересоздать БД из fixture

python manage.py generate_fixture         # пересобрать cars.json из cars_data.py
python manage.py download_car_photos      # скачать фото в media/cars/
python manage.py download_car_photos --force
python manage.py export_cars              # экспорт БД → fixtures/cars.json
```

### Скрипты (из корня проекта)

```powershell
.\scripts\import_data.ps1           # импорт
.\scripts\import_data.ps1 -Force
.\scripts\export_data.ps1           # экспорт
.\scripts\download_photos.ps1       # скачать все фото
```

```bash
./scripts/import_data.sh
./scripts/export_data.sh
./scripts/download_photos.sh
```

## Workflow: `main` и `for_ec2_amazon`

Две ветки — один код приложения, разная инфраструктура.

| Ветка | Где работает | Docker |
|-------|--------------|--------|
| **`main`** | Локально (ПК) | `db` + `backend` + `frontend` (:3000) |
| **`for_ec2_amazon`** | Прод (EC2) | `backend` + `nginx` (HTTPS), БД — **RDS** |

### Локальная разработка (`main`)

```bash
git checkout main
docker compose up --build
```

- **Сайт:** http://localhost:3000  
- **API:** http://localhost:8000/api/  
- **БД:** контейнер `db` на компьютере  

Альтернатива без фронтенд-контейнера:

```bash
docker compose up db backend
cd frontend && npm run dev
```

### Выкладка на прод

```bash
git checkout for_ec2_amazon
git merge main
git push origin for_ec2_amazon
```

На EC2:

```bash
cd ~/Dev/CarReviews
git pull origin for_ec2_amazon
docker compose up -d --build
```

Файл `.env` на сервере не коммитится — там RDS, домен и секреты. При деплое его не перезаписывай.

### Два разных `.env`

| Переменная | Локально (`main`) | EC2 (`for_ec2_amazon`) |
|------------|-------------------|------------------------|
| `POSTGRES_HOST` | `db` (в docker-compose) | endpoint RDS |
| `CORS_ALLOWED_ORIGINS` | `http://localhost:3000` | `https://drivelog.live,...` |
| `DOMAIN` | не нужен | `drivelog.live` |

### Конфликты при merge

Чаще всего в `docker-compose.yml`, `nginx.conf`, `README`.  
Правило: в каждой ветке оставляй **свою** инфраструктурную версию файла — код Django/React мержится как обычно.

```text
ПК:  feature → main  →  merge  →  for_ec2_amazon  →  push
                                        ↓
EC2:                              git pull + docker compose up
```

**Не веди разработку постоянно в `for_ec2_amazon`** — только merge из `main` и правки, специфичные для прода (nginx, SSL).

## Деплой на AWS EC2 (ветка `for_ec2_amazon`)

Стек: **Nginx (порт 80)** + **Django backend** + **RDS PostgreSQL** (без контейнера `db`).

### Подготовка на сервере

```bash
git clone https://github.com/alekseikogan/CarReviews.git
cd CarReviews
git checkout for_ec2_amazon

cp .env.example .env
# отредактируйте .env: RDS endpoint, пароль, ALLOWED_HOSTS (IP/домен EC2)
```

Security Group EC2: **80** (HTTP), **443** (HTTPS).  
RDS: PostgreSQL **5432** ← security group EC2.

### Запуск

```bash
./scripts/deploy_ec2.sh
```

Скрипт собирает образ nginx (React `npm run build` внутри Docker) и поднимает контейнеры.

Вручную:

```bash
docker compose up -d --build
```

- **Сайт:** `https://drivelog.live/`
- **API:** `/api/`
- **Админка:** `/admin/`

### HTTPS (Let's Encrypt)

В `.env`:

```env
DOMAIN=drivelog.live
CERTBOT_EMAIL=you@example.com
CORS_ALLOWED_ORIGINS=https://drivelog.live,https://www.drivelog.live
CSRF_TRUSTED_ORIGINS=https://drivelog.live,https://www.drivelog.live
```

На EC2:

```bash
git pull
chmod +x scripts/init-letsencrypt.sh
docker compose up -d --build
./scripts/init-letsencrypt.sh
docker compose up -d --build backend
```

Скрипт получает сертификат, включает HTTPS в nginx и поднимает автообновление certbot.
