from django.urls import path
from main.views import main ,panel
urlpatterns = [
    path('', main),
    path('panel/', panel),
    
]
