import React, { useState, useEffect } from 'react';
import api from '../services/api';

function GestionCategories() {
  const [categories, setCategories] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [editingCategorie, setEditingCategorie] = useState(null);
  const [formData, setFormData] = useState({
    nom: '',
    description: ''
  });

  useEffect(() => {
    chargerCategories();
  }, []);

  const chargerCategories = async () => {
    try {
      const response = await api.get('/categories/');
      setCategories(response.data.results || response.data);
    } catch (error) {
      console.error('Erreur:', error);
      alert('Erreur lors du chargement des catégories');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.nom) {
      alert('Veuillez saisir un nom de catégorie');
      return;
    }

    try {
      if (editingCategorie) {
        await api.put(`/categories/${editingCategorie.id}/`, formData);
        alert('Catégorie modifiée avec succès');
      } else {
        await api.post('/categories/', formData);
        alert('Catégorie ajoutée avec succès');
      }
      resetForm();
      chargerCategories();
    } catch (error) {
      console.error('Erreur:', error);
      alert('Erreur lors de la sauvegarde: ' + (error.response?.data?.error || error.message));
    }
  };

  const handleDelete = async (id) => {
    // Vérifier si la catégorie contient des livres
    try {
      const livresResponse = await api.get('/livres/');
      const livresCategorie = livresResponse.data.filter(l => l.categorie === id);
      
      if (livresCategorie.length > 0) {
        alert(`Impossible de supprimer cette catégorie car elle contient ${livresCategorie.length} livre(s).`);
        return;
      }
      
      if (window.confirm('Êtes-vous sûr de vouloir supprimer cette catégorie ?')) {
        await api.delete(`/categories/${id}/`);
        alert('Catégorie supprimée avec succès');
        chargerCategories();
      }
    } catch (error) {
      console.error('Erreur:', error);
      alert('Erreur lors de la suppression');
    }
  };

  const handleEdit = (categorie) => {
    setEditingCategorie(categorie);
    setFormData({
      nom: categorie.nom,
      description: categorie.description || ''
    });
    setShowForm(true);
  };

  const resetForm = () => {
    setShowForm(false);
    setEditingCategorie(null);
    setFormData({
      nom: '',
      description: ''
    });
  };

  return (
    <div className="gestion-livres">
      <div className="header-actions">
        <h1>🏷️ Gestion des Catégories</h1>
        <button className="btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Annuler' : '+ Ajouter une catégorie'}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleSubmit} className="form-livre">
          <h3>{editingCategorie ? 'Modifier la catégorie' : 'Ajouter une nouvelle catégorie'}</h3>
          
          <div className="form-group">
            <label>Nom de la catégorie *</label>
            <input
              type="text"
              value={formData.nom}
              onChange={(e) => setFormData({...formData, nom: e.target.value})}
              placeholder="Ex: Roman, Science, Histoire..."
              required
            />
          </div>
          
          <div className="form-group">
            <label>Description (optionnel)</label>
            <textarea
              value={formData.description}
              onChange={(e) => setFormData({...formData, description: e.target.value})}
              placeholder="Description de la catégorie..."
              rows="3"
              style={{width: '100%', padding: '0.8rem', borderRadius: '8px', border: '1px solid #ddd'}}
            />
          </div>
          
          <div className="form-actions">
            <button type="submit" className="btn-primary">
              {editingCategorie ? 'Mettre à jour' : 'Ajouter'}
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
            <th>Nom</th>
            <th>Description</th>
            <th>Nombre de livres</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {categories.length === 0 ? (
            <tr>
              <td colSpan="5" style={{textAlign: 'center'}}>
                Aucune catégorie. Cliquez sur "+ Ajouter une catégorie" pour commencer !
              </td>
            </tr>
          ) : (
            categories.map((categorie) => (
              <tr key={categorie.id}>
                <td>{categorie.id}</td>
                <td><strong>{categorie.nom}</strong></td>
                <td>{categorie.description || '-'}</td>
                <td>{categorie.nombre_livres || 0}</td>
                <td>
                  <button className="btn-secondary" onClick={() => handleEdit(categorie)}>
                    ✏️ Modifier
                  </button>
                  <button className="btn-danger" onClick={() => handleDelete(categorie.id)}>
                    🗑️ Supprimer
                  </button>
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
      
      <div style={{marginTop: '2rem', padding: '1rem', background: '#e7f3ff', borderRadius: '10px'}}>
        <h4>💡 Astuce :</h4>
        <p>Les catégories aident à organiser vos livres. Vous ne pouvez pas supprimer une catégorie qui contient des livres.</p>
      </div>
    </div>
  );
}

export default GestionCategories;