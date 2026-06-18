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
python manage.py download_car_photos      # привязать фото из media/cars/
python manage.py download_car_photos --force
python manage.py export_cars              # экспорт БД → fixtures/cars.json
```

### Скрипты (из корня проекта)

```powershell
.\scripts\import_data.ps1           # импорт
.\scripts\import_data.ps1 -Force
.\scripts\export_data.ps1           # экспорт
.\scripts\download_photos.ps1       # привязать локальные фото
```

```bash
./scripts/import_data.sh
./scripts/export_data.sh
./scripts/download_photos.sh
```
