from django import template
register = template.Library()

import requests

@register.filter
def ip_location(value):
    url = 'http://ip-api.com/json/{}'.format(value)
    response = requests.get(url)
    data = response.json()
    if data['status'] == 'success':
        city_region_country = data['city'] + ', ' + data['regionName'] + ', ' + data['country']
    elif data['status'] == 'fail':
        if data['query'] == '127.0.0.1':
            city_region_country = 'Localhost'
        else:
            city_region_country = 'Unknown'
    return city_region_country