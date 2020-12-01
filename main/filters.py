import django_filters
from .models import Producto

class ProductoFilter(django_filters.FilterSet):
    
    CHOICES = (
        ('ascendente', 'Mayor precio'),
        ('descendente', 'Menor precio')
    )
    
    ordering = django_filters.ChoiceFilter(label='Ordering', choices=CHOICES, method='filter_by_order')
    
    class Meta:
        model = Producto
        fields = {
            'nombre':['icontains'],
            'pk':['iexact'], 
            'precio':['lt', 'gt']}
        
    def filter_by_order(self, queryset, name, value):
        expresion = 'precio' if value == 'ascendente' else '-precio'
        return queryset.order_by(expression)
    