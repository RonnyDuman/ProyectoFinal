import json
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.db.models import ProtectedError
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseNotAllowed, JsonResponse
from django.views.decorators.http import require_http_methods
from Aplicaciones.categorias.models import Categoria

# Create your views here.
@csrf_exempt 
def categoria_list_create(request):
    if request.method == 'GET':
        categorias = list(Categoria.objects.values('id', 'nombre'))
        return JsonResponse(categorias, safe=False)
