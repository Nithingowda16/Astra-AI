import React from 'react';
import { Sun, Moon } from 'lucide-react';

export default function ThemeToggle({ theme, toggleTheme }) {
  const isDark = theme === 'dark';

  return (
    <button
      type="button"
      className={`theme-switch ${isDark ? 'is-dark' : 'is-light'}`}
      onClick={toggleTheme}
      title={isDark ? 'Switch to White / Light Mode' : 'Switch to Dark Mode'}
      aria-label="Toggle visual theme"
    >
      <div className="theme-switch-track">
        <Sun size={12} className="switch-icon sun-icon" />
        <Moon size={12} className="switch-icon moon-icon" />
        <span className="theme-switch-slider">
          {isDark ? (
            <Moon size={11} className="slider-icon moon-color" />
          ) : (
            <Sun size={11} className="slider-icon sun-color" />
          )}
        </span>
      </div>
    </button>
  );
}
