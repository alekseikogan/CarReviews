import { NavLink } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { useAuth } from '../context/AuthContext';

export default function Header() {
  const { lang, setLang, theme, setTheme, t } = useApp();
  const { isAuthenticated, user } = useAuth();

  return (
    <header className="header">
      <div className="header__inner">
        <NavLink to="/" className="logo">
          <img src="/favicon-128.png" alt="DriveLog" className="logo__icon" />
          <span className="logo__word">
            Drive<span className="logo__accent">Log</span>
          </span>
        </NavLink>

        <nav className="nav">
          <NavLink
            to="/"
            className={({ isActive }) => `nav__link${isActive ? ' nav__link--active' : ''}`}
            end
          >
            {t.catalog}
          </NavLink>
          <NavLink
            to="/about"
            className={({ isActive }) => `nav__link${isActive ? ' nav__link--active' : ''}`}
          >
            {t.about}
          </NavLink>
        </nav>

        <div className="header__controls">
          <NavLink
            to={isAuthenticated ? '/account' : '/login'}
            className={({ isActive }) => `nav__link nav__link--account${isActive ? ' nav__link--active' : ''}`}
          >
            {isAuthenticated ? (user?.username || t.account) : t.login}
          </NavLink>

          <div className="theme-toggle" role="group" aria-label="Theme">
            <button
              type="button"
              className={`control-btn${theme === 'light' ? ' control-btn--active' : ''}`}
              onClick={() => setTheme('light')}
              title={t.themeLight}
            >
              ☀
            </button>
            <button
              type="button"
              className={`control-btn${theme === 'dark' ? ' control-btn--active' : ''}`}
              onClick={() => setTheme('dark')}
              title={t.themeDark}
            >
              ☾
            </button>
          </div>

          <div className="lang-toggle" role="group" aria-label="Language">
            <button
              type="button"
              className={`control-btn${lang === 'ru' ? ' control-btn--active' : ''}`}
              onClick={() => setLang('ru')}
            >
              RU
            </button>
            <button
              type="button"
              className={`control-btn${lang === 'en' ? ' control-btn--active' : ''}`}
              onClick={() => setLang('en')}
            >
              EN
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}
