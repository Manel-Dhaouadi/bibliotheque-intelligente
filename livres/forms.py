from django import forms
from .models import Livre, Categorie

class LivreForm(forms.ModelForm):
    class Meta:
        model = Livre
        fields = ['titre', 'auteur', 'categorie', 'annee_publication', 'quantite_totale', 'quantite_disponible']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre du livre'}),
            'auteur': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de l\'auteur'}),
            'categorie': forms.Select(attrs={'class': 'form-control'}),
            'annee_publication': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Année'}),
            'quantite_totale': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'quantite_disponible': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        quantite_totale = cleaned_data.get('quantite_totale', 0)
        quantite_disponible = cleaned_data.get('quantite_disponible', 0)
        if quantite_disponible > quantite_totale:
            raise forms.ValidationError("La quantité disponible ne peut pas dépasser la quantité totale")
        return cleaned_data

class CategorieForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = ['nom', 'description']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de la catégorie'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description (optionnel)'}),
        }