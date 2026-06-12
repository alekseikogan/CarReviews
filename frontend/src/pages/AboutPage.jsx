import { useApp } from '../context/AppContext';

export default function AboutPage() {
  const { t } = useApp();

  return (
    <article className="about">
      <h1 className="about__title">{t.aboutTitle}</h1>
      <p className="about__text">{t.aboutText1}</p>
      <p className="about__text">{t.aboutText2}</p>
      <h2 className="about__subtitle">{t.technologies}</h2>
      <div className="tech-stack">
        {['Django', 'Django REST Framework', 'PostgreSQL', 'React', 'Vite', 'Docker'].map(
          (tech) => (
            <span key={tech} className="tech-badge">{tech}</span>
          ),
        )}
      </div>
    </article>
  );
}
