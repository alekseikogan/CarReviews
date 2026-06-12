import { useApp } from '../context/AppContext';

export default function BrandFilter({ marks, selected, onSelect }) {
  const { t } = useApp();

  return (
    <div className="brand-filter">
      <button
        type="button"
        className={`brand-chip${!selected ? ' brand-chip--active' : ''}`}
        onClick={() => onSelect('')}
      >
        {t.allBrands}
      </button>
      {marks.map((mark) => (
        <button
          key={mark.slug}
          type="button"
          className={`brand-chip${selected === mark.slug ? ' brand-chip--active' : ''}`}
          onClick={() => onSelect(mark.slug)}
        >
          {mark.name}
          <span className="brand-chip__count">{mark.car_count}</span>
        </button>
      ))}
    </div>
  );
}
