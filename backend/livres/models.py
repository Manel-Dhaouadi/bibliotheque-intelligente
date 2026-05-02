from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date, timedelta

class Categorie(models.Model):
    """Modèle pour les catégories de livres"""
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['nom']
    
    def __str__(self):
        return self.nom
    
    @property
    def nombre_livres(self):
        """Retourne le nombre de livres dans cette catégorie"""
        return self.livres.count()

class Livre(models.Model):
    """Modèle principal pour les livres"""
    
    STATUS_CHOICES = [
        ('disponible', 'Disponible'),
        ('emprunte', 'Emprunté'),
        ('reserve', 'Réservé'),
        ('indisponible', 'Indisponible'),
    ]
    
    id_livre = models.AutoField(primary_key=True)
    titre = models.CharField(max_length=300, verbose_name="Titre")
    auteur = models.CharField(max_length=200, verbose_name="Auteur")
    categorie = models.ForeignKey(
        Categorie, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='livres',
        verbose_name="Catégorie"
    )
    annee_publication = models.IntegerField(
        validators=[MinValueValidator(1450), MaxValueValidator(date.today().year)],
        verbose_name="Année de publication"
    )
    quantite_disponible = models.IntegerField(
        default=1,
        validators=[MinValueValidator(0)],
        verbose_name="Quantité disponible"
    )
    quantite_totale = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name="Quantité totale"
    )
    statut = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='disponible',
        verbose_name="Statut"
    )
    date_ajout = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Livre"
        verbose_name_plural = "Livres"
        ordering = ['titre']
        indexes = [
            models.Index(fields=['titre']),
            models.Index(fields=['auteur']),
            models.Index(fields=['categorie']),
        ]
    
    def __str__(self):
        return f"{self.titre} - {self.auteur}"
    
    def save(self, *args, **kwargs):
        """Override save method to automatically update status based on quantity"""
        if self.quantite_disponible <= 0:
            self.statut = 'indisponible'
        elif self.quantite_disponible < self.quantite_totale:
            self.statut = 'emprunte'
        else:
            self.statut = 'disponible'
        super().save(*args, **kwargs)
    
    @property
    def est_disponible(self):
        """Vérifie si au moins un exemplaire est disponible"""
        return self.quantite_disponible > 0
    
    @property
    def taux_disponibilite(self):
        """Calcule le taux de disponibilité"""
        if self.quantite_totale == 0:
            return 0
        return (self.quantite_disponible / self.quantite_totale) * 100
    
    def emprunter(self):
        """Méthode pour emprunter un livre"""
        if self.quantite_disponible > 0:
            self.quantite_disponible -= 1
            self.save()
            return True
        return False
    
    def retourner(self):
        """Méthode pour retourner un livre"""
        if self.quantite_disponible < self.quantite_totale:
            self.quantite_disponible += 1
            self.save()
            return True
        return False

class Emprunt(models.Model):
    """Modèle pour gérer les emprunts de livres"""
    
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE, related_name='emprunts')
    utilisateur_nom = models.CharField(max_length=150, verbose_name="Nom de l'emprunteur")
    date_emprunt = models.DateField(auto_now_add=True)
    date_retour_prevue = models.DateField()
    date_retour_reelle = models.DateField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Emprunt"
        verbose_name_plural = "Emprunts"
        ordering = ['-date_emprunt']
    
    def __str__(self):
        return f"{self.livre.titre} - {self.utilisateur_nom}"
    
    def save(self, *args, **kwargs):
        if not self.date_retour_prevue:
            self.date_retour_prevue = date.today() + timedelta(days=14)
        super().save(*args, **kwargs)
    
    @property
    def est_en_retard(self):
        """Vérifie si l'emprunt est en retard"""
        if not self.date_retour_reelle and self.date_retour_prevue < date.today():
            return True
        return False
    
    @property
    def jours_retard(self):
        """Calcule le nombre de jours de retard"""
        if self.est_en_retard:
            return (date.today() - self.date_retour_prevue).days
        return 0