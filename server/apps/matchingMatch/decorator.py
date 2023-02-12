
from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages
from .models import Team
from django.http import HttpResponse



def admin_required(function):
  def wrap(request, *args, **kwargs):
      if request.user.is_superuser == True:
        return function(request, *args, **kwargs)
      else:  
        messages.info(request, "접근 권한이 없습니다.")
        return redirect('/users/main/')
  
  return wrap