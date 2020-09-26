from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, FormView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth import login
from .models import *
from .forms import *

def home(request):
    return HttpResponse("Hola Mundo. Te encuentras en la página de inicio de Linio Express")


# Create your views here.

class HomePageView(TemplateView):

    template_name = "main/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_products'] = Producto.objects.all()[:5]

        return context

class ProductListView(ListView):
    model = Producto
    
class ProductDetailView(DetailView):
    model = Producto
    
class RegistrationView(FormView):
    template_name = 'registration/register.html'
    form_class = UserForm
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        # This methos is called when valid from data has been POSTed
        # It should return an HttpResponse

        # Create User
        username = form.cleaned_data['username']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password1']

        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
        user.save()
        
        # Create Profile
        documento_identidad = form.cleaned_data['documento_identidad']
        fecha_nacimiento = form.cleaned_data['fecha_nacimiento']
        estado = form.cleaned_data['estado']
        genero = form.cleaned_data['genero']

        user_profile = Profile.objects.create( user=user, documento_identidad=documento_identidad, fecha_nacimiento=fecha_nacimiento, estado=estado, genero=genero)
        user_profile.save()
        
        # Create Cliente if needed
        is_cliente = form.cleaned_data['is_cliente']
        if is_cliente:
            cliente = Cliente.objects.create(user_profile=user_profile)

            # Handle special attribute
            preferencias = form.cleaned_data['preferencias']
            preferencias_set = Categoria.objects.filter(pk=preferencias.pk)
            cliente.preferencias.set(preferencias_set)

            cliente.save()
        
        # Create Colaborador if needed
        is_colaborador = form.cleaned_data['is_colaborador']
        if is_colaborador:
            reputacion = form.cleaned_data['reputacion']
            colaborador = Colaborador.objects.create(user_profile=user_profile, reputacion=reputacion)

            # Handle special attribute
            cobertura_entrega = form.cleaned_data['cobertura_entrega']
            cobertura_entrega_set = Localizacion.objects.filter(pk=cobertura_entrega.pk)
            colaborador.cobertura_entrega.set(cobertura_entrega_set)

            colaborador.save()
        
        # Login the user
        login(self.request, user)

        return super().form_valid(form)