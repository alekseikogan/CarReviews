import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import AuthForm from '../components/AuthForm';
import { useApp } from '../context/AppContext';
import { useAuth } from '../context/AuthContext';

export default function RegisterPage() {
  const { t } = useApp();
  const { register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({
    username: '',
    email: '',
    password: '',
    password_confirm: '',
  });
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const update = (key) => (e) => setForm((prev) => ({ ...prev, [key]: e.target.value }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      await register(form);
      navigate('/account');
    } catch (err) {
      setError(err.message || t.authError);
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthForm
      title={t.registerTitle}
      subtitle={t.registerSubtitle}
      footer={<Link to="/login">{t.loginLink}</Link>}
    >
      <form className="auth-form" onSubmit={handleSubmit}>
        <label className="auth-form__field">
          <span>{t.username}</span>
          <input value={form.username} onChange={update('username')} required autoComplete="username" />
        </label>
        <label className="auth-form__field">
          <span>Email</span>
          <input type="email" value={form.email} onChange={update('email')} required autoComplete="email" />
        </label>
        <label className="auth-form__field">
          <span>{t.password}</span>
          <input type="password" value={form.password} onChange={update('password')} required minLength={8} autoComplete="new-password" />
        </label>
        <label className="auth-form__field">
          <span>{t.passwordConfirm}</span>
          <input type="password" value={form.password_confirm} onChange={update('password_confirm')} required minLength={8} autoComplete="new-password" />
        </label>
        {error && <div className="error">{error}</div>}
        <button type="submit" className="btn btn--primary auth-form__submit" disabled={loading}>
          {loading ? t.loading : t.register}
        </button>
      </form>
    </AuthForm>
  );
}
