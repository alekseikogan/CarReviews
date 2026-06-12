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

```bash
python manage.py load_cars          # загрузить, если БД пуста
python manage.py load_cars --force  # пересоздать все записи
```
