export default function BrandFilter({ marks, selected, onSelect }) {
  return (
    <div className="brand-filter">
      <button
        type="button"
        className={`brand-chip${!selected ? ' brand-chip--active' : ''}`}
        onClick={() => onSelect('')}
      >
        Все
      </button>
      {marks.map((mark) => (
        <button
          key={mark.slug}
          type="button"
          className={`brand-chip${selected === mark.slug ? ' brand-chip--active' : ''}`}
          onClick={() => onSelect(mark.slug)}
        >
          {mark.name}
          <span style={{ opacity: 0.6, marginLeft: '0.3rem' }}>{mark.car_count}</span>
        </button>
      ))}
    </div>
  );
}
