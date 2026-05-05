import React from 'react';
import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav className="navbar">
      <div className="nav-container">
        <div className="nav-brand">
          <Link to="/" style={{ textDecoration: 'none', color: 'inherit' }}>
            📚 Bibliothèque Intelligente
          </Link>
        </div>
        <div className="nav-links">
          <Link to="/">🏠 Accueil</Link>
          <Link to="/livres">📖 Livres</Link>
          <Link to="/chatbot">🤖 Chatbot</Link>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;