from django import template
register = template.Library()

import requests

@register.filter
def ip_location(value):
    try:
        url = 'https://ipinfo.io/{}/geo'.format(value)
        response = requests.get(url)
        data = response.json()
        try:
            city_region_country = data['city'] + ', ' + data['region'] + ', ' + data['country']
        except Exception:
            city_region_country = 'Unknown'
        return city_region_country
    except Exception:
        return value