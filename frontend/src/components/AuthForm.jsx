export default function AuthForm({ title, subtitle, children, footer }) {
  return (
    <section className="auth-page">
      <div className="auth-card">
        <h1 className="auth-card__title">{title}</h1>
        {subtitle && <p className="auth-card__subtitle">{subtitle}</p>}
        {children}
        {footer && <div className="auth-card__footer">{footer}</div>}
      </div>
    </section>
  );
}
