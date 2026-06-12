import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { getCar } from '../api';

export default function CarDetailPage() {
  const { slug } = useParams();
  const [car, setCar] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    getCar(slug)
      .then(setCar)
      .catch(() => setError('Автомобиль не найден'))
      .finally(() => setLoading(false));
  }, [slug]);

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner" />
        Загрузка...
      </div>
    );
  }

  if (error || !car) {
    return <div className="error">{error || 'Не найдено'}</div>;
  }

  const title = car.complect
    ? `${car.model} ${car.complect}`
    : car.model;

  return (
    <article className="car-detail">
      <Link to="/" className="back-link">← Назад к каталогу</Link>

      <div className="car-detail__hero">
        <img
          className="car-detail__image"
          src={car.photo_display}
          alt={`${car.mark.name} ${title}`}
          onError={(e) => {
            e.target.src = `https://loremflickr.com/1200/675/car,automobile?lock=${car.id}`;
          }}
        />
      </div>

      <div className="car-detail__content">
        <div className="car-detail__mark">{car.mark.name}</div>
        <h1 className="car-detail__title">{title}</h1>
        <div className="car-detail__tags">
          <span className="tag">{car.year} год</span>
          {car.body && <span className="tag">{car.body.name}</span>}
        </div>
        <p className="car-detail__description">{car.description}</p>
      </div>
    </article>
  );
}
