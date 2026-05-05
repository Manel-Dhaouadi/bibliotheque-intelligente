import React, { useState, useEffect } from 'react';
import api from '../services/api';

function GestionLivres() {
  const [livres, setLivres] = useState([]);
  const [livresFiltres, setLivresFiltres] = useState([]);
  const [categories, setCategories] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [editingLivre, setEditingLivre] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [searchType, setSearchType] = useState('titre'); // 'titre', 'auteur', 'id'
  const [formData, setFormData] = useState({
    titre: '',
    auteur: '',
    categorie: '',
    annee_publication: new Date().getFullYear(),
    quantite_disponible: 1,
    quantite_totale: 1
  });

  useEffect(() => {
    chargerLivres();
    chargerCategories();
  }, []);

  useEffect(() => {
    filtrerLivres();
  }, [searchTerm, searchType, livres]);

  const chargerLivres = async () => {
    try {
      const response = await api.get('/livres/');
      const livresData = response.data.results || response.data;
      setLivres(livresData);
      setLivresFiltres(livresData);
    } catch (error) {
      console.error('Erreur:', error);
      alert('Erreur lors du chargement des livres');
    }
  };

  const chargerCategories = async () => {
    try {
      const response = await api.get('/categories/');
      const categoriesData = response.data.results || response.data;
      setCategories(categoriesData);
    } catch (error) {
      console.error('Erreur catégories:', error);
    }
  };

  const filtrerLivres = () => {
    if (!searchTerm.trim()) {
      setLivresFiltres(livres);
      return;
    }

    const term = searchTerm.toLowerCase().trim();
    
    const filtres = livres.filter(livre => {
      if (searchType === 'titre') {
        return livre.titre?.toLowerCase().includes(term);
      } else if (searchType === 'auteur') {
        return livre.auteur?.toLowerCase().includes(term);
      } else if (searchType === 'id') {
        return livre.id_livre?.toString() === term;
      }
      return false;
    });
    
    setLivresFiltres(filtres);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.titre || !formData.auteur) {
      alert('Veuillez remplir le titre et l\'auteur');
      return;
    }

    if (formData.quantite_disponible > formData.quantite_totale) {
      alert('La quantité disponible ne peut pas dépasser la quantité totale');
      return;
    }

    const dataToSend = {
      titre: formData.titre,
      auteur: formData.auteur,
      annee_publication: parseInt(formData.annee_publication),
      quantite_totale: parseInt(formData.quantite_totale),
      quantite_disponible: parseInt(formData.quantite_disponible)
    };

    if (formData.categorie) {
      dataToSend.categorie = parseInt(formData.categorie);
    }

    try {
      if (editingLivre) {
        await api.put(`/livres/${editingLivre.id_livre}/`, dataToSend);
        alert('Livre modifié avec succès');
      } else {
        await api.post('/livres/', dataToSend);
        alert('Livre ajouté avec succès');
      }
      resetForm();
      chargerLivres();
    } catch (error) {
      console.error('Erreur:', error);
      alert('Erreur lors de la sauvegarde: ' + (error.response?.data?.error || error.message));
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Êtes-vous sûr de vouloir supprimer ce livre ?')) {
      try {
        await api.delete(`/livres/${id}/`);
        alert('Livre supprimé avec succès');
        chargerLivres();
      } catch (error) {
        console.error('Erreur:', error);
        alert('Erreur lors de la suppression');
      }
    }
  };

  const handleEmprunter = async (id) => {
    const nom = prompt('Entrez votre nom :');
    if (nom) {
      try {
        await api.post(`/livres/${id}/emprunter/`, { utilisateur_nom: nom });
        alert('Livre emprunté avec succès');
        chargerLivres();
      } catch (error) {
        alert('Ce livre n\'est pas disponible');
      }
    }
  };

  const handleEdit = (livre) => {
    setEditingLivre(livre);
    setFormData({
      titre: livre.titre,
      auteur: livre.auteur,
      categorie: livre.categorie || '',
      annee_publication: livre.annee_publication,
      quantite_totale: livre.quantite_totale,
      quantite_disponible: livre.quantite_disponible
    });
    setShowForm(true);
  };

  const resetForm = () => {
    setShowForm(false);
    setEditingLivre(null);
    setFormData({
      titre: '',
      auteur: '',
      categorie: '',
      annee_publication: new Date().getFullYear(),
      quantite_totale: 1,
      quantite_disponible: 1
    });
  };

  const handleResetSearch = () => {
    setSearchTerm('');
    setLivresFiltres(livres);
  };

  return (
    <div className="gestion-livres">
      <div className="header-actions">
        <h1>📚 Gestion des Livres</h1>
        <button className="btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Annuler' : '+ Ajouter un livre'}
        </button>
      </div>

      {/* Barre de recherche */}
      <div className="search-bar">
        <h3>🔍 Rechercher un livre</h3>
        <div className="search-container">
          <select 
            value={searchType} 
            onChange={(e) => setSearchType(e.target.value)}
            className="search-select"
          >
            <option value="titre">Par Titre</option>
            <option value="auteur">Par Auteur</option>
            <option value="id">Par ID</option>
          </select>
          <input
            type="text"
            placeholder={`Rechercher par ${searchType === 'titre' ? 'titre' : searchType === 'auteur' ? 'auteur' : 'ID'}...`}
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
          <button onClick={handleResetSearch} className="btn-secondary">
            Réinitialiser
          </button>
        </div>
        {searchTerm && (
          <p className="search-result">
            {livresFiltres.length} livre(s) trouvé(s)
          </p>
        )}
      </div>

      {/* Formulaire d'ajout/modification */}
      {showForm && (
        <form onSubmit={handleSubmit} className="form-livre">
          <h3>{editingLivre ? 'Modifier le livre' : 'Ajouter un nouveau livre'}</h3>
          
          <div className="form-row">
            <div className="form-group">
              <label>Titre *</label>
              <input
                type="text"
                value={formData.titre}
                onChange={(e) => setFormData({...formData, titre: e.target.value})}
                required
              />
            </div>
            
            <div className="form-group">
              <label>Auteur *</label>
              <input
                type="text"
                value={formData.auteur}
                onChange={(e) => setFormData({...formData, auteur: e.target.value})}
                required
              />
            </div>
          </div>
          
          <div className="form-row">
            <div className="form-group">
              <label>Catégorie</label>
              <select
                value={formData.categorie}
                onChange={(e) => setFormData({...formData, categorie: e.target.value})}
              >
                <option value="">-- Sélectionner une catégorie --</option>
                {categories.map(cat => (
                  <option key={cat.id} value={cat.id}>{cat.nom}</option>
                ))}
              </select>
            </div>
            
            <div className="form-group">
              <label>Année de parution</label>
              <input
                type="number"
                value={formData.annee_publication}
                onChange={(e) => setFormData({...formData, annee_publication: parseInt(e.target.value)})}
                min="1450"
                max={new Date().getFullYear()}
              />
            </div>
          </div>
          
          <div className="form-row">
            <div className="form-group">
              <label>Quantité totale</label>
              <input
                type="number"
                value={formData.quantite_totale}
                onChange={(e) => {
                  const newTotal = parseInt(e.target.value);
                  setFormData({
                    ...formData, 
                    quantite_totale: newTotal,
                    quantite_disponible: Math.min(formData.quantite_disponible, newTotal)
                  });
                }}
                min="1"
              />
            </div>
            
            <div className="form-group">
              <label>Quantité disponible</label>
              <input
                type="number"
                value={formData.quantite_disponible}
                onChange={(e) => {
                  const value = parseInt(e.target.value);
                  if (value <= formData.quantite_totale) {
                    setFormData({...formData, quantite_disponible: value});
                  } else {
                    alert('La quantité disponible ne peut pas dépasser la quantité totale');
                  }
                }}
                min="0"
                max={formData.quantite_totale}
              />
            </div>
          </div>
          
          <div className="form-actions">
            <button type="submit" className="btn-primary">
              {editingLivre ? 'Mettre à jour' : 'Ajouter'}
            </button>
            <button type="button" className="btn-secondary" onClick={resetForm}>
              Annuler
            </button>
          </div>
        </form>
      )}

      {/* Liste des livres */}
      {livresFiltres.length === 0 ? (
        <div className="empty-state">
          <p>📭 {searchTerm ? 'Aucun livre ne correspond à votre recherche.' : 'Aucun livre dans la bibliothèque.'}</p>
          {searchTerm && <button onClick={handleResetSearch} className="btn-secondary">Voir tous les livres</button>}
        </div>
      ) : (
        <div className="table-container">
          <div className="table-header">
            <h3>📖 Liste des livres ({livresFiltres.length})</h3>
          </div>
          <table className="livres-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Titre</th>
                <th>Auteur</th>
                <th>Catégorie</th>
                <th>Année de parution</th>
                <th>Quantité disponible</th>
                <th>Statut</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {livresFiltres.map((livre) => (
                <tr key={livre.id_livre}>
                  <td>{livre.id_livre}</td>
                  <td><strong>{livre.titre}</strong></td>
                  <td>{livre.auteur}</td>
                  <td>{livre.categorie_nom || '-'}</td>
                  <td>{livre.annee_publication || '-'}</td>
                  <td style={{ color: livre.quantite_disponible > 0 ? '#28a745' : '#dc3545', fontWeight: 'bold' }}>
                    {livre.quantite_disponible}
                  </td>
                  <td>
                    <span className={`statut ${livre.statut}`}>
                      {livre.statut === 'disponible' ? '✅ Disponible' : 
                       livre.statut === 'emprunte' ? '📖 Emprunté' : '🔴 Indisponible'}
                    </span>
                  </td>
                  <td className="actions-cell">
                    <button 
                      className="btn-success" 
                      onClick={() => handleEmprunter(livre.id_livre)}
                      disabled={livre.quantite_disponible === 0}
                      title={livre.quantite_disponible === 0 ? 'Non disponible' : 'Emprunter'}
                    >
                      Emprunter
                    </button>
                    <button className="btn-secondary" onClick={() => handleEdit(livre)}>
                      Modifier
                    </button>
                    <button className="btn-danger" onClick={() => handleDelete(livre.id_livre)}>
                      Supprimer
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default GestionLivres;