import { useCallback, useEffect, useState } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { getCars, getMarks, getStats } from '../api';
import { useApp } from '../context/AppContext';
import CarCard from '../components/CarCard';
import BrandFilter from '../components/BrandFilter';
import Pagination from '../components/Pagination';

export default function HomePage() {
  const { t } = useApp();
  const [searchParams, setSearchParams] = useSearchParams();
  const [cars, setCars] = useState([]);
  const [marks, setMarks] = useState([]);
  const [stats, setStats] = useState(null);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [selectedMark, setSelectedMark] = useState(searchParams.get('mark') || '');
  const [selectedBody, setSelectedBody] = useState(searchParams.get('body') || '');
  const [search, setSearch] = useState('');
  const [searchInput, setSearchInput] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    getMarks()
      .then((data) => setMarks(Array.isArray(data) ? data : data.results || []))
      .catch(() => {});
    getStats().then(setStats).catch(() => {});
  }, []);

  useEffect(() => {
    const mark = searchParams.get('mark') || '';
    const body = searchParams.get('body') || '';
    setSelectedMark(mark);
    setSelectedBody(body);
    setPage(1);
  }, [searchParams]);

  const syncParams = useCallback((mark, body) => {
    const params = {};
    if (mark) params.mark = mark;
    if (body) params.body = body;
    setSearchParams(params);
  }, [setSearchParams]);

  const loadCars = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getCars({
        page,
        mark: selectedMark,
        body: selectedBody,
        search,
      });
      setCars(data.results);
      setTotalPages(Math.ceil(data.count / 12) || 1);
    } catch {
      setError(t.loadError);
    } finally {
      setLoading(false);
    }
  }, [page, selectedMark, selectedBody, search, t.loadError]);

  useEffect(() => {
    loadCars();
  }, [loadCars]);

  const handleMarkSelect = (slug) => {
    syncParams(slug, selectedBody);
  };

  const handleSearch = (e) => {
    e.preventDefault();
    setSearch(searchInput);
    setPage(1);
  };

  return (
    <>
      <section className="hero">
        <div className="hero__badge">{t.heroBadge}</div>
        <h1 className="hero__title">{t.heroTitle}</h1>
        <p className="hero__subtitle">{t.heroSubtitle}</p>
        {stats && (
          <div className="stats">
            <div className="stat">
              <div className="stat__value">{stats.total_cars}</div>
              <div className="stat__label">{t.statCars}</div>
            </div>
            <Link to="/marks" className="stat stat--clickable">
              <div className="stat__value">{stats.total_marks}</div>
              <div className="stat__label">{t.statMarks}</div>
            </Link>
            <Link to="/bodies" className="stat stat--clickable">
              <div className="stat__value">{stats.total_bodies}</div>
              <div className="stat__label">{t.statBodies}</div>
            </Link>
          </div>
        )}
      </section>

      <div className="filters">
        <form onSubmit={handleSearch} className="search-form">
          <input
            className="search-input"
            type="search"
            placeholder={t.searchPlaceholder}
            value={searchInput}
            onChange={(e) => setSearchInput(e.target.value)}
          />
        </form>
      </div>

      {marks.length > 0 && (
        <BrandFilter
          marks={marks}
          selected={selectedMark}
          onSelect={handleMarkSelect}
        />
      )}

      {loading && (
        <div className="loading">
          <div className="spinner" />
          {t.loadingCars}
        </div>
      )}

      {error && <div className="error">{error}</div>}

      {!loading && !error && (
        <>
          <div className="car-grid">
            {cars.map((car) => (
              <CarCard key={car.id} car={car} />
            ))}
          </div>
          {cars.length === 0 && (
            <div className="loading">{t.noCars}</div>
          )}
          <Pagination page={page} totalPages={totalPages} onPageChange={setPage} />
        </>
      )}
    </>
  );
}
