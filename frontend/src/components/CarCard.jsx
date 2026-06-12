import { Link } from 'react-router-dom';

export default function CarCard({ car }) {
  const title = car.complect
    ? `${car.model} ${car.complect}`
    : car.model;

  return (
    <article className="car-card">
      <div className="car-card__image-wrap">
        <img
          className="car-card__image"
          src={car.photo_display}
          alt={`${car.mark.name} ${title}`}
          loading="lazy"
          onError={(e) => {
            e.target.src = `https://loremflickr.com/800/500/car,automobile?lock=${car.id}`;
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
        <Link to={`/cars/${car.slug}`} className="car-card__link">
          Подробнее →
        </Link>
      </div>
    </article>
  );
}
