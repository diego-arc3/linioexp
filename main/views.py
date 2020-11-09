from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, FormView, TemplateView, View, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.db.models import F
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib import messages

from random import randint

from .models import *
from .forms import *



# Create your views here.

class HomePageView(TemplateView):

    template_name = "main/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_products'] = Producto.objects.all()[:5]

        return context


class ProductListView(ListView):
    model = Producto
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query is not None:
            object_list = Producto.objects.filter(nombre__icontains=query)
            return object_list
        else:
            return Producto.objects.all()
 
    
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
    
    
class AddToCartView(LoginRequiredMixin, View):
    def get(self, request, product_pk):
        # Obten el cliente
        user_profile = Profile.objects.get(user=request.user)
        cliente = Cliente.objects.get(user_profile=user_profile)
        
        # Obtén el producto que queremos añadir al carrito
        producto = Producto.objects.get(pk=product_pk)
        
        # Obtén/Crea un/el pedido en proceso (EP) del usuario
        pedido, _  = Pedido.objects.get_or_create(cliente=cliente, estado='EP')
        
        # Obtén/Crea un/el detalle de pedido
        detalle_pedido, created = DetallePedido.objects.get_or_create(
            producto=producto,
            pedido=pedido,
        )

        # Si el detalle de pedido es creado la cantidad es 1
        # Si no sumamos 1 a la cantidad actual
        if created:
            detalle_pedido.cantidad = 1
        else:
            detalle_pedido.cantidad = F('cantidad') + 1
        # Guardamos los cambios
        detalle_pedido.save()
        # Recarga la página
        return redirect(request.META['HTTP_REFERER'])


class RemoveFromCartView(View):
    def get(self, request, product_pk):
        # Obten el cliente
        user_profile = Profile.objects.get(user=request.user)
        cliente = Cliente.objects.get(user_profile=user_profile)
        # Obtén el producto que queremos añadir al carrito
        producto = Producto.objects.get(pk=product_pk)
        # Obtén el pedido en proceso (EP) del usuario
        pedido  = Pedido.objects.get(cliente=cliente, estado='EP')
        # Obtén/Crea un/el detalle de pedido
        detalle_pedido = DetallePedido.objects.get(
            producto=producto,
            pedido=pedido,
        )
        # Si la cantidad actual menos 1 es 0 elmina el producto del carrito
        # Si no restamos 1 a la cantidad actual
        if detalle_pedido.cantidad - 1 == 0:
            detalle_pedido.delete()
        else:
            detalle_pedido.cantidad = F('cantidad') - 1
            # Guardamos los cambios
            detalle_pedido.save()
        # Recarga la página
        return redirect(request.META['HTTP_REFERER'])


class PedidoDetailView(LoginRequiredMixin, DetailView):
    model = Pedido

    def get_object(self):
        # Obten el cliente
        user_profile = Profile.objects.get(user=self.request.user)
        cliente = Cliente.objects.get(user_profile=user_profile)
        # Obtén/Crea un/el pedido en proceso (EP) del usuario
        pedido = Pedido.objects.get(cliente=cliente, estado='EP')
        return pedido
 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detalles'] = context['object'].detallepedido_set.all()
        return context
    


class PedidoUpdateView(UpdateView):
    model = Pedido
    fields = ['ubicacion', 'direccion_entrega']
    success_url = reverse_lazy('payment')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        self.object = form.save(commit=False)
        # Calculo de tarifa
        self.object.tarifa = randint(5, 20)
        return super().form_valid(form)
    
    
class PaymentView(TemplateView):
    
    template_name = "main/payment.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obten el cliente
        user_profile = Profile.objects.get(user=self.request.user)
        cliente = Cliente.objects.get(user_profile=user_profile)
        
        # Obten el pedido
        context['pedido'] = Pedido.objects.get(cliente=cliente, estado='EP')

        return context
    
    
class CompletePaymentView(View):
    def get(self, request):
        # Obten el cliente
        user_profile = Profile.objects.get(user=request.user)
        cliente = Cliente.objects.get(user_profile=user_profile)
        # Obtén/Crea un/el pedido en proceso (EP) del usuario
        pedido = Pedido.objects.get(cliente=cliente, estado='EP')
        # Cambia el estado del pedido
        pedido.estado = 'PAG'
        # Asignacion de repartidor
        pedido.repartidor = Colaborador.objects.order_by('?').first()
        # Guardamos los cambios
        pedido.save()
        messages.success(request, 'Gracias por tu compra! Un repartidor ha sido asignado a tu pedido.')
        return redirect('home')


