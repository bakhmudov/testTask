from django.urls import path
from .views import draw_menu

app_name = 'menu'

urlpatterns = [
    path('<str:menu_name>/', draw_menu, name='draw_menu'),
]
