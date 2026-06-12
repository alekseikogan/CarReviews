import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import AuthForm from '../components/AuthForm';
import { useApp } from '../context/AppContext';
import { useAuth } from '../context/AuthContext';

export default function LoginPage() {
  const { t } = useApp();
  const { login } = useAuth();
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      await login(username, password);
      navigate('/account');
    } catch (err) {
      setError(err.message || t.authError);
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthForm
      title={t.loginTitle}
      subtitle={t.loginSubtitle}
      footer={(
        <>
          <Link to="/register">{t.registerLink}</Link>
          {' · '}
          <Link to="/forgot-password">{t.forgotPassword}</Link>
        </>
      )}
    >
      <form className="auth-form" onSubmit={handleSubmit}>
        <label className="auth-form__field">
          <span>{t.username}</span>
          <input value={username} onChange={(e) => setUsername(e.target.value)} required autoComplete="username" />
        </label>
        <label className="auth-form__field">
          <span>{t.password}</span>
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required autoComplete="current-password" />
        </label>
        {error && <div className="error">{error}</div>}
        <button type="submit" className="btn btn--primary auth-form__submit" disabled={loading}>
          {loading ? t.loading : t.login}
        </button>
      </form>
    </AuthForm>
  );
}
