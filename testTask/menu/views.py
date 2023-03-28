from django.shortcuts import render
from django.urls import reverse

from .models import MenuItem


def is_active(menu_item, path):
    if path == menu_item.url:
        return True
    elif menu_item.url_name:
        try:
            url = reverse(menu_item.url_name)
            return path.startwith(url)
        except:
            return False
    else:
        return False


def draw_menu(request, menu_name):
    menu_items = MenuItem.objects.filter(parent__isnull=True).select_related('children')
    current_path = request.path_info
    for menu_item in menu_items:
        menu_item.active = is_active(menu_item, current_path)
        for child in menu_item.children.all():
            child.active = is_active(child, current_path)
    return render(request, 'menu/draw_menu.html', {'menu_items': menu_items, 'menu_name': menu_name})
