from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("busca/", views.busca, name="busca"),
    path("categorias/<int:categoria_id>/", views.categoria, name="categoria"),
    path("artigos/<int:artigo_id>/", views.artigo, name="artigo"),
]
