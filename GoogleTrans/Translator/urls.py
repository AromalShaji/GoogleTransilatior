from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', login, name='login'),
    path('home', home, name='home'),
    path('translate_text', translate_text, name='translate_text'),
    path('register', register, name='register'),
    path('logout', logout, name='logout'),
    path('history', history, name='history'),
    path('feedback', feedback, name='feedback'),
    path('history_delete/<id>', history_delete, name='history_delete'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)