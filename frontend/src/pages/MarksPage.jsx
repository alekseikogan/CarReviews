import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getMarks } from '../api';
import { useApp } from '../context/AppContext';
import TileCard from '../components/TileCard';

export default function MarksPage() {
  const { t } = useApp();
  const [marks, setMarks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getMarks()
      .then((data) => setMarks(Array.isArray(data) ? data : data.results || []))
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

  const sorted = [...marks].sort((a, b) =>
    a.name.localeCompare(b.name, 'ru', { sensitivity: 'base' }),
  );

  return (
    <div className="directory-page">
      <Link to="/" className="back-link">{t.backToCatalog}</Link>
      <h1 className="directory-page__title">{t.marksPageTitle}</h1>
      <p className="directory-page__subtitle">{t.marksPageSubtitle}</p>
      <div className="tile-grid">
        {sorted.map((mark) => (
          <TileCard
            key={mark.slug}
            to={`/?mark=${mark.slug}`}
            title={mark.name}
            subtitle={t.carsCount(mark.car_count)}
            image={mark.cover_photo}
          />
        ))}
      </div>
    </div>
  );
}
