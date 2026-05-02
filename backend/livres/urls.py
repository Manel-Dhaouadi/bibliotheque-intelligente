from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LivreViewSet, CategorieViewSet, ChatbotViewSet

router = DefaultRouter()
router.register(r'livres', LivreViewSet, basename='livre')
router.register(r'categories', CategorieViewSet, basename='categorie')
router.register(r'chatbot', ChatbotViewSet, basename='chatbot')

urlpatterns = [
    path('', include(router.urls)),
]