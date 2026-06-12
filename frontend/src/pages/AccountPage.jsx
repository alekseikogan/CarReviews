import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import AuthForm from '../components/AuthForm';
import { updateMe } from '../api';
import { useApp } from '../context/AppContext';
import { useAuth } from '../context/AuthContext';

export default function AccountPage() {
  const { t } = useApp();
  const { user, loading, logout, refreshProfile } = useAuth();
  const navigate = useNavigate();
  const [firstName, setFirstName] = useState('');
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState(null);
  const [error, setError] = useState(null);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (!loading && !user) {
      navigate('/login');
    }
  }, [loading, user, navigate]);

  useEffect(() => {
    if (user) {
      setFirstName(user.first_name || '');
      setEmail(user.email || '');
    }
  }, [user]);

  if (loading || !user) {
    return <div className="loading"><div className="spinner" />{t.loading}</div>;
  }

  const handleSave = async (e) => {
    e.preventDefault();
    setSaving(true);
    setError(null);
    setMessage(null);
    try {
      await updateMe({ first_name: firstName, email });
      await refreshProfile();
      setMessage(t.profileSaved);
    } catch (err) {
      setError(err.message || t.authError);
    } finally {
      setSaving(false);
    }
  };

  return (
    <AuthForm title={t.accountTitle} subtitle={t.accountSubtitle}>
      <form className="auth-form" onSubmit={handleSave}>
        <label className="auth-form__field">
          <span>{t.username}</span>
          <input value={user.username} disabled />
        </label>
        <label className="auth-form__field">
          <span>{t.displayName}</span>
          <input value={firstName} onChange={(e) => setFirstName(e.target.value)} />
        </label>
        <label className="auth-form__field">
          <span>Email</span>
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </label>
        {message && <div className="success">{message}</div>}
        {error && <div className="error">{error}</div>}
        <button type="submit" className="btn btn--primary auth-form__submit" disabled={saving}>
          {saving ? t.loading : t.save}
        </button>
        <button type="button" className="btn btn--ghost auth-form__submit" onClick={() => { logout(); navigate('/'); }}>
          {t.logout}
        </button>
        <p className="auth-card__footer">
          <Link to="/forgot-password">{t.changePassword}</Link>
        </p>
      </form>
    </AuthForm>
  );
}
