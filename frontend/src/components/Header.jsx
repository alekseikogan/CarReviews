import { NavLink } from 'react-router-dom';

export default function Header() {
  return (
    <header className="header">
      <div className="header__inner">
        <NavLink to="/" className="logo">
          <div className="logo__icon">🚗</div>
          My<span>Cars</span>
        </NavLink>
        <nav className="nav">
          <NavLink
            to="/"
            className={({ isActive }) => `nav__link${isActive ? ' nav__link--active' : ''}`}
            end
          >
            Каталог
          </NavLink>
          <NavLink
            to="/about"
            className={({ isActive }) => `nav__link${isActive ? ' nav__link--active' : ''}`}
          >
            О проекте
          </NavLink>
        </nav>
      </div>
    </header>
  );
}
