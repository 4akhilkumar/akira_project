from django import template
register = template.Library()

import requests

@register.filter
def ip_location(value):
    try:
        url = 'https://ipinfo.io/{}/geo'.format(value)
        response = requests.get(url)
        data = response.json()
        if data['bogon'] == True:
            if data['ip'] == '127.0.0.1':
                city_region_country = 'Localhost'
            else:
                city_region_country = 'Unknown'
        else:
            city_region_country = data['city'] + ', ' + data['region'] + ', ' + data['country']
        return city_region_country
    except Exception as e:
        return value