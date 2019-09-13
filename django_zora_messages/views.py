# from django.shortcuts import render
from .utils import get_message as msg
from django.http import HttpResponse
# Create your views here.


def index(request):
    welcome_message = msg("welcome.msg")
    under_construction = msg("site.under.construction")
    html = f"""
        <html>
        <body>
        <h1>{welcome_message.value}</h1>
        <h3>{under_construction.value}</h3>
        </body>

        </html>
    """
    return HttpResponse(html)