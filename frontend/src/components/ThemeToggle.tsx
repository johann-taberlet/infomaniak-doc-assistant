import { useState, useEffect } from 'react';

export type Theme = 'light' | 'dark' | 'system';

const THEME_STORAGE_KEY = 'theme';
const THEME_ATTRIBUTE = 'data-theme';

/** Type guard to validate theme values from localStorage */
const isValidTheme = (value: string | null): value is Theme =>
  value === 'light' || value === 'dark' || value === 'system';

/** Safely read theme from localStorage with fallback */
const getStoredTheme = (): Theme => {
  try {
    const saved = localStorage.getItem(THEME_STORAGE_KEY);
    return isValidTheme(saved) ? saved : 'system';
  } catch (error) {
    console.warn('Failed to read theme from localStorage:', error);
    return 'system';
  }
};

/** Safely persist theme to localStorage */
const persistTheme = (theme: Theme): void => {
  try {
    localStorage.setItem(THEME_STORAGE_KEY, theme);
  } catch (error) {
    console.warn('Failed to persist theme to localStorage:', error);
  }
};

export function ThemeToggle() {
  const [theme, setTheme] = useState<Theme>(getStoredTheme);

  useEffect(() => {
    const root = document.documentElement;

    const applyTheme = (selectedTheme: Theme) => {
      if (selectedTheme === 'system') {
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        root.setAttribute(THEME_ATTRIBUTE, prefersDark ? 'dark' : 'light');
      } else {
        root.setAttribute(THEME_ATTRIBUTE, selectedTheme);
      }
    };

    applyTheme(theme);
    persistTheme(theme);

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
