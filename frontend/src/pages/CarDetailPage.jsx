import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { getCar } from '../api';
import { useApp } from '../context/AppContext';
import { fallbackPhoto } from '../utils/photos';
import CarComments from '../components/CarComments';

export default function CarDetailPage() {
  const { slug } = useParams();
  const { t } = useApp();
  const [car, setCar] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    getCar(slug)
      .then(setCar)
      .catch(() => setError(t.carNotFound))
      .finally(() => setLoading(false));
  }, [slug, t.carNotFound]);

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner" />
        {t.loading}
      </div>
    );
  }

  if (error || !car) {
    return <div className="error">{error || t.notFound}</div>;
  }

  const title = car.complect
    ? `${car.model} ${car.complect}`
    : car.model;

  return (
    <article className="car-detail">
      <Link to="/" className="back-link">{t.backToCatalog}</Link>

      <div className="car-detail__content">
        <div className="car-detail__mark">{car.mark.name}</div>
        <h1 className="car-detail__title">{title}</h1>
        <div className="car-detail__tags">
          <span className="tag">{car.year} {t.year}</span>
          {car.body && <span className="tag">{car.body.name}</span>}
        </div>
        <p className="car-detail__description">{car.description}</p>
      </div>

      <div className="car-detail__hero">
        <img
          className="car-detail__image"
          src={car.photo_display}
          alt={`${car.mark.name} ${title}`}
          onError={(e) => {
            e.target.src = fallbackPhoto(car);
          }}
        />
      </div>

      <CarComments carSlug={car.slug} />
    </article>
  );
}
