import React, { useEffect, useState } from 'react';
import api from '../services/api';

function Accueil() {
  const [stats, setStats] = useState(null);
  const [derniersLivres, setDerniersLivres] = useState([]);

  useEffect(() => {
    chargerStats();
    chargerDerniersLivres();
  }, []);

  const chargerStats = async () => {
    try {
      const response = await api.get('/chatbot/statistiques/');
      setStats(response.data);
    } catch (error) {
      console.error('Erreur stats:', error);
    }
  };

  const chargerDerniersLivres = async () => {
    try {
      const response = await api.get('/livres/');
      // CORRECTION : Les livres sont dans response.data.results
      const livresData = response.data.results || response.data;
      // Prendre les 6 derniers livres
      setDerniersLivres(livresData.slice(0, 6));
    } catch (error) {
      console.error('Erreur livres:', error);
    }
  };

  return (
    <div className="accueil">
      <div className="hero-section">
        <h1>📚 Bienvenue à la Bibliothèque Intelligente</h1>
        <p>Découvrez notre catalogue de livres et interagissez avec notre assistant IA</p>
      </div>

      {stats && (
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-icon">📚</div>
            <div className="stat-number">{stats.total_livres}</div>
            <div className="stat-label">Livres total</div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">✅</div>
            <div className="stat-number">{stats.livres_disponibles}</div>
            <div className="stat-label">Livres disponibles</div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">📊</div>
            <div className="stat-number">{Math.round(stats.taux_disponibilite)}%</div>
            <div className="stat-label">Taux de disponibilité</div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">🔄</div>
            <div className="stat-number">{stats.emprunts_actifs}</div>
            <div className="stat-label">Emprunts actifs</div>
          </div>
        </div>
      )}

      <div className="derniers-livres">
        <h2>📖 Derniers livres ajoutés</h2>
        {derniersLivres.length === 0 ? (
          <p style={{ textAlign: 'center', padding: '2rem', background: 'white', borderRadius: '15px' }}>
            📭 Aucun livre pour le moment. Ajoutez-en dans la section "Gestion des Livres" !
          </p>
        ) : (
          <div className="livres-grid">
            {derniersLivres.map(livre => (
              <div key={livre.id_livre} className="livre-card">
                <h3>{livre.titre}</h3>
                <p className="auteur">Par {livre.auteur}</p>
                <p className="categorie">{livre.categorie_nom || 'Non catégorisé'}</p>
                <div className={`statut ${livre.statut}`}>
                  {livre.statut === 'disponible' ? '✅ Disponible' : 
                   livre.statut === 'emprunte' ? '📖 Emprunté' : '🔴 Indisponible'}
                </div>
                <p style={{ marginTop: '0.5rem', fontSize: '0.8rem', color: '#666' }}>
                  📊 {livre.quantite_disponible}/{livre.quantite_totale} exemplaires
                </p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default Accueil;