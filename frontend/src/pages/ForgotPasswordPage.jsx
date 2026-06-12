import { useState } from 'react';
import { Link } from 'react-router-dom';
import AuthForm from '../components/AuthForm';
import { requestPasswordReset } from '../api';
import { useApp } from '../context/AppContext';

export default function ForgotPasswordPage() {
  const { t } = useApp();
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setMessage(null);
    try {
      const data = await requestPasswordReset(email);
      setMessage(data.detail || t.resetEmailSent);
    } catch (err) {
      setError(err.message || t.authError);
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthForm
      title={t.forgotPasswordTitle}
      subtitle={t.forgotPasswordSubtitle}
      footer={<Link to="/login">{t.loginLink}</Link>}
    >
      <form className="auth-form" onSubmit={handleSubmit}>
        <label className="auth-form__field">
          <span>Email</span>
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required autoComplete="email" />
        </label>
        {message && <div className="success">{message}</div>}
        {error && <div className="error">{error}</div>}
        <button type="submit" className="btn btn--primary auth-form__submit" disabled={loading}>
          {loading ? t.loading : t.sendResetLink}
        </button>
      </form>
    </AuthForm>
  );
}
