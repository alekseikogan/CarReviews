export default function AboutPage() {
  return (
    <article className="about">
      <h1 className="about__title">О проекте</h1>
      <p className="about__text">
        MyCars — личный каталог автомобилей, на которых я когда-либо сидел за рулём.
        Здесь собраны впечатления от вождения: управляемость, комфорт, обзорность
        и всё то, что запоминается после поездки.
      </p>
      <p className="about__text">
        В каталоге 145 автомобилей — от отечественной классики ВАЗ и УАЗ
        до премиальных BMW, Mercedes, Lexus и спортивных Camaro, Mustang, GT86.
      </p>
      <h2 style={{ fontSize: '1.25rem', marginBottom: '1rem', fontWeight: 700 }}>
        Технологии
      </h2>
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
