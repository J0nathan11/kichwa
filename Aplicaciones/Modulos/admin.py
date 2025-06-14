from django.contrib import admin
from .models import Profesor, Aprender_Objetos, Aprender_Meses,Aprender_Numeros, Aprender_Dias
from .models import Aprender_Saludos, Aprender_Animales, Aprender_Colores, Aprender_Cuerpo_Humano
from .models import Aprender_Parentesco, Aprender_Elemento_Naturaleza, Estudiante_Cuarto, Estudiante_Tercero
from .models import Evaluacion_Cuarto, Evaluacion_Tercero, Resultado_Evaluacion_Cuarto, Resultado_Evaluacion_Tercero 
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
admin.site.register(Estudiante_Cuarto)
admin.site.register(Estudiante_Tercero)
admin.site.register(Evaluacion_Cuarto)
admin.site.register(Evaluacion_Tercero)
admin.site.register(Resultado_Evaluacion_Cuarto)
admin.site.register(Resultado_Evaluacion_Tercero)
