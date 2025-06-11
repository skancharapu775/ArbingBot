import {React, useEffect, useState} from 'react'
import { Moon, Sun } from 'lucide-react';

const ToggleTheme = () => {
    const [theme, setTheme] = useState("dark")
    useEffect(() => {
        const saved = localStorage.getItem("theme") || "dark";
        setTheme(saved);
      }, []);

    useEffect(() => {
        document.documentElement.setAttribute("data-theme", theme);
        localStorage.setItem("theme", theme);
    }, [theme]);

    const toggleTheme = () => {
        setTheme(prev => (prev === "light" ? "dark" : "light"));
    };
  return (
    <button onClick={toggleTheme} className="btn btn-sm btn-outline text-blue-700">
      {theme === "light" ? <Sun/> : <Moon/>}
    </button>
  )
}

export default ToggleTheme