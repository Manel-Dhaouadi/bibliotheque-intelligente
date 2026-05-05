import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Accueil from './pages/Accueil';
import GestionLivres from './pages/GestionLivres';
import GestionCategories from './pages/GestionCategories';  // Ajout
import ChatbotPage from './pages/ChatbotPage';
import './App.css';

function App() {
  return (
    <Router>
      <div className="app">
        <nav className="navbar">
          <div className="nav-container">
            <div className="nav-brand">📚 Bibliothèque Intelligente</div>
            <div className="nav-links">
              <Link to="/">🏠 Accueil</Link>
              <Link to="/livres">📖 Livres</Link>
              <Link to="/categories">🏷️ Catégories</Link>  {/* Ajout */}
              <Link to="/chatbot">🤖 Chatbot IA</Link>
            </div>
          </div>
        </nav>
        
        <div className="container">
          <Routes>
            <Route path="/" element={<Accueil />} />
            <Route path="/livres" element={<GestionLivres />} />
            <Route path="/categories" element={<GestionCategories />} />
            <Route path="/chatbot" element={<ChatbotPage />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;