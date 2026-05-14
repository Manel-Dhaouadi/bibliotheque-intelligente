from django.db import models
from django.contrib.auth.models import AbstractUser

class Utilisateur(AbstractUser):
    """Modèle utilisateur personnalisé avec rôles"""
    
    ROLE_CHOICES = [
        ('admin', 'Administrateur'),
        ('client', 'Client'),
    ]
    
    email = models.EmailField(unique=True, verbose_name="Email")
    telephone = models.CharField(max_length=20, blank=True, null=True)
    adresse = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')
    date_inscription = models.DateTimeField(auto_now_add=True)
    est_actif = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ['-date_inscription']
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def est_admin(self):
        return self.role == 'admin'
    
    @property
    def est_client(self):
        return self.role == 'client'

class Profile(models.Model):
    """Profil utilisateur étendu"""
    
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    date_naissance = models.DateField(null=True, blank=True)
    preferences = models.JSONField(default=dict, blank=True)
    
    def __str__(self):
        return f"Profil de {self.utilisateur.username}"