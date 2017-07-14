from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def active_view(context, view_name):
    request = context['request']
    return 'active' if request.resolver_match.view_name == view_name else ''

@register.inclusion_tag('navbar_entry.html', takes_context=True)
def navbar_entry(context, view_name, entry_title, url_append=''):
    return {'request': context['request'], 'view_name': view_name, 'entry_title': entry_title, 'url_append': url_append}
