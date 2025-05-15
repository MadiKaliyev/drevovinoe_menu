from django import template
from main.models import Menu_ithems
from django.utils.safestring import mark_safe
from django.urls import reverse, NoReverseMatch

register = template.Library()

@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    tekushiy_url = context['request'].path
    vse_punkty = Menu_ithems.objects.filter(menu_name=menu_name).select_related('roditel')

    # ключ — id 
    derevo = {}

    # Преобразуем в словарь
    for punkt in vse_punkty:
        derevo[punkt.id] = {
            'punkt': punkt,
            'deti': [],
            'aktivnyy': tekushiy_url.startswith(punkt.url),
            'pokazat': False  # будем использовать для фильтрации
        }

    # Собираем дерево
    kornevye_punkty = []
    for uzel in derevo.values():
        punkt = uzel['punkt']
        if punkt.roditel:
            roditel = derevo.get(punkt.roditel.id)
            if roditel:
                roditel['deti'].append(uzel)
        else:
            kornevye_punkty.append(uzel)

    # Определим активный элемент и его родителей
    aktivnaya_tsep = []

    def naiti_aktivnyy_put():
        for uzel in derevo.values():
            if uzel['aktivnyy']:
                tekushiy = uzel['punkt']
                while tekushiy:
                    aktivnaya_tsep.append(tekushiy.id)
                    tekushiy = tekushiy.roditel
                break

    naiti_aktivnyy_put()

    # Отмечаем какие узлы показывать
    def otmetit_vidimye():
        def pokazat_vse_potomki(uzel):
            uzel['pokazat'] = True
            for rebenok in uzel['deti']:
                pokazat_vse_potomki(rebenok)

        for punkt_id in aktivnaya_tsep:
            uzel = derevo.get(punkt_id)
            if uzel:
                pokazat_vse_potomki(uzel)

    otmetit_vidimye()

    # создаем HTML из дерева
    def postroit_html(uzel):
        punkt = uzel['punkt']
        try:
            url = reverse(punkt.url)
        except NoReverseMatch:
            url = punkt.url

        klass = "active" if uzel['aktivnyy'] else ""
        html = f"<li class='{klass}' data-id='{punkt.id}'>" \
            f"<a href='#' onclick='toggleMenu(event, {punkt.id})'>{punkt.name}</a>"

        vidimye_deti = uzel['deti']  
        if vidimye_deti:
            html += f"<ul id='menu-{punkt.id}' style='display: none;'>"
            for rebenok in vidimye_deti:
                html += postroit_html(rebenok)
            html += "</ul>"

        html += "</li>"
        return html
    
    itog_html = "<ul>"
    for koren in kornevye_punkty:
        itog_html += postroit_html(koren)  
    itog_html += "</ul>"


    return mark_safe(itog_html)
