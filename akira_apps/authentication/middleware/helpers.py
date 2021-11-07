import requests
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.template.loader import render_to_string

def verify_recaptcha(request):
    if request.method == "POST" and request.path != "/":
        recaptcha_response = request.POST.get('g-recaptcha-response')
        data = {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': recaptcha_response
        }
        r = requests.post(
            'https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()

        print(result)
        if result['success'] and \
                float(result['score']) > settings.RECAPTCHA_REQUIRED_SCORE:
            return None

        respond = render_to_string(
            'G_Recaptcha/ReCaptcha_error.html',
            {}
        )
        return HttpResponseBadRequest(respond)