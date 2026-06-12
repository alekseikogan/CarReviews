import { createContext, useContext, useEffect, useMemo, useState } from 'react';
import { translations } from '../i18n/translations';

const AppContext = createContext(null);

export function AppProvider({ children }) {
  const [lang, setLang] = useState(() => localStorage.getItem('lang') || 'ru');
  const [theme, setTheme] = useState(() => localStorage.getItem('theme') || 'dark');

  const t = translations[lang];

  useEffect(() => {
    document.documentElement.lang = lang;
    document.documentElement.dataset.theme = theme;
    document.title = t.pageTitle;
    localStorage.setItem('lang', lang);
    localStorage.setItem('theme', theme);
  }, [lang, theme, t.pageTitle]);

  const value = useMemo(
    () => ({
      lang,
      setLang,
      theme,
      setTheme,
      t,
    }),
    [lang, theme, t],
  );

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
}

export function useApp() {
  const ctx = useContext(AppContext);
  if (!ctx) throw new Error('useApp must be used within AppProvider');
  return ctx;
}
