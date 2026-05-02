import React, { useState, useEffect } from 'react';
import api from '../services/api';

function GestionLivres() {
  const [livres, setLivres] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [editingLivre, setEditingLivre] = useState(null);
  const [formData, setFormData] = useState({
    titre: '',
    auteur: '',
    annee_publication: new Date().getFullYear(),
    quantite_totale: 1,
    quantite_disponible: 1
  });

  useEffect(() => {
    chargerLivres();
  }, []);

  const chargerLivres = async () => {
    try {
      const response = await api.get('/livres/');
      setLivres(response.data);
    } catch (error) {
      console.error('Erreur:', error);
      alert('Erreur lors du chargement des livres');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingLivre) {
        await api.put(`/livres/${editingLivre.id_livre}/`, formData);
        alert('Livre modifié avec succès');
      } else {
        await api.post('/livres/', formData);
        alert('Livre ajouté avec succès');
      }
      resetForm();
      chargerLivres();
    } catch (error) {
      console.error('Erreur:', error);
      alert('Erreur lors de la sauvegarde');
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
      annee_publication: new Date().getFullYear(),
      quantite_totale: 1,
      quantite_disponible: 1
    });
  };

  return (
    <div className="gestion-livres">
      <div className="header-actions">
        <h1>📚 Gestion des Livres</h1>
        <button className="btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Annuler' : '+ Ajouter un livre'}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleSubmit} className="form-livre">
          <h3>{editingLivre ? 'Modifier le livre' : 'Ajouter un nouveau livre'}</h3>
          
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
          
          <div className="form-group">
            <label>Année de publication</label>
            <input
              type="number"
              value={formData.annee_publication}
              onChange={(e) => setFormData({...formData, annee_publication: parseInt(e.target.value)})}
            />
          </div>
          
          <div className="form-group">
            <label>Quantité totale</label>
            <input
              type="number"
              value={formData.quantite_totale}
              onChange={(e) => setFormData({...formData, quantite_totale: parseInt(e.target.value)})}
              min="1"
            />
          </div>
          
          <div className="form-group">
            <label>Quantité disponible</label>
            <input
              type="number"
              value={formData.quantite_disponible}
              onChange={(e) => setFormData({...formData, quantite_disponible: parseInt(e.target.value)})}
              min="0"
            />
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

      <table className="livres-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Titre</th>
            <th>Auteur</th>
            <th>Année</th>
            <th>Disponible</th>
            <th>Total</th>
            <th>Statut</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {livres.map((livre) => (
            <tr key={livre.id_livre}>
              <td>{livre.id_livre}</td>
              <td>{livre.titre}</td>
              <td>{livre.auteur}</td>
              <td>{livre.annee_publication}</td>
              <td>{livre.quantite_disponible}</td>
              <td>{livre.quantite_totale}</td>
              <td>
                <span className={`statut ${livre.statut}`}>
                  {livre.statut}
                </span>
              </td>
              <td>
                <button className="btn-success" onClick={() => handleEmprunter(livre.id_livre)}>
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
  );
}

export default GestionLivres;