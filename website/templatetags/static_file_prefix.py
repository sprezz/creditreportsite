from django import template


register = template.Library()


@register.simple_tag
def fileurl_prefix(country, landing_page):
    """
    >>> fileurl_prefix('US', 'lp2')
    '/lps/us/lp2'
    """
    return u'/lps/{}/{}'.format(country.lower(), landing_page.lower())
