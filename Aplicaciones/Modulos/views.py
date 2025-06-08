from django.shortcuts import render, redirect,get_object_or_404
from .models import Aprender_Objetos, Aprender_Meses, Aprender_Numeros, Aprender_Dias, Profesor
from .models import Aprender_Saludos, Aprender_Animales, Aprender_Colores, Aprender_Cuerpo_Humano
from .models import Aprender_Parentesco, Aprender_Elemento_Naturaleza
from django.contrib import messages
import re
# 
def inicio(request):
    return render(request,'Bienvenida/inicio.html')

#---------------------------LOGIN------------------------
def login_profesor(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        contrasena = request.POST.get('contrasena')

        try:
            profesor = Profesor.objects.get(usuario=usuario)
        except Profesor.DoesNotExist:
            profesor = None

        if profesor and profesor.contrasena == contrasena:
            request.session['profesor_id'] = profesor.id
            request.session['profesor_usuario'] = profesor.usuario
            return redirect('profesor_bienvenida')  
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'Login/login_profesor.html')

def profesor_bienvenida(request):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')  

    return render(request, 'Profesores/profesor_bienvenida.html')

def logout_profesor(request):
    request.session.flush() 
    return redirect('login_profesor')

######################## LADO DEL ADMINISTRADOR #############################
# -----------------OBJETOS---------------------
def lista_objetos(request):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')

    objetos = Aprender_Objetos.objects.all()
    return render(request, 'AprendizajeAdmin/Objetos/lista_objetos.html', {'objetos': objetos})

#AGREGAR
def agregar_objeto(request):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')

    error_palabra = None

    if request.method == 'POST':
        palabra = request.POST.get('palabra_obj').strip()
        imagen = request.FILES.get('imagen_obj')
        audio = request.FILES.get('audio_kichwa_obj')

        if Aprender_Objetos.objects.filter(palabra_obj__iexact=palabra).exists():
            error_palabra = f'La palabra "{palabra}" ya está registrada.'
        else:
            Aprender_Objetos.objects.create(
                palabra_obj=palabra,
                imagen_obj=imagen,
                audio_kichwa_obj=audio
            )
            messages.success(request, "Palabra agregada exitosamente.")
            return redirect('lista_objetos')

    return render(request, 'AprendizajeAdmin/Objetos/agregar_objeto.html', {
        'error_palabra': error_palabra,
    })

#EDITAR
def editar_objeto(request, id):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')

    objeto = get_object_or_404(Aprender_Objetos, id=id)
    error_palabra = None

    if request.method == 'POST':
        palabra = request.POST.get('palabra_obj').strip()
        imagen = request.FILES.get('imagen_obj')
        audio = request.FILES.get('audio_kichwa_obj')

        if Aprender_Objetos.objects.filter(palabra_obj__iexact=palabra).exclude(id=id).exists():
            error_palabra = f'La palabra "{palabra}" ya está registrada.'
        else:
            objeto.palabra_obj = palabra
            if imagen:
                objeto.imagen_obj = imagen
            if audio:
                objeto.audio_kichwa_obj = audio
            objeto.save()
            messages.success(request, "Objeto actualizado correctamente.")
            return redirect('lista_objetos')

    return render(request, 'AprendizajeAdmin/Objetos/editar_objeto.html', {
        'objeto': objeto,
        'error_palabra': error_palabra
    })

#ELIMINAR
def eliminar_objeto(request, id):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')

    objeto = get_object_or_404(Aprender_Objetos, id=id)
    objeto.delete()
    messages.success(request, "Palabra eliminada correctamente.")
    return redirect('lista_objetos')


# ------------------------------- MESES ----------------------------------
def lista_meses(request):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')

    meses = Aprender_Meses.objects.all()
    return render(request, 'AprendizajeAdmin/Meses/lista_meses.html', {'meses': meses})

#AGREGAR
def agregar_mes(request):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')

    error_palabra = None

    if request.method == 'POST':
        palabra = request.POST.get('palabra_mes', '').strip()
        imagen = request.FILES.get('imagen_mes')
        audio_kichwa = request.FILES.get('audio_kichwa_mes')

        if Aprender_Meses.objects.filter(palabra_mes__iexact=palabra).exists():
            error_palabra = f'La palabra "{palabra}" ya está registrada.'
        else:
            Aprender_Meses.objects.create(
                palabra_mes=palabra,
                imagen_mes=imagen,
                audio_kichwa_mes=audio_kichwa
            )
            messages.success(request, "Palabra agregada exitosamente.")
            return redirect('lista_meses')

    return render(request, 'AprendizajeAdmin/Meses/agregar_mes.html', {
        'error_palabra': error_palabra,
    })

#EDITAR
def editar_mes(request, id):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')

    mes = get_object_or_404(Aprender_Meses, id=id)

    if request.method == 'POST':
        palabra = request.POST.get('palabra', '').strip()
        imagen = request.FILES.get('imagen')
        audio_kichwa = request.FILES.get('audio_kichwa')

        errores = {}

        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', palabra):
            errores['palabra'] = 'La palabra no debe contener números ni caracteres especiales'

        existe = Aprender_Meses.objects.filter(palabra_mes__iexact=palabra).exclude(id=id).exists()
        if existe:
            errores['palabra'] = 'Ya existe otra palabra igual.'

        if not errores:
            mes.palabra_mes = palabra

            if imagen:
                mes.imagen_mes = imagen
            if audio_kichwa:
                mes.audio_kichwa_mes = audio_kichwa

            mes.save()
            messages.success(request, "Palabra actualizada exitosamente.")
            return redirect('lista_meses')

        return render(request, 'AprendizajeAdmin/Meses/editar_mes.html', {
            'errores': errores,
            'palabra': palabra,
            'mes': mes,
        })

    return render(request, 'AprendizajeAdmin/Meses/editar_mes.html', {'mes': mes})

#ELIMINAR
def eliminar_mes(request, id):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')

    mes = get_object_or_404(Aprender_Meses, id=id)
    mes.delete()
    messages.success(request, "Palabra eliminada correctamente.")
    return redirect('lista_meses')

# -------------------------------- NUMEROS -----------------------------
def lista_numeros(request):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')

    numeros = Aprender_Numeros.objects.all()
    return render(request, 'AprendizajeAdmin/Numeros/lista_numeros.html', {'numeros': numeros})

# AGREGAR
def agregar_numero(request):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')

    error_palabra = None

    if request.method == 'POST':
        palabra = request.POST.get('palabra_num').strip()
        imagen = request.FILES.get('imagen_num')
        audio = request.FILES.get('audio_kichwa_num')

        if Aprender_Numeros.objects.filter(palabra_num__iexact=palabra).exists():
            error_palabra = f'La palabra "{palabra}" ya está registrada.'
        else:
            Aprender_Numeros.objects.create(
                palabra_num=palabra,
                imagen_num=imagen,
                audio_kichwa_num=audio
            )
            messages.success(request, "Número agregado exitosamente.")
            return redirect('lista_numeros')

    return render(request, 'AprendizajeAdmin/Numeros/agregar_numero.html', {
        'error_palabra': error_palabra,
    })

# EDITAR
def editar_numero(request, id):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')

    numero = get_object_or_404(Aprender_Numeros, id=id)
    error_palabra = None

    if request.method == 'POST':
        palabra = request.POST.get('palabra_num').strip()
        imagen = request.FILES.get('imagen_num')
        audio = request.FILES.get('audio_kichwa_num')

        if Aprender_Numeros.objects.filter(palabra_num__iexact=palabra).exclude(id=id).exists():
            error_palabra = f'La palabra "{palabra}" ya está registrada.'
        else:
            numero.palabra_num = palabra
            if imagen:
                numero.imagen_num = imagen
            if audio:
                numero.audio_kichwa_num = audio
            numero.save()
            messages.success(request, "Número actualizado correctamente.")
            return redirect('lista_numeros')

    return render(request, 'AprendizajeAdmin/Numeros/editar_numero.html', {
        'numero': numero,
        'error_palabra': error_palabra
    })

# ELIMINAR 
def eliminar_numero(request, id):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')

    numero = get_object_or_404(Aprender_Numeros, id=id)
    numero.delete()
    messages.success(request, "Número eliminado correctamente.")
    return redirect('lista_numeros')

# ---------------------------- DIAS -------------------------------
def lista_dias(request):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')

    dias = Aprender_Dias.objects.all()
    return render(request, 'AprendizajeAdmin/Dias/lista_dias.html', {'dias': dias})

# AGREGAR
def agregar_dia(request):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')

    error_palabra = None

    if request.method == 'POST':
        palabra = request.POST.get('palabra_dia').strip()
        imagen = request.FILES.get('imagen_dia')
        audio = request.FILES.get('audio_kichwa_dia')

        if Aprender_Dias.objects.filter(palabra_dia__iexact=palabra).exists():
            error_palabra = f'La palabra "{palabra}" ya está registrada.'
        else:
            Aprender_Dias.objects.create(
                palabra_dia=palabra,
                imagen_dia=imagen,
                audio_kichwa_dia=audio
            )
            messages.success(request, "Día agregado exitosamente.")
            return redirect('lista_dias')

    return render(request, 'AprendizajeAdmin/Dias/agregar_dia.html', {
        'error_palabra': error_palabra,
    })

# EDITAR
def editar_dia(request, id):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')

    dia = get_object_or_404(Aprender_Dias, id=id)
    error_palabra = None

    if request.method == 'POST':
        palabra = request.POST.get('palabra_dia').strip()
        imagen = request.FILES.get('imagen_dia')
        audio = request.FILES.get('audio_kichwa_dia')

        if Aprender_Dias.objects.filter(palabra_dia__iexact=palabra).exclude(id=id).exists():
            error_palabra = f'La palabra "{palabra}" ya está registrada.'
        else:
            dia.palabra_dia = palabra
            if imagen:
                dia.imagen_dia = imagen
            if audio:
                dia.audio_kichwa_dia = audio
            dia.save()
            messages.success(request, "Día actualizado correctamente.")
            return redirect('lista_dias')

    return render(request, 'AprendizajeAdmin/Dias/editar_dia.html', {
        'dia': dia,
        'error_palabra': error_palabra
    })

# ELIMINAR
def eliminar_dia(request, id):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')

    dia = get_object_or_404(Aprender_Dias, id=id)
    dia.delete()
    messages.success(request, "Día eliminado correctamente.")
    return redirect('lista_dias')

#------------------------- SALUDOS ------------------------------
def lista_saludos(request):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')

    saludos = Aprender_Saludos.objects.all()
    return render(request, 'AprendizajeAdmin/Saludos/lista_saludos.html', {'saludos': saludos})

# AGREGAR
def agregar_saludo(request):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')

    error_palabra = None

    if request.method == 'POST':
        palabra = request.POST.get('palabra_sal').strip()
        imagen = request.FILES.get('imagen_sal')
        audio = request.FILES.get('audio_kichwa_sal')

        if Aprender_Saludos.objects.filter(palabra_sal__iexact=palabra).exists():
            error_palabra = f'La palabra "{palabra}" ya está registrada.'
        else:
            Aprender_Saludos.objects.create(
                palabra_sal=palabra,
                imagen_sal=imagen,
                audio_kichwa_sal=audio
            )
            messages.success(request, "Saludo agregado exitosamente.")
            return redirect('lista_saludos')

    return render(request, 'AprendizajeAdmin/Saludos/agregar_saludo.html', {
        'error_palabra': error_palabra,
    })

# EDITAR
def editar_saludo(request, id):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')

    saludo = get_object_or_404(Aprender_Saludos, id=id)
    error_palabra = None

    if request.method == 'POST':
        palabra = request.POST.get('palabra_sal').strip()
        imagen = request.FILES.get('imagen_sal')
        audio = request.FILES.get('audio_kichwa_sal')

        if Aprender_Saludos.objects.filter(palabra_sal__iexact=palabra).exclude(id=id).exists():
            error_palabra = f'La palabra "{palabra}" ya está registrada.'
        else:
            saludo.palabra_sal = palabra
            if imagen:
                saludo.imagen_sal = imagen
            if audio:
                saludo.audio_kichwa_sal = audio
            saludo.save()
            messages.success(request, "Saludo actualizado correctamente.")
            return redirect('lista_saludos')

    return render(request, 'AprendizajeAdmin/Saludos/editar_saludo.html', {
        'saludo': saludo,
        'error_palabra': error_palabra
    })

# ELIMINAR
def eliminar_saludo(request, id):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')

    saludo = get_object_or_404(Aprender_Saludos, id=id)
    saludo.delete()
    messages.success(request, "Saludo eliminado correctamente.")
    return redirect('lista_saludos')

#----------------------------------ANIMALES--------------------------------
def lista_animales(request):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')

    animales = Aprender_Animales.objects.all()
    return render(request, 'AprendizajeAdmin/Animales/lista_animales.html', {'animales': animales})

# AGREGAR
def agregar_animal(request):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')

    error_palabra = None

    if request.method == 'POST':
        palabra = request.POST.get('palabra_ani').strip()
        imagen = request.FILES.get('imagen_ani')
        audio = request.FILES.get('audio_kichwa_ani')

        if Aprender_Animales.objects.filter(palabra_ani__iexact=palabra).exists():
            error_palabra = f'La palabra "{palabra}" ya está registrada.'
        else:
            Aprender_Animales.objects.create(
                palabra_ani=palabra,
                imagen_ani=imagen,
                audio_kichwa_ani=audio
            )
            messages.success(request, "Animal agregado exitosamente.")
            return redirect('lista_animales')

    return render(request, 'AprendizajeAdmin/Animales/agregar_animal.html', {
        'error_palabra': error_palabra,
    })

# EDITAR
def editar_animal(request, id):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')

    animal = get_object_or_404(Aprender_Animales, id=id)
    error_palabra = None

    if request.method == 'POST':
        palabra = request.POST.get('palabra_ani').strip()
        imagen = request.FILES.get('imagen_ani')
        audio = request.FILES.get('audio_kichwa_ani')

        if Aprender_Animales.objects.filter(palabra_ani__iexact=palabra).exclude(id=id).exists():
            error_palabra = f'La palabra "{palabra}" ya está registrada.'
        else:
            animal.palabra_ani = palabra
            if imagen:
                animal.imagen_ani = imagen
            if audio:
                animal.audio_kichwa_ani = audio
            animal.save()
            messages.success(request, "Animal actualizado correctamente.")
            return redirect('lista_animales')

    return render(request, 'AprendizajeAdmin/Animales/editar_animal.html', {
        'animal': animal,
        'error_palabra': error_palabra
    })

# ELIMINAR
def eliminar_animal(request, id):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')

    animal = get_object_or_404(Aprender_Animales, id=id)
    animal.delete()
    messages.success(request, "Animal eliminado correctamente.")
    return redirect('lista_animales')

#------------------------------COLORES---------------------------------
def lista_colores(request):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')

    colores = Aprender_Colores.objects.all()
    return render(request, 'AprendizajeAdmin/Colores/lista_colores.html', {'colores': colores})

# AGREGAR
def agregar_color(request):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')

    error_palabra = None

    if request.method == 'POST':
        palabra = request.POST.get('palabra_col').strip()
        imagen = request.FILES.get('imagen_col')
        audio = request.FILES.get('audio_kichwa_col')

        if Aprender_Colores.objects.filter(palabra_col__iexact=palabra).exists():
            error_palabra = f'La palabra "{palabra}" ya está registrada.'
        else:
            Aprender_Colores.objects.create(
                palabra_col=palabra,
                imagen_col=imagen,
                audio_kichwa_col=audio
            )
            messages.success(request, "Color agregado exitosamente.")
            return redirect('lista_colores')

    return render(request, 'AprendizajeAdmin/Colores/agregar_color.html', {
        'error_palabra': error_palabra,
    })

# EDITAR
def editar_color(request, id):
    color = get_object_or_404(Aprender_Colores, id=id)

    if request.method == 'POST':
        palabra_col = request.POST.get('palabra_col').strip()
        imagen_col = request.FILES.get('imagen_col')
        audio_kichwa_col = request.FILES.get('audio_kichwa_col')

        if Aprender_Colores.objects.filter(palabra_col__iexact=palabra_col).exclude(id=id).exists():
            return render(request, 'editar_color.html', {
                'color': color,
                'error_palabra': 'Ya existe un color con ese nombre.'
            })

        color.palabra_col = palabra_col

        if imagen_col:
            color.imagen_col = imagen_col

        if audio_kichwa_col:
            color.audio_kichwa_col = audio_kichwa_col

        color.save()
        messages.success(request, 'Color actualizado correctamente.')
        return redirect('lista_colores')

    return render(request, 'AprendizajeAdmin/Colores/editar_color.html', {'color': color})

# ELIMINAR
def eliminar_color(request, id):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')

    color = get_object_or_404(Aprender_Colores, id=id)
    color.delete()
    messages.success(request, "Color eliminado correctamente.")
    return redirect('lista_colores')

#-------------------------CUERPO HUMANO-----------------------
def lista_cuerpo_humano(request):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')

    partes = Aprender_Cuerpo_Humano.objects.all()
    return render(request, 'AprendizajeAdmin/Cuerpo_Humano/lista_cuerpo_humano.html', {'partes': partes})

# AGREGAR
def agregar_cuerpo_humano(request):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')

    error_palabra = None

    if request.method == 'POST':
        palabra = request.POST.get('palabra_cue').strip()
        imagen = request.FILES.get('imagen_cue')
        audio = request.FILES.get('audio_kichwa_cue')

        if Aprender_Cuerpo_Humano.objects.filter(palabra_cue__iexact=palabra).exists():
            error_palabra = f'La palabra "{palabra}" ya está registrada.'
        else:
            Aprender_Cuerpo_Humano.objects.create(
                palabra_cue=palabra,
                imagen_cue=imagen,
                audio_kichwa_cue=audio
            )
            messages.success(request, "Parte del cuerpo humano agregada exitosamente.")
            return redirect('lista_cuerpo_humano')

    return render(request, 'AprendizajeAdmin/Cuerpo_Humano/agregar_cuerpo_humano.html', {
        'error_palabra': error_palabra,
    })

# EDITAR
def editar_cuerpo_humano(request, id):
    cuerpo = get_object_or_404(Aprender_Cuerpo_Humano, id=id)

    if request.method == 'POST':
        palabra_cue = request.POST.get('palabra_cue').strip()
        imagen_cue = request.FILES.get('imagen_cue')
        audio_kichwa_cue = request.FILES.get('audio_kichwa_cue')

        if Aprender_Cuerpo_Humano.objects.filter(palabra_cue__iexact=palabra_cue).exclude(id=id).exists():
            return render(request, 'AprendizajeAdmin/CuerpoHumano/editar_cuerpo_humano.html', {
                'cuerpo': cuerpo,
                'error_palabra': 'Ya existe una parte del cuerpo con ese nombre.'
            })

        cuerpo.palabra_cue = palabra_cue

        if imagen_cue:
            cuerpo.imagen_cue = imagen_cue

        if audio_kichwa_cue:
            cuerpo.audio_kichwa_cue = audio_kichwa_cue

        cuerpo.save()
        messages.success(request, 'Parte del cuerpo actualizada correctamente.')
        return redirect('lista_cuerpo_humano')

    return render(request, 'AprendizajeAdmin/Cuerpo_Humano/editar_cuerpo_humano.html', {'cuerpo': cuerpo})

# ELIMINAR
def eliminar_cuerpo_humano(request, id):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')

    cuerpo = get_object_or_404(Aprender_Cuerpo_Humano, id=id)
    cuerpo.delete()
    messages.success(request, "Parte del cuerpo eliminada correctamente.")
    return redirect('lista_cuerpo_humano')

#-----------------------PARENTESCO-----------------------
def lista_parentesco(request):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')

    parentescos = Aprender_Parentesco.objects.all()
    return render(request, 'AprendizajeAdmin/Parentesco/lista_parentesco.html', {'parentescos': parentescos})

# AGREGAR
def agregar_parentesco(request):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')

    error_palabra = None

    if request.method == 'POST':
        palabra = request.POST.get('palabra_par').strip()
        imagen = request.FILES.get('imagen_par')
        audio = request.FILES.get('audio_kichwa_par')

        if Aprender_Parentesco.objects.filter(palabra_par__iexact=palabra).exists():
            error_palabra = f'La palabra "{palabra}" ya está registrada.'
        else:
            Aprender_Parentesco.objects.create(
                palabra_par=palabra,
                imagen_par=imagen,
                audio_kichwa_par=audio
            )
            messages.success(request, "Parentesco agregado exitosamente.")
            return redirect('lista_parentesco')

    return render(request, 'AprendizajeAdmin/Parentesco/agregar_parentesco.html', {
        'error_palabra': error_palabra,
    })

# EDITAR
def editar_parentesco(request, id):
    parentesco = get_object_or_404(Aprender_Parentesco, id=id)

    if request.method == 'POST':
        palabra_par = request.POST.get('palabra_par', '').strip()
        imagen_par = request.FILES.get('imagen_par')
        audio_kichwa_par = request.FILES.get('audio_kichwa_par')

        if Aprender_Parentesco.objects.filter(palabra_par__iexact=palabra_par).exclude(id=id).exists():
            return render(request, 'AprendizajeAdmin/Parentesco/editar_parentesco.html', {
                'parentesco': parentesco,
                'error_palabra': 'Ya existe un registro con ese nombre.'
            })

        parentesco.palabra_par = palabra_par

        if imagen_par:
            parentesco.imagen_par = imagen_par

        if audio_kichwa_par:
            parentesco.audio_kichwa_par = audio_kichwa_par

        parentesco.save()
        messages.success(request, 'Parentesco actualizado correctamente.')
        return redirect('lista_parentesco')  

    return render(request, 'AprendizajeAdmin/Parentesco/editar_parentesco.html', {'parentesco': parentesco})

# ELIMINAR
def eliminar_parentesco(request, id):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')

    parentesco = get_object_or_404(Aprender_Parentesco, id=id)
    parentesco.delete()
    messages.success(request, "Parentesco eliminado correctamente.")
    return redirect('lista_parentesco')

#------------------------ELEMENTOS NATURALEZA-------------------
def lista_elemento_naturaleza(request):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')

    elementos = Aprender_Elemento_Naturaleza.objects.all()
    return render(request, 'AprendizajeAdmin/Elemento_Naturaleza/lista_elemento_naturaleza.html', {'elementos': elementos})

# AGREGAR
def agregar_elemento_naturaleza(request):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')

    error_palabra = None

    if request.method == 'POST':
        palabra = request.POST.get('palabra_ele').strip()
        imagen = request.FILES.get('imagen_ele')
        audio = request.FILES.get('audio_kichwa_ele')

        if Aprender_Elemento_Naturaleza.objects.filter(palabra_ele__iexact=palabra).exists():
            error_palabra = f'La palabra "{palabra}" ya está registrada.'
        else:
            Aprender_Elemento_Naturaleza.objects.create(
                palabra_ele=palabra,
                imagen_ele=imagen,
                audio_kichwa_ele=audio
            )
            messages.success(request, "Elemento de la naturaleza agregado exitosamente.")
            return redirect('lista_elemento_naturaleza')

    return render(request, 'AprendizajeAdmin/Elemento_Naturaleza/agregar_elemento_naturaleza.html', {
        'error_palabra': error_palabra,
    })

# EDITAR
def editar_elemento_naturaleza(request, id):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')

    elemento = get_object_or_404(Aprender_Elemento_Naturaleza, id=id)

    if request.method == 'POST':
        palabra_ele = request.POST.get('palabra_ele').strip()
        imagen_ele = request.FILES.get('imagen_ele')
        audio_kichwa_ele = request.FILES.get('audio_kichwa_ele')

        if Aprender_Elemento_Naturaleza.objects.filter(palabra_ele__iexact=palabra_ele).exclude(id=id).exists():
            return render(request, 'AprendizajeAdmin/Naturaleza/editar_elemento_naturaleza.html', {
                'elemento': elemento,
                'error_palabra': 'Ya existe un elemento de la naturaleza con ese nombre.'
            })

        elemento.palabra_ele = palabra_ele

        if imagen_ele:
            elemento.imagen_ele = imagen_ele

        if audio_kichwa_ele:
            elemento.audio_kichwa_ele = audio_kichwa_ele

        elemento.save()
        messages.success(request, 'Elemento de la naturaleza actualizado correctamente.')
        return redirect('lista_elemento_naturaleza')

    return render(request, 'AprendizajeAdmin/Elemento_Naturaleza/editar_elemento_naturaleza.html', {
        'elemento': elemento
    })

#ELIMINAR
def eliminar_elemento_naturaleza(request, id):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')

    elemento = get_object_or_404(Aprender_Elemento_Naturaleza, id=id)
    elemento.delete()
    messages.success(request, "Elemento de la naturaleza eliminado correctamente.")
    return redirect('lista_elemento_naturaleza')








############################### LADO DEL USUARIO #################################

#-------------------------------ARENDER  ---------------------
# MESES
def ver_meses(request):
    meses = Aprender_Meses.objects.all()
    return render(request, 'Aprender/meses.html', {'meses': meses})

# OBJETOS
def ver_objetos(request):
    objetos = Aprender_Objetos.objects.all()
    return render(request, 'Aprender/objetos.html', {'objetos': objetos})

# NUMEROS
def ver_numeros(request):
    numeros = Aprender_Numeros.objects.all()
    return render(request, 'Aprender/numeros.html', {'numeros': numeros})

# DIAS DE LA SEMANA
def ver_dias(request):
    dias = Aprender_Dias.objects.all()
    return render(request, 'Aprender/dias.html', {'dias': dias})

# ANIMALES
def ver_animales(request):
    animales = Aprender_Animales.objects.all()
    return render(request, 'Aprender/animales.html', {'animales': animales})

# SALUDOS
def ver_saludos(request):
    saludos = Aprender_Saludos.objects.all()
    return render(request, 'Aprender/saludos.html', {'saludos': saludos})

# COLORES
def ver_colores(request):
    colores = Aprender_Colores.objects.all()
    return render(request, 'Aprender/colores.html', {'colores': colores})

# CUERPO HUMANO
def ver_cuerpo_humano(request):
    cuerpo_humano = Aprender_Cuerpo_Humano.objects.all()
    return render(request, 'Aprender/cuerpo_humano.html', {'cuerpo_humano': cuerpo_humano})

# PARENTESCO
def ver_parentesco(request):
    parentescos = Aprender_Parentesco.objects.all()
    return render(request, 'Aprender/parentesco.html', {'parentescos': parentescos})

# ELEMENTO NATURALEZA
def ver_elemento_naturaleza(request):
    elemento_naturaleza = Aprender_Elemento_Naturaleza.objects.all()
    return render(request, 'Aprender/elemento_naturaleza.html', {'elemento_naturaleza': elemento_naturaleza})

#-----------------------JUGAR ------------------------------
# MESES
def jugar_meses(request):
    meses = Aprender_Meses.objects.all()
    return render(request, 'Juegos/jugar_meses.html', {'meses': meses})

# OBJETOS
import random
def jugar_objetos(request):
    objetos = list(Aprender_Objetos.objects.all())
    random.shuffle(objetos)
    objetos = objetos[:10]  # Selecciona 10 aleatorios

    return render(request, 'Juegos/jugar_objetos.html', {'objetos': objetos})

# NUMEROS
def jugar_numeros(request):
    numeros = Aprender_Numeros.objects.all()
    return render(request, 'Juegos/jugar_numeros.html', {'numeros': numeros})

# DIAS DE LA SEMANA
def jugar_dias(request):
    dias = Aprender_Dias.objects.all()
    return render(request, 'Juegos/jugar_dias.html', {'dias': dias})

# ANIMALES
def jugar_animales(request):
    todos = list(Aprender_Animales.objects.all())
    seleccionados = random.sample(todos, min(15, len(todos)))  # 15 al azar o menos si hay pocos
    return render(request, 'Juegos/jugar_animales.html', {'animales': seleccionados})

# COLORES
def jugar_colores(request):
    colores = Aprender_Colores.objects.all()
    return render(request, 'Juegos/jugar_colores.html', {'colores': colores})

# SALUDOS
def jugar_saludos(request):
    saludos = list(Aprender_Saludos.objects.all())  
    random.shuffle(saludos) 
    return render(request, 'Juegos/jugar_saludos.html', {'saludos': saludos})

# CUERPO HUMANO
def jugar_cuerpo_humano(request):
    cuerpo_humano = Aprender_Cuerpo_Humano.objects.all()
    return render(request, 'Juegos/jugar_cuerpo_humano.html', {'cuerpo_humano': cuerpo_humano})

# PARENTESCO
def jugar_parentesco(request):
    parentescos = list(Aprender_Parentesco.objects.all())
    random.shuffle(parentescos)
    return render(request, 'Juegos/jugar_parentesco.html', {'parentescos': parentescos})

# ELEMENTOS NATURALEZA
def jugar_elementos_naturaleza(request):
    elementos = Aprender_Elemento_Naturaleza.objects.all()
    return render(request, 'Juegos/jugar_elementos_naturaleza.html', {'elementos': elementos})


#--------------------------APRENDER DIFERENTES MODULOS-------------------------------
def aprender(request):
    aprender_items = Aprender_Objetos.objects.all() 
    return render(request, 'Aprender/aprender.html', {'aprender_items': aprender_items})

