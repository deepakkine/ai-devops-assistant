import { Moon, Sun } from "lucide-react";

import { useTheme } from "../../context/ThemeContext";

export default function ThemeToggle() {
  const { theme, toggleTheme } = useTheme();

  return (
    <button
      onClick={toggleTheme}
      className="flex items-center gap-2 rounded-lg border border-slate-300 bg-white px-4 py-2 text-slate-700 shadow transition hover:bg-slate-100 dark:border-slate-700 dark:bg-slate-800 dark:text-white dark:hover:bg-slate-700"
      title="Toggle Theme"
    >
      {theme === "dark" ? (
        <>
          <Sun size={18} />
          <span>Light</span>
        </>
      ) : (
        <>
          <Moon size={18} />
          <span>Dark</span>
        </>
      )}
    </button>
  );
}