from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from .models import *

def home(request):
    return HttpResponse("Hola Mundo. Te encuentras en la página de inicio de Linio Express")


# Create your views here.

class ProductListView(ListView):
    model = Producto
    
class ProductDetailView(DetailView):
    model = Producto