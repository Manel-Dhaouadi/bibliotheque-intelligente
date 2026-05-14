from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Utilisateur, Profile

class UtilisateurSerializer(serializers.ModelSerializer):
    """Sérializer pour l'utilisateur"""
    
    class Meta:
        model = Utilisateur
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                  'telephone', 'adresse', 'role', 'date_inscription', 'est_actif']
        read_only_fields = ['id', 'date_inscription']

class RegisterSerializer(serializers.ModelSerializer):
    """Sérializer pour l'inscription"""
    
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = Utilisateur
        fields = ['username', 'email', 'password', 'password_confirm', 
                  'first_name', 'last_name', 'telephone']
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas")
        if Utilisateur.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Cet email est déjà utilisé")
        if Utilisateur.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Ce nom d'utilisateur est déjà pris")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = Utilisateur.objects.create_user(**validated_data)
        Profile.objects.create(utilisateur=user)
        return user

class LoginSerializer(serializers.Serializer):
    """Sérializer pour la connexion avec email"""
    
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            raise serializers.ValidationError("Veuillez fournir email et mot de passe")
        
        try:
            user = Utilisateur.objects.get(email=email)
        except Utilisateur.DoesNotExist:
            raise serializers.ValidationError("Email ou mot de passe incorrect")
        
        user = authenticate(username=user.username, password=password)
        
        if not user:
            raise serializers.ValidationError("Email ou mot de passe incorrect")
        
        if not user.est_actif:
            raise serializers.ValidationError("Votre compte est désactivé")
        
        return user

class ProfileSerializer(serializers.ModelSerializer):
    """Sérializer pour le profil"""
    
    class Meta:
        model = Profile
        fields = ['avatar', 'date_naissance', 'preferences']