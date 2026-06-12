import { useApp } from '../context/AppContext';

export default function Footer() {
  const { t } = useApp();

  return (
    <footer className="footer">
      <p>{t.footerText}</p>
      <p
        className="footer__credit"
        dangerouslySetInnerHTML={{ __html: t.iconCredit }}
      />
    </footer>
  );
}
