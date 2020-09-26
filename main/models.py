from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Proveedor(models.Model):
    ruc = models.CharField(max_length=11)
    razon_social = models.CharField(max_length=20)
    telefono = models.CharField(max_length=9)

class Categoria(models.Model):
    codigo = models.CharField(max_length=4)
    nombre = models.CharField(max_length=50)

class Localizacion(models.Model):
    distrito = models.CharField(max_length=20)
    provincia = models.CharField(max_length=20)
    departamento = models.CharField(max_length=20)

class Producto(models.Model):
    # Relaciones
    categoria = models.ForeignKey('Categoria', on_delete=models.SET_NULL, null=True)
    proveedor = models.ForeignKey('Proveedor', on_delete=models.SET_NULL, null=True)

    # Atributos
    nombre = models.CharField(max_length=20)
    descripcion = models.TextField()
    precio = models.FloatField()
    estado = models.CharField(max_length=3)
    descuento = models.FloatField(default=0)

    def precio_final(self):
        return self.precio * (1 - self.descuento)

    def sku(self):
        codigo_categoria = self.categoria.codigo.zfill(4)
        codigo_producto = str(self.id).zfill(6)

        return f'{codigo_categoria}-{codigo_producto}'
    
class Profile(models.Model):
    # Relacion con el modelo User de Django
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Atributos adicionales para el usuario
    documento_identidad = models.CharField(max_length=8)
    fecha_nacimiento = models.DateField()
    estado = models.CharField(max_length=3)
    ## Opciones de genero
    MASCULINO = 'MA'
    FEMENINO = 'FE'
    NO_BINARIO = 'NB'
    GENERO_CHOICES = [
        (MASCULINO, 'Masculino'),
        (FEMENINO, 'Femenino'),
        (NO_BINARIO, 'No Binario')
    ]
    genero = models.CharField(max_length=2, choices=GENERO_CHOICES)

    def __str__(self):
        return self.user.get_username()

class Cliente(models.Model):
    # Relacion con el modelo Perfil
    user_profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    # Atributos especificos del Cliente
    preferencias = models.ManyToManyField(to='Categoria')

    def __str__(self):
        return f'Cliente: {self.user_profile.user.get_username()}'


class Colaborador(models.Model):
    # Relacion con el modelo Perfil
    user_profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    # Atributos especificos del Colaborador
    reputacion = models.FloatField()
    cobertura_entrega = models.ManyToManyField(to='Localizacion')

    def __str__(self):
        return f'Colaborador: {self.user_profile.user.get_username()}'

