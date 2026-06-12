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

Security Group EC2: открыть **80** (HTTP).  
RDS: разрешить вход с security group EC2 на порт **5432**.

### Запуск

```bash
./scripts/deploy_ec2.sh
```

Скрипт собирает образ nginx (React `npm run build` внутри Docker) и поднимает контейнеры.

Вручную:

```bash
docker compose up -d --build
```

- **Сайт:** `http://<ec2-ip>/`
- **API:** `http://<ec2-ip>/api/`
- **Админка:** `http://<ec2-ip>/admin/`

Статика React вшита в образ nginx — не нужен `frontend/dist` на хосте.  
Фронтенд ходит в API по относительному пути `/api` (без порта 3000).
