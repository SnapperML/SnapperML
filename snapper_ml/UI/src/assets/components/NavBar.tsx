import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import "/node_modules/fontawesome-free/css/all.min.css";

const NavBar: React.FC = () => {
  const [isDarkMode, setIsDarkMode] = useState(false);

  useEffect(() => {
    if (isDarkMode) {
      document.body.classList.add("dark-mode");
      document.body.classList.remove("light-mode");
    } else {
      document.body.classList.add("light-mode");
      document.body.classList.remove("dark-mode");
    }
  }, [isDarkMode]);

  const handleThemeToggle = () => {
    setIsDarkMode(!isDarkMode);
  };

  return (
    <header>
      <nav className="navbar navbar-expand-lg">
        <Link className="navbar-brand" to="/">
          <img
            src="/snapper.png"
            alt="SnapperML Logo"
            style={{ height: "40px", marginRight: "10px" }}
          />
          SnapperML
        </Link>
        <button
          className="navbar-toggler"
          type="button"
          data-toggle="collapse"
          data-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav mr-auto">
            <li className="nav-item active">
              <Link className="nav-link" to="/">
                Home
              </Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/about">
                About
              </Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/contact">
                Contact
              </Link>
            </li>
          </ul>
        </div>
      </nav>
      <button
        className="btn btn-outline-secondary dark-mode-toggle"
        onClick={handleThemeToggle}
        aria-label="Toggle dark mode"
      >
        <i className={isDarkMode ? "fas fa-moon" : "fas fa-sun"}></i>
      </button>
    </header>
  );
};

export default NavBar;
