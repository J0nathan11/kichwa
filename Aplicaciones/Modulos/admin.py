from django.contrib import admin
from .models import Profesor, Aprender_Objetos, Aprender_Meses,Aprender_Numeros, Aprender_Dias
from .models import Aprender_Saludos, Aprender_Animales, Aprender_Colores, Aprender_Cuerpo_Humano
from .models import Aprender_Parentesco, Aprender_Elemento_Naturaleza
# Register your models here.
admin.site.register(Aprender_Objetos)
admin.site.register(Aprender_Meses)
admin.site.register(Aprender_Numeros)
admin.site.register(Aprender_Dias)
admin.site.register(Aprender_Saludos)
admin.site.register(Aprender_Animales)
admin.site.register(Aprender_Colores)
admin.site.register(Aprender_Cuerpo_Humano)
admin.site.register(Aprender_Parentesco)
admin.site.register(Aprender_Elemento_Naturaleza)
admin.site.register(Profesor)
