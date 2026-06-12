import { useCallback, useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { deleteComment, getCarComments, postCarComment } from '../api';
import { useApp } from '../context/AppContext';
import { useAuth } from '../context/AuthContext';

export default function CarComments({ carSlug }) {
  const { t } = useApp();
  const { isAuthenticated } = useAuth();
  const [comments, setComments] = useState([]);
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  const loadComments = useCallback(async () => {
    setLoading(true);
    try {
      const data = await getCarComments(carSlug);
      setComments(Array.isArray(data) ? data : []);
    } catch {
      setError(t.commentsLoadError);
    } finally {
      setLoading(false);
    }
  }, [carSlug, t.commentsLoadError]);

  useEffect(() => {
    loadComments();
  }, [loadComments]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const trimmed = text.trim();
    if (!trimmed) return;
    setSubmitting(true);
    setError(null);
    try {
      const comment = await postCarComment(carSlug, trimmed);
      setComments((prev) => [comment, ...prev]);
      setText('');
    } catch (err) {
      setError(err.message || t.commentsPostError);
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (id) => {
    try {
      await deleteComment(id);
      setComments((prev) => prev.filter((c) => c.id !== id));
    } catch (err) {
      setError(err.message || t.commentsDeleteError);
    }
  };

  return (
    <section className="comments">
      <h2 className="comments__title">{t.commentsTitle}</h2>

      {isAuthenticated ? (
        <form className="comments__form" onSubmit={handleSubmit}>
          <textarea
            className="comments__input"
            rows={3}
            placeholder={t.commentPlaceholder}
            value={text}
            onChange={(e) => setText(e.target.value)}
            maxLength={2000}
          />
          <button type="submit" className="btn btn--primary" disabled={submitting || !text.trim()}>
            {submitting ? t.sending : t.commentSubmit}
          </button>
        </form>
      ) : (
        <p className="comments__login-hint">
          {t.commentLoginHint}{' '}
          <Link to="/login">{t.login}</Link>
        </p>
      )}

      {error && <div className="error comments__error">{error}</div>}

      {loading ? (
        <div className="comments__loading">{t.loading}</div>
      ) : comments.length === 0 ? (
        <p className="comments__empty">{t.commentsEmpty}</p>
      ) : (
        <ul className="comments__list">
          {comments.map((comment) => (
            <li key={comment.id} className="comment">
              <div className="comment__header">
                <span className="comment__author">{comment.author_name}</span>
                <time className="comment__date">
                  {new Date(comment.time_create).toLocaleString()}
                </time>
              </div>
              <p className="comment__text">{comment.text}</p>
              {comment.is_owner && (
                <button
                  type="button"
                  className="comment__delete"
                  onClick={() => handleDelete(comment.id)}
                >
                  {t.commentDelete}
                </button>
              )}
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
