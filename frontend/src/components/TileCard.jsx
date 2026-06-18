import { Link } from 'react-router-dom';
import { tileFallbackPhoto } from '../utils/photos';

export default function TileCard({ to, title, subtitle, image }) {
  return (
    <Link to={to} className="tile-card">
      <div className="tile-card__image-wrap">
        <img
          className="tile-card__image"
          src={image || tileFallbackPhoto()}
          alt={title}
          loading="lazy"
          onError={(e) => {
            e.target.src = tileFallbackPhoto();
          }}
        />
      </div>
      <div className="tile-card__body">
        <h2 className="tile-card__title">{title}</h2>
        {subtitle && <p className="tile-card__subtitle">{subtitle}</p>}
      </div>
    </Link>
  );
}
