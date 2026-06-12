import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getBodies } from '../api';
import { useApp } from '../context/AppContext';
import { getBodyName } from '../utils/bodyNames';
import TileCard from '../components/TileCard';

export default function BodiesPage() {
  const { t, lang } = useApp();
  const [bodies, setBodies] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getBodies()
      .then((data) => setBodies(Array.isArray(data) ? data : data.results || []))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner" />
        {t.loading}
      </div>
    );
  }

  const sorted = [...bodies].sort((a, b) =>
    getBodyName(a, lang).localeCompare(getBodyName(b, lang), lang, { sensitivity: 'base' }),
  );

  return (
    <div className="directory-page">
      <Link to="/" className="back-link">{t.backToCatalog}</Link>
      <h1 className="directory-page__title">{t.bodiesPageTitle}</h1>
      <p className="directory-page__subtitle">{t.bodiesPageSubtitle}</p>
      <div className="tile-grid">
        {sorted.map((body) => (
          <TileCard
            key={body.slug}
            to={`/?body=${body.slug}`}
            title={getBodyName(body, lang)}
            subtitle={t.carsCount(body.car_count)}
            image={body.cover_photo}
            imageSeed={body.id}
          />
        ))}
      </div>
    </div>
  );
}
