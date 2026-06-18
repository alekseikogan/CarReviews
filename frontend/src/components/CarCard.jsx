import { Link } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { fallbackPhoto } from '../utils/photos';

export default function CarCard({ car }) {
  const { t } = useApp();
  const title = car.complect
    ? `${car.model} ${car.complect}`
    : car.model;

  return (
    <Link to={`/cars/${car.slug}`} className="car-card">
      <div className="car-card__image-wrap">
        <img
          className="car-card__image"
          src={car.photo_display || fallbackPhoto()}
          alt={`${car.mark.name} ${title}`}
          loading="lazy"
          onError={(e) => {
            e.target.src = fallbackPhoto();
          }}
        />
        <span className="car-card__year">{car.year}</span>
      </div>
      <div className="car-card__body">
        <div className="car-card__mark">{car.mark.name}</div>
        <h2 className="car-card__title">{title}</h2>
        <div className="car-card__meta">
          {car.body && <span className="tag">{car.body.name}</span>}
        </div>
        <p className="car-card__desc">{car.description}</p>
        <span className="car-card__link">{t.readMore}</span>
      </div>
    </Link>
  );
}
