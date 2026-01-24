import { useState, useEffect } from 'react';

type Theme = 'light' | 'dark' | 'system';

export function ThemeToggle() {
  const [theme, setTheme] = useState<Theme>(() => {
    const saved = localStorage.getItem('theme') as Theme | null;
    return saved || 'system';
  });

  useEffect(() => {
    const root = document.documentElement;

    const applyTheme = (selectedTheme: Theme) => {
      if (selectedTheme === 'system') {
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        root.setAttribute('data-theme', prefersDark ? 'dark' : 'light');
      } else {
        root.setAttribute('data-theme', selectedTheme);
      }
    };

    applyTheme(theme);
    localStorage.setItem('theme', theme);

    // Listen for system theme changes when in system mode
    if (theme === 'system') {
      const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
      const handleChange = () => applyTheme('system');
      mediaQuery.addEventListener('change', handleChange);
      return () => mediaQuery.removeEventListener('change', handleChange);
    }
  }, [theme]);

  const toggleTheme = () => {
    setTheme((current) => {
      if (current === 'light') return 'dark';
      if (current === 'dark') return 'system';
      return 'light';
    });
  };

  const getIcon = () => {
    if (theme === 'light') return '☀️';
    if (theme === 'dark') return '🌙';
    return '🖥️';
  };

  const getLabel = () => {
    if (theme === 'light') return 'Light';
    if (theme === 'dark') return 'Dark';
    return 'Auto';
  };

  return (
    <button
      className="flex items-center gap-1.5 px-3 py-1.5 bg-[var(--ik-bg-secondary)] border border-[var(--ik-border)] rounded-[var(--ik-radius-sm)] cursor-pointer text-[0.8125rem] text-[var(--ik-text-secondary)] transition-all duration-200 hover:bg-[var(--ik-bg-tertiary)] hover:border-[var(--ik-primary)] hover:text-[var(--ik-primary)]"
      onClick={toggleTheme}
      aria-label={`Current theme: ${theme}. Click to change.`}
      title={`Theme: ${getLabel()}`}
    >
      <span className="text-base leading-none">{getIcon()}</span>
      <span className="font-medium">{getLabel()}</span>
    </button>
  );
}
