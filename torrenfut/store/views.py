from django.http import HttpResponse
from django.template import loader
from .models import Camiseta


def store(request):
  camisetas = Camiseta.objects.all()
  template = loader.get_template('index.html')
  context = {
    'camisetas': camisetas,
  }
  return HttpResponse(template.render(context, request))

  