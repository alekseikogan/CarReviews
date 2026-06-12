export default function Pagination({ page, totalPages, onPageChange }) {
  if (totalPages <= 1) return null;

  return (
    <div className="pagination">
      <button
        type="button"
        className="pagination__btn"
        disabled={page <= 1}
        onClick={() => onPageChange(page - 1)}
      >
        ← Назад
      </button>
      <span className="pagination__info">
        {page} / {totalPages}
      </span>
      <button
        type="button"
        className="pagination__btn"
        disabled={page >= totalPages}
        onClick={() => onPageChange(page + 1)}
      >
        Вперёд →
      </button>
    </div>
  );
}
