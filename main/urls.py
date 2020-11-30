from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('productos', views.ProductListView.as_view(), name='product-list'),
    path('productos/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('registro/', views.RegistrationView.as_view(), name='register'),
    path('registro-cliente/', views.ClienteRegistrationView.as_view(), name='register-cliente'),
    path('registro-colaborador/', views.ColaboradorRegistrationView.as_view(), name='register-colaborador'),
    
    path('pedidos_cliente/', views.PedidosClienteView.as_view(), name='pedidos-cliente'),
    path('cancelar_pedido/<int:pedido_pk>', views.CancelarPedidoView.as_view(), name='cancelar-pedido'),
    
    path('estado_en_tienda/<int:pedido_pk>', views.EstadoEnTiendaView.as_view(), name='estado-en-tienda'),
    path('estado_en_camino/<int:pedido_pk>', views.EstadoEnCaminoView.as_view(), name='estado-en-camino'),
    path('estado_entregado/<int:pedido_pk>', views.EstadoEntregadoView.as_view(), name='estado-entregado'),
    
    path('add_to_cart/<int:product_pk>', views.AddToCartView.as_view(), name='add-to-cart'),
    path('remove_from_cart/<int:product_pk>', views.RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('carrito/', views.PedidoDetailView.as_view(), name='pedido-detail'),
    path('checkout/<int:pk>', views.PedidoUpdateView.as_view(), name='pedido-update'),
    path('payment/', views.PaymentView.as_view(), name='payment'),
    path('complete_payment/', views.CompletePaymentView.as_view(), name='complete-payment'),
    path('pedidos/', views.PedidosColaboradorView.as_view(), name='pedidos-list')
]