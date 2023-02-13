from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings
from .models import Team
from django.http import HttpResponse
from functools import wraps
import requests

def admin_required(function):
  def wrap(request, *args, **kwargs):
      if request.user.is_superuser == True:
        return function(request, *args, **kwargs)
      else:  
        messages.info(request, "접근 권한이 없습니다.")
        return redirect('/users/main/')
  
  return wrap



def check_recaptcha(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        request.recaptcha_is_valid = None
        if request.method == 'POST':
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            if result['success']:
                request.recaptcha_is_valid = True
            else:
                request.recaptcha_is_valid = False
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')
        return view_func(request, *args, **kwargs)
    return _wrapped_view