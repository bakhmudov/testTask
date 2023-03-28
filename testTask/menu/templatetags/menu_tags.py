from django import template
from django.urls import reverse

from ..models import MenuItem

register = template.Library()


def is_active(menu_item, path):
    return path.startwith(menu_item.url) or path == reverse(menu_item.url_name)


def draw_menu(parser, token):
    try:
        tag_name, menu_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(f"{token.contents} tag requires a single argument")
    return MenuNode(menu_name)


class MenuNode(template.Node):
    def __int__(self, menu_name):
        self.menu_name = template.Variable(menu_name)

    def render(self, context):
        menu_name = self.menu_name.resolve(context)
        menu_items = MenuItem.objects.filter(menu_name=menu_name).prefetch_related('children')

        request = context.get('request')
        path = request.path if request else ''

        menu_html = ''
        for item in menu_items:
            if not item.parent:
                menu_html += f'<li class="nav-item {"active" if is_active(item, path) else ""}">'
                if item.children.exists():
                    menu_html += f'<a href="#" class="nav-link dropdown-toggle" data-toggle="dropdown">{item.title}</a>'
                    menu_html += '<ul class="dropdown-menu">'
                    for child in item.children.all():
                        menu_html += f'<li class="nav-item {"active" if is_active(child, path) else ""}">'
                        menu_html += f'<a href="{child.url or reverse(child.url_name)}" class="nav-link">{child.title}</a>'
                        menu_html += '</li>'
                        menu_html += '</ul>'
                else:
                    menu_html += f'<a href="{item.url or reverse(item.url_name)}" class="nav-link">{item.title}</a>'
                menu_html += '</li>'

        return menu_html
