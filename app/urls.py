from django.urls import path
from . import views

urlpatterns = [
    path("", views.main, name='home'),
    path("png/", views.pngView, name='png'),
    path("pdf/", views.pdfView, name='pdf'),
]
