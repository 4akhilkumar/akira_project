import re
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.encoding import force_str
from .helpers import verify_recaptcha

_POST_FORM_RE = re.compile(
    r'(<form\W[^>]*\bmethod\s*=\s*(\'|"|)POST(\'|"|)\b[^>]*>)', re.IGNORECASE
)
_HTML_TYPES = ("text/html", "application/xhtml+xml")


class BaseRecapthaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)


class RecaptchaRequestMiddleware(BaseRecapthaMiddleware):
    def process_view(self, request, callback, callback_args, callback_kwargs):
        if request.is_ajax():
            return None

        return verify_recaptcha(request)


class RecaptchaResponseMiddleware(BaseRecapthaMiddleware):

    def __call__(self, request):
        response = self.get_response(request)

        try:
            content_type = response["Content-Type"].split(";")[0]
        except (KeyError, AttributeError):
            content_type = None

        if content_type in _HTML_TYPES and request.path != "/":

            def add_recaptcha_field(match):
                return mark_safe(
                    match.group()
                    + render_to_string(
                        "G_Recaptcha/RecaptchaV3.html",
                        {'recaptcha_site_key': settings.RECAPTCHA_PUBLIC_KEY},
                    )
                )

            response.content = _POST_FORM_RE.sub(
                add_recaptcha_field, force_str(response.content)
            )

        return response

class RecaptchaMiddleware(RecaptchaRequestMiddleware, RecaptchaResponseMiddleware):
    pass