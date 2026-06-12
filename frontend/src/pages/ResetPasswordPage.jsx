import { useState } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import AuthForm from '../components/AuthForm';
import { confirmPasswordReset } from '../api';
import { useApp } from '../context/AppContext';

export default function ResetPasswordPage() {
  const { t } = useApp();
  const [params] = useSearchParams();
  const [password, setPassword] = useState('');
  const [passwordConfirm, setPasswordConfirm] = useState('');
  const [message, setMessage] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const uid = params.get('uid');
  const token = params.get('token');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (password !== passwordConfirm) {
      setError(t.passwordMismatch);
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const data = await confirmPasswordReset({ uid, token, password });
      setMessage(data.detail || t.passwordUpdated);
    } catch (err) {
      setError(err.message || t.authError);
    } finally {
      setLoading(false);
    }
  };

  if (!uid || !token) {
    return (
      <AuthForm title={t.resetPasswordTitle} footer={<Link to="/forgot-password">{t.forgotPassword}</Link>}>
        <div className="error">{t.resetLinkInvalid}</div>
      </AuthForm>
    );
  }

  return (
    <AuthForm
      title={t.resetPasswordTitle}
      subtitle={t.resetPasswordSubtitle}
      footer={message ? <Link to="/login">{t.loginLink}</Link> : null}
    >
      <form className="auth-form" onSubmit={handleSubmit}>
        <label className="auth-form__field">
          <span>{t.newPassword}</span>
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required minLength={8} />
        </label>
        <label className="auth-form__field">
          <span>{t.passwordConfirm}</span>
          <input type="password" value={passwordConfirm} onChange={(e) => setPasswordConfirm(e.target.value)} required minLength={8} />
        </label>
        {message && <div className="success">{message}</div>}
        {error && <div className="error">{error}</div>}
        {!message && (
          <button type="submit" className="btn btn--primary auth-form__submit" disabled={loading}>
            {loading ? t.loading : t.savePassword}
          </button>
        )}
      </form>
    </AuthForm>
  );
}
