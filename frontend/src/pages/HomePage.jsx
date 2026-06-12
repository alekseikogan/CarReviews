import { useCallback, useEffect, useState } from 'react';
import { getCars, getMarks, getStats } from '../api';
import CarCard from '../components/CarCard';
import BrandFilter from '../components/BrandFilter';
import Pagination from '../components/Pagination';

export default function HomePage() {
  const [cars, setCars] = useState([]);
  const [marks, setMarks] = useState([]);
  const [stats, setStats] = useState(null);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [selectedMark, setSelectedMark] = useState('');
  const [search, setSearch] = useState('');
  const [searchInput, setSearchInput] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    getMarks().then(setMarks).catch(() => {});
    getStats().then(setStats).catch(() => {});
  }, []);

  const loadCars = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getCars({ page, mark: selectedMark, search });
      setCars(data.results);
      setTotalPages(Math.ceil(data.count / 12) || 1);
    } catch {
      setError('Не удалось загрузить автомобили. Проверьте, что backend запущен.');
    } finally {
      setLoading(false);
    }
  }, [page, selectedMark, search]);

  useEffect(() => {
    loadCars();
  }, [loadCars]);

  const handleMarkSelect = (slug) => {
    setSelectedMark(slug);
    setPage(1);
  };

  const handleSearch = (e) => {
    e.preventDefault();
    setSearch(searchInput);
    setPage(1);
  };

  return (
    <>
      <section className="hero">
        <div className="hero__badge">145 автомобилей · личный опыт</div>
        <h1 className="hero__title">Машины, на которых я ездил за рулём</h1>
        <p className="hero__subtitle">
          Каталог автомобилей с описанием впечатлений от вождения — от классики до современных кроссоверов
        </p>
        {stats && (
          <div className="stats">
            <div className="stat">
              <div className="stat__value">{stats.total_cars}</div>
              <div className="stat__label">Автомобилей</div>
            </div>
            <div className="stat">
              <div className="stat__value">{stats.total_marks}</div>
              <div className="stat__label">Марок</div>
            </div>
            <div className="stat">
              <div className="stat__value">{stats.total_bodies}</div>
              <div className="stat__label">Типов кузова</div>
            </div>
          </div>
        )}
      </section>

      <div className="filters">
        <form onSubmit={handleSearch} style={{ flex: 1, minWidth: '200px' }}>
          <input
            className="search-input"
            type="search"
            placeholder="Поиск по марке или модели..."
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
          Загрузка автомобилей...
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
            <div className="loading">Автомобили не найдены</div>
          )}
          <Pagination page={page} totalPages={totalPages} onPageChange={setPage} />
        </>
      )}
    </>
  );
}
