from django.shortcuts import render, redirect,get_object_or_404
from .models import Aprender_Objetos, Aprender_Meses, Aprender_Numeros, Aprender_Dias, Profesor
from .models import Aprender_Saludos, Aprender_Animales, Aprender_Colores, Aprender_Cuerpo_Humano
from .models import Aprender_Parentesco, Aprender_Elemento_Naturaleza, Estudiante_Cuarto, Estudiante_Tercero
from .models import Evaluacion_Cuarto, Evaluacion_Tercero, Resultado_Evaluacion_Cuarto, Resultado_Evaluacion_Tercero
from django.contrib import messages
import re
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login


def login_admin(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        contrasena = request.POST.get('contrasena')

        user = authenticate(request, username=usuario, password=contrasena)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin_bienvenida')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')

    return render(request, 'Login/login_admin.html')


# SOLO ADMIN
@login_required(login_url='login_admin')
@user_passes_test(lambda u: u.is_superuser, login_url='login_admin')
def admin_bienvenida(request):
    return render(request, 'Admin/admin_bienvenida.html', {
        'usuario': request.user
    })


from django.contrib.auth import logout

def logout_admin(request):
    logout(request)
    return redirect('login_admin')


#-------------------------SUPER ADMINISTRADOR------------
# LISTA PROFESORES
def lista_profesor(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('login_admin')  # Solo admins acceden

    profesores = Profesor.objects.all()
    return render(request, 'Admin/Profesores/lista_profesor.html', {
        'profesores': profesores
    })

# CAMBIAR ESTADO DEL PROFESOR 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@login_required(login_url='login_admin')
@user_passes_test(lambda u: u.is_superuser, login_url='login_admin')
@csrf_exempt
def ajax_cambiar_estado_profesor(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        profesor = get_object_or_404(Profesor, id=id)
        profesor.estado = not profesor.estado
        profesor.save()
        return JsonResponse({'estado': profesor.estado})
    return JsonResponse({'error': 'Método no permitido'}, status=405)

# -----------VALIDACIONES -------------
import re
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

# VALIDACION TELEFONO
def validar_telefono_ecuador(numero):
    return bool(re.fullmatch(r'09\d{8}', numero))

# VALIDACION CORREO
def validar_correo(correo):
    try:
        validate_email(correo)
        return True
    except ValidationError:
        return False

# AGREGAR PROFESOR
from django.core.mail import send_mail
from django.template.loader import render_to_string

def agregar_profesor(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('login_admin')

    error_cedula = None
    error_usuario = None
    error_email = None
    error_telefono = None

    if request.method == 'POST':
        nombres = request.POST.get('nombres').strip()
        apellidos = request.POST.get('apellidos').strip()
        cedula = request.POST.get('cedula').strip()
        telefono = request.POST.get('telefono').strip()
        email = request.POST.get('email').strip()
        sexo = request.POST.get('sexo')
        estado = True if request.POST.get('estado') == 'ACTIVO' else False
        usuario = request.POST.get('usuario').strip()
        contrasena = request.POST.get('contrasena')
        foto = request.FILES.get('foto')

        # Validaciones
        if not validar_cedula_ecuatoriana(cedula):
            error_cedula = "La cédula ingresada no es válida."
        elif Profesor.objects.filter(cedula=cedula).exists():
            error_cedula = f"La cédula '{cedula}' ya está registrada."
        elif Profesor.objects.filter(usuario=usuario).exists():
            error_usuario = f"El usuario '{usuario}' ya está registrado."
        elif Profesor.objects.filter(email=email).exists():
            error_email = f"El correo '{email}' ya está registrado."
        elif not validar_telefono_ecuador(telefono):
            error_telefono = "El número de teléfono debe comenzar con 09 y tener 10 dígitos."
        elif not validar_correo(email):
            error_email = "El correo electrónico ingresado no es válido."
        else:
            profesor = Profesor(
                nombres=nombres,
                apellidos=apellidos,
                cedula=cedula,
                telefono=telefono,
                email=email,
                sexo=sexo,
                estado=estado,
                usuario=usuario,
                contrasena=contrasena
            )
            if foto:
                profesor.foto = foto

            profesor.save()

            # ✅ Enviar correo al profesor
            try:
                asunto = '🎓 Confirmación de Registro'
                mensaje = render_to_string('correos/profesor_confirmacion.html', {
                    'nombre': nombres,
                    'usuario': usuario,
                    'email': email,
                })
                
                send_mail(
                    asunto,
                    '',
                    settings.EMAIL_HOST_USER,  # ✅ usa lo que tienes en settings.py
                    [email],
                    html_message=mensaje,
                    fail_silently=False
                )
            except Exception as e:
                print("✅ Enviando correo a:", email)

                print("❌ Error al enviar correo:", e)

            messages.success(request, 'Profesor agregado correctamente.')
            return redirect('lista_profesor')

    return render(request, 'Admin/Profesores/agregar_profesor.html', {
        'error_cedula': error_cedula,
        'error_usuario': error_usuario,
        'error_email': error_email,
        'error_telefono': error_telefono
    })


from django.core.mail import send_mail
from django.template.loader import render_to_string

# EDITAR PROFESOR
def editar_profesor(request, id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('login_admin')

    profesor = get_object_or_404(Profesor, id=id)

    error_cedula = None
    error_usuario = None
    error_email = None
    error_telefono = None

    email_anterior = profesor.email  # 🔍 Guarda el correo anterior

    if request.method == 'POST':
        nombres = request.POST.get('nombres').strip()
        apellidos = request.POST.get('apellidos').strip()
        cedula = request.POST.get('cedula').strip()
        telefono = request.POST.get('telefono').strip()
        email = request.POST.get('email').strip()
        sexo = request.POST.get('sexo')
        estado = True if request.POST.get('estado') == 'ACTIVO' else False
        usuario = request.POST.get('usuario').strip()
        contrasena = request.POST.get('contrasena')
        foto = request.FILES.get('foto')

        # Validaciones
        if not validar_cedula_ecuatoriana(cedula):
            error_cedula = "La cédula ingresada no es válida."
        elif Profesor.objects.exclude(id=id).filter(cedula=cedula).exists():
            error_cedula = f"La cédula '{cedula}' ya está registrada."
        elif Profesor.objects.exclude(id=id).filter(usuario=usuario).exists():
            error_usuario = f"El usuario '{usuario}' ya está registrado."
        elif Profesor.objects.exclude(id=id).filter(email=email).exists():
            error_email = f"El correo '{email}' ya está registrado."
        elif not validar_telefono_ecuador(telefono):
            error_telefono = "El número de teléfono debe comenzar con 09 y tener 10 dígitos."
        elif not validar_correo(email):
            error_email = "El correo electrónico ingresado no es válido."
        else:
            profesor.nombres = nombres
            profesor.apellidos = apellidos
            profesor.cedula = cedula
            profesor.telefono = telefono
            profesor.email = email
            profesor.sexo = sexo
            profesor.estado = estado
            profesor.usuario = usuario
            profesor.contrasena = contrasena

            if foto:
                profesor.foto = foto

            profesor.save()

            # ✅ Si cambió el correo, enviar notificación al nuevo email
            if email != email_anterior:
                try:
                    asunto = '📧 Actualización de Correo Electrónico'
                    mensaje = render_to_string('correos/profesor_confirmacion.html', {
                        'nombre': nombres,
                        'usuario': usuario,
                        'email': email,
                    })

                    send_mail(
                        asunto,
                        '',
                        settings.EMAIL_HOST_USER,
                        [email],
                        html_message=mensaje,
                        fail_silently=False
                    )
                except Exception as e:
                    print("❌ Error al enviar notificación de correo cambiado:", e)

            messages.success(request, 'Datos del profesor actualizados correctamente.')
            return redirect('lista_profesor')

    return render(request, 'Admin/Profesores/editar_profesor.html', {
        'profesor': profesor,
        'error_cedula': error_cedula,
        'error_usuario': error_usuario,
        'error_email': error_email,
        'error_telefono': error_telefono
    })

# ELIMINAR
def eliminar_profesor(request, id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('login_admin')

    profesor = get_object_or_404(Profesor, id=id)
    profesor.delete()
    messages.success(request, "Profesor eliminado correctamente.")
    return redirect('lista_profesor') 

# ----------------------PAGUINA DE INICIO----------------------
def inicio(request):
    return render(request,'Bienvenida/inicio.html')

#---------------------------LOGIN PROFESOR------------------------
def login_profesor(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        contrasena = request.POST.get('contrasena')

        try:
            profesor = Profesor.objects.get(usuario=usuario)
        except Profesor.DoesNotExist:
            profesor = None

        if profesor:
            if profesor.contrasena != contrasena:
                messages.error(request, 'Contraseña incorrecta.')
            elif not profesor.estado:
                messages.error(request, 'Su cuenta está inactiva. Comuníquese con el administrador.')
            else:
                request.session['profesor_id'] = profesor.id
                request.session['profesor_usuario'] = profesor.usuario
                return redirect('profesor_bienvenida')
        else:
            messages.error(request, 'El usuario no existe.')

    return render(request, 'Login/login_profesor.html')

# SALIDA
def logout_profesor(request):
    request.session.flush() 
    return redirect('login_profesor')

# BIENVENIDA PROFESOR
def profesor_bienvenida(request):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')  

    profesor_id = request.session.get('profesor_id')
    profesor = Profesor.objects.get(id=profesor_id)

    return render(request, 'Profesores/profesor_bienvenida.html', {
        'profesor': profesor
    })

# CONFIGURACION PROFESOR
def configuracion_profesor(request):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')

    profesor = get_object_or_404(Profesor, id=request.session['profesor_id'])

    if request.method == 'POST':
        profesor.nombres = request.POST.get('nombres')
        profesor.apellidos = request.POST.get('apellidos')
        profesor.cedula = request.POST.get('cedula')
        profesor.telefono = request.POST.get('telefono')
        profesor.email = request.POST.get('email')
        profesor.sexo = request.POST.get('sexo')
        profesor.usuario = request.POST.get('usuario')
        profesor.contrasena = request.POST.get('contrasena')  # texto plano como pediste

        if 'foto' in request.FILES:
            profesor.foto = request.FILES['foto']

        profesor.save()

        # ✅ Enviar correo de confirmación de actualización
        try:
            asunto = '🔔 Actualización de Datos'
            mensaje = render_to_string('correos/profesor_actualizacion.html', {
                'nombre': profesor.nombres,
                'usuario': profesor.usuario,
                'email': profesor.email,
            })

            send_mail(
                asunto,
                '',
                settings.EMAIL_HOST_USER,
                [profesor.email],
                html_message=mensaje,
                fail_silently=False
            )
        except Exception as e:
            print("❌ Error al enviar correo de actualización:", e)

        messages.success(request, 'Datos actualizados correctamente.')
        return redirect('configuracion_profesor')

    return render(request, 'Administrador/Profesores/configuracion_profesor.html', {'profesor': profesor})


######################## LADO DEL ADMINISTRADOR #############################
# PDF Modelos de Aprendizaje
from django.conf import settings
from django.templatetags.static import static
from django.utils.encoding import smart_str
import os
from urllib.parse import unquote

def link_callback(uri, rel):

    uri = unquote(uri)
    # Convierte rutas estáticas y de medios en rutas absolutas en disco
    if uri.startswith(settings.MEDIA_URL):
        path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    elif uri.startswith(settings.STATIC_URL):
        path = os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, ""))
    else:
        return uri  # URL completa http(s)
    
    if not os.path.isfile(path):
        raise Exception(f'Media URI must exist: {path}')
    return path

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

# PDF
def generar_pdf_objetos(request):
    objetos = Aprender_Objetos.objects.all()
    total_objetos = objetos.count()

    template = get_template('AprendizajeAdmin/Objetos/Reportes/reporte_objetos.html')
    html = template.render({'objetos': objetos, 'total_objetos': total_objetos}, request)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reporte_objetos.pdf"'

    pisa_status = pisa.CreatePDF(
        BytesIO(html.encode('utf-8')),
        dest=response,
        link_callback=link_callback
    )

    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)

    return response

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

# PDF
def generar_pdf_meses(request):
    meses = Aprender_Meses.objects.all()
    total_meses = meses.count()

    template = get_template('AprendizajeAdmin/Meses/Reportes/reporte_meses.html')
    html = template.render({
        'meses': meses,
        'total_meses': total_meses
    }, request)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reporte_meses.pdf"'

    pisa_status = pisa.CreatePDF(
        BytesIO(html.encode('utf-8')),
        dest=response,
        link_callback=link_callback
    )

    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)

    return response

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

# PDF
def generar_pdf_numeros(request):
    numeros = Aprender_Numeros.objects.all()
    total_numeros = numeros.count()

    template = get_template('AprendizajeAdmin/Numeros/Reportes/reporte_numeros.html')
    html = template.render({'numeros': numeros, 'total_numeros': total_numeros}, request)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reporte_numeros.pdf"'

    pisa_status = pisa.CreatePDF(
        BytesIO(html.encode('utf-8')),
        dest=response,
        link_callback=link_callback
    )

    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)

    return response

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

# PDF
def generar_pdf_dias(request):
    dias = Aprender_Dias.objects.all()
    total_dias = dias.count()

    template = get_template('AprendizajeAdmin/Dias/Reportes/reporte_dias.html')
    html = template.render({
        'dias': dias,
        'total_dias': total_dias
    }, request)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reporte_dias.pdf"'

    pisa_status = pisa.CreatePDF(
        BytesIO(html.encode('utf-8')),
        dest=response,
        link_callback=link_callback
    )

    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)

    return response

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

# PDF
def generar_pdf_saludos(request):
    saludos = Aprender_Saludos.objects.all()
    total_saludos = saludos.count()

    template = get_template('AprendizajeAdmin/Saludos/Reportes/reporte_saludos.html')
    html = template.render({'saludos': saludos, 'total_saludos': total_saludos}, request)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reporte_saludos.pdf"'

    pisa_status = pisa.CreatePDF(
        BytesIO(html.encode('utf-8')),
        dest=response,
        link_callback=link_callback
    )

    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)

    return response

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

# PDF
def generar_pdf_animales(request):
    animales = Aprender_Animales.objects.all()
    total_animales = animales.count()

    template = get_template('AprendizajeAdmin/Animales/Reportes/reporte_animales.html')
    html = template.render({
        'animales': animales,
        'total_animales': total_animales
    }, request)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reporte_animales.pdf"'

    pisa_status = pisa.CreatePDF(
        BytesIO(html.encode('utf-8')),
        dest=response,
        link_callback=link_callback
    )

    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)

    return response

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

# PDF
def generar_pdf_colores(request):
    colores = Aprender_Colores.objects.all()
    total_colores = colores.count()

    template = get_template('AprendizajeAdmin/Colores/Reportes/reporte_colores.html')
    html = template.render({
        'colores': colores,
        'total_colores': total_colores
    }, request)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reporte_colores.pdf"'

    pisa_status = pisa.CreatePDF(
        BytesIO(html.encode('utf-8')),
        dest=response,
        link_callback=link_callback
    )

    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)

    return response

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

# PDF
def generar_pdf_cuerpo_humano(request):
    partes = Aprender_Cuerpo_Humano.objects.all()
    total_partes = partes.count()

    template = get_template('AprendizajeAdmin/Cuerpo_Humano/Reportes/reporte_cuerpo.html')
    html = template.render({
        'partes': partes,
        'total_partes': total_partes
    }, request)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reporte_cuerpo_humano.pdf"'

    pisa_status = pisa.CreatePDF(
        BytesIO(html.encode('utf-8')),
        dest=response,
        link_callback=link_callback
    )

    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)

    return response

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

# PDF
def generar_pdf_parentescos(request):
    parentescos = Aprender_Parentesco.objects.all()
    total_parentescos = parentescos.count()

    template = get_template('AprendizajeAdmin/Parentesco/Reportes/reporte_parentescos.html')
    html = template.render({'parentescos': parentescos, 'total_parentescos': total_parentescos}, request)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reporte_parentescos.pdf"'

    pisa_status = pisa.CreatePDF(
        BytesIO(html.encode('utf-8')),
        dest=response,
        link_callback=link_callback
    )

    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)

    return response

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

# PDF
def generar_pdf_elementos(request):
    elementos = Aprender_Elemento_Naturaleza.objects.all()
    total_elementos = elementos.count()

    template = get_template('AprendizajeAdmin/Elemento_Naturaleza/Reportes/reporte_elementos.html')
    html = template.render({
        'elementos': elementos,
        'total_elementos': total_elementos
    }, request)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reporte_elementos_naturaleza.pdf"'

    pisa_status = pisa.CreatePDF(
        BytesIO(html.encode('utf-8')),
        dest=response,
        link_callback=link_callback
    )

    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)

    return response

#----------------------SELECCION DE ESTUDIANTE------------
def seleccion_estudiantes(request):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')
    
    estudiantes = Profesor.objects.all()
    return render(request, 'Administrador/Estudiantes/seleccion_estudiantes.html', {'estudiantes': estudiantes})


# -----------------------ESTUDIANTES CUARTO-----------------------
# VALIDACION CEDULA
def validar_cedula_ecuatoriana(cedula):
    if not cedula.isdigit() or len(cedula) != 10:
        return False

    provincia = int(cedula[0:2])
    if provincia < 1 or provincia > 24:
        return False

    coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2]
    suma = 0
    for i in range(9):
        val = int(cedula[i]) * coeficientes[i]
        if val >= 10:
            val -= 9
        suma += val

    digito_verificador = 10 - (suma % 10)
    if digito_verificador == 10:
        digito_verificador = 0

    return digito_verificador == int(cedula[9])


# LISTADO
def lista_estudiantes_cuarto(request):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')
    
    estudiantes = Estudiante_Cuarto.objects.all()
    return render(request, 'Administrador/Estudiantes/Cuarto/lista_estudiantes_cuarto.html', {'estudiantes': estudiantes})

# AGREGAR CUARTO
def agregar_estudiante_cuarto(request):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')

    error_cedula = None

    if request.method == 'POST':
        nombres = request.POST.get('nombres_est').strip()
        apellidos = request.POST.get('apellidos_est').strip()
        cedula = request.POST.get('cedula_est').strip()
        genero = request.POST.get('genero_est')
        nivel = request.POST.get('nivel_escolar_est')
        estado = request.POST.get('estado_est')

        if not validar_cedula_ecuatoriana(cedula):
            error_cedula = "La cédula ingresada no es válida."
        elif Estudiante_Cuarto.objects.filter(cedula_est_cua=cedula).exists():
            error_cedula = f'La cédula "{cedula}" ya está registrada.'
        else:
            Estudiante_Cuarto.objects.create(
                nombres_est_cua=nombres,
                apellidos_est_cua=apellidos,
                cedula_est_cua=cedula,
                genero_est_cua=genero,
                nivel_escolar_est_cua=nivel,
                estado_est_cua=estado
            )
            messages.success(request, "Estudiante de Cuarto agregado exitosamente.")
            return redirect('lista_estudiantes_cuarto')

    return render(request, 'Administrador/Estudiantes/Cuarto/agregar_estudiante_cuarto.html', {
        'error_cedula': error_cedula,
    })

# EDITAR CUARTO
def editar_estudiante_cuarto(request, id_est):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')

    estudiante = get_object_or_404(Estudiante_Cuarto, id=id_est)
    error_cedula = None

    if request.method == 'POST':
        nombres = request.POST.get('nombres_est').strip()
        apellidos = request.POST.get('apellidos_est').strip()
        cedula = request.POST.get('cedula_est').strip()
        genero = request.POST.get('genero_est')
        nivel = request.POST.get('nivel_escolar_est')
        estado = request.POST.get('estado_est')

        if not validar_cedula_ecuatoriana(cedula):
            error_cedula = "La cédula ingresada no es válida."
        elif Estudiante_Cuarto.objects.filter(cedula_est_cua=cedula).exclude(id=id_est).exists():
            error_cedula = f'La cédula \"{cedula}\" ya está registrada en otro estudiante.'
        else:
            estudiante.nombres_est_cua = nombres
            estudiante.apellidos_est_cua = apellidos
            estudiante.cedula_est_cua = cedula
            estudiante.genero_est_cua = genero
            estudiante.nivel_escolar_est_cua = nivel
            estudiante.estado_est_cua = estado
            estudiante.save()

            messages.success(request, "Estudiante de Cuarto actualizado exitosamente.")
            return redirect('lista_estudiantes_cuarto')

    return render(request, 'Administrador/Estudiantes/Cuarto/editar_estudiante_cuarto.html', {
        'estudiante': estudiante,
        'error_cedula': error_cedula
    })

# ELIMINAR CUARTO
def eliminar_estudiante_cuarto(request, id):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')

    estudiante = get_object_or_404(Estudiante_Cuarto, id=id)
    estudiante.delete()
    messages.success(request, "Estudiante de Cuarto eliminado correctamente.")
    return redirect('lista_estudiantes_cuarto')



# -----------------------ESTUDIANTES TERCERO-----------------------
def lista_estudiantes_tercero(request):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')
    
    estudiantes = Estudiante_Tercero.objects.all()
    return render(request, 'Administrador/Estudiantes/Tercero/lista_estudiantes_tercero.html', {'estudiantes': estudiantes})

# AGREGAR TERCERO
def agregar_estudiante_tercero(request):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')

    error_cedula = None

    if request.method == 'POST':
        nombres = request.POST.get('nombres_est').strip()
        apellidos = request.POST.get('apellidos_est').strip()
        cedula = request.POST.get('cedula_est').strip()
        genero = request.POST.get('genero_est')
        nivel = request.POST.get('nivel_escolar_est')
        estado = request.POST.get('estado_est')

        if not validar_cedula_ecuatoriana(cedula):
            error_cedula = "La cédula ingresada no es válida."
        elif Estudiante_Tercero.objects.filter(cedula_est_ter=cedula).exists():
            error_cedula = f'La cédula \"{cedula}\" ya está registrada.'
        else:
            Estudiante_Tercero.objects.create(
                nombres_est_ter=nombres,
                apellidos_est_ter=apellidos,
                cedula_est_ter=cedula,
                genero_est_ter=genero,
                nivel_escolar_est_ter=nivel,
                estado_est_ter=estado
            )
            messages.success(request, "Estudiante de Tercero agregado exitosamente.")
            return redirect('lista_estudiantes_tercero')

    return render(request, 'Administrador/Estudiantes/Tercero/agregar_estudiante_tercero.html', {
        'error_cedula': error_cedula,
    })

# EDITAR TERCERO
def editar_estudiante_tercero(request, id_est):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')

    estudiante = get_object_or_404(Estudiante_Tercero, id=id_est)
    error_cedula = None

    if request.method == 'POST':
        nombres = request.POST.get('nombres_est').strip()
        apellidos = request.POST.get('apellidos_est').strip()
        cedula = request.POST.get('cedula_est').strip()
        genero = request.POST.get('genero_est')
        nivel = request.POST.get('nivel_escolar_est')
        estado = request.POST.get('estado_est')

        if not validar_cedula_ecuatoriana(cedula):
            error_cedula = "La cédula ingresada no es válida."
        elif Estudiante_Tercero.objects.filter(cedula_est_ter=cedula).exclude(id=id_est).exists():
            error_cedula = f'La cédula \"{cedula}\" ya está registrada en otro estudiante.'
        else:
            estudiante.nombres_est_ter = nombres
            estudiante.apellidos_est_ter = apellidos
            estudiante.cedula_est_ter = cedula
            estudiante.genero_est_ter = genero
            estudiante.nivel_escolar_est_ter = nivel
            estudiante.estado_est_ter = estado
            estudiante.save()

            messages.success(request, "Estudiante de Tercero actualizado exitosamente.")
            return redirect('lista_estudiantes_tercero')

    return render(request, 'Administrador/Estudiantes/Tercero/editar_estudiante_tercero.html', {
        'estudiante': estudiante,
        'error_cedula': error_cedula
    })

# ELIMINAR TERCERO
def eliminar_estudiante_tercero(request, id):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')

    estudiante = get_object_or_404(Estudiante_Tercero, id=id)
    estudiante.delete()
    messages.success(request, "Estudiante de Tercero eliminado correctamente.")
    return redirect('lista_estudiantes_tercero')




#----------------------PROFESORES------------
def lista_profesores(request):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')
    
    profesores = Profesor.objects.all()
    return render(request, 'Administrador/Profesores/lista_profesores.html', {'profesores': profesores})




#----------------------SELECCION DE EVALUACION------------
def seleccion_evaluacion(request):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')
    
    evaluaciones = Profesor.objects.all()
    return render(request, 'Administrador/Evaluaciones/seleccion_evaluacion.html', {'evaluaciones': evaluaciones})

#--------EVALUACION CUARTO------------------------
from django.utils import timezone

TIPOS_APRENDIZAJE = [
    ("objetos", "Objetos"),
    ("meses", "Meses"),
    ("numeros", "Números"),
    ("dias", "Días"),
    ("saludos", "Saludos"),
    ("animales", "Animales"),
    ("colores", "Colores"),
    ("cuerpo_humano", "Cuerpo Humano"),
    ("parentesco", "Parentesco"),
    ("naturaleza", "Elementos de la Naturaleza"),
]

# AGREGAR EVALUACION CUARTO
def agregar_evaluacion_cuarto(request):
    error_titulo = None
    max_evaluaciones = 3
    total_evaluaciones = Evaluacion_Cuarto.objects.count()

    if total_evaluaciones >= max_evaluaciones:
        messages.warning(request, "Ya has alcanzado el límite de 3 evaluaciones para Cuarto.")
        return redirect("lista_evaluaciones_cuarto")

    if request.method == "POST":
        titulo = request.POST.get("titulo_eva_cua", "").strip()
        descripcion = request.POST.get("descripcion_eva_cua", "")
        nivel_escolar = request.POST.get("nivel_escolar_eva_cua", "").strip()
        estado = request.POST.get("estado_eva_cua") == "on"
        tipos = request.POST.getlist("tipo_aprendizaje_eva_cua")

        if Evaluacion_Cuarto.objects.filter(titulo_eva_cua__iexact=titulo).exists():
            error_titulo = f'El título "{titulo}" ya está registrado.'
        else:
            Evaluacion_Cuarto.objects.create(
                titulo_eva_cua=titulo,
                descripcion_eva_cua=descripcion,
                nivel_escolar_eva_cua=nivel_escolar,
                estado_eva_cua=estado,
                tipo_aprendizaje_eva_cua=",".join(tipos),
                fecha_creacion_eva_cua=timezone.now()
            )
            messages.success(request, "Evaluación agregada exitosamente.")
            return redirect("lista_evaluaciones_cuarto")

    return render(request, "Administrador/Evaluaciones/Cuarto/agregar_evaluacion_cuarto.html", {
        "tipos_aprendizaje": TIPOS_APRENDIZAJE,
        "error_titulo": error_titulo
    })

# LISTAR EVALUACIONES CUARTO
def lista_evaluaciones_cuarto(request):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')

    evaluaciones = Evaluacion_Cuarto.objects.all()
    for eva in evaluaciones:
        eva.tipos_lista = [t.strip() for t in eva.tipo_aprendizaje_eva_cua.split(",")] if eva.tipo_aprendizaje_eva_cua else []

    total_evaluaciones = evaluaciones.count()

    return render(request, 'Administrador/Evaluaciones/Cuarto/lista_evaluacion_cuarto.html', {
        'evaluaciones': evaluaciones,
        'total_evaluaciones': total_evaluaciones
    })


# EDITAR EVALUACION CUARTO
def editar_evaluacion_cuarto(request, id):
    evaluacion = get_object_or_404(Evaluacion_Cuarto, id=id)
    error_titulo = None

    if request.method == "POST":
        titulo = request.POST.get("titulo_eva_cua", "").strip()
        descripcion = request.POST.get("descripcion_eva_cua", "")
        nivel_escolar = request.POST.get("nivel_escolar_eva_cua", "").strip()
        estado = request.POST.get("estado_eva_cua") == "on"
        tipos = request.POST.getlist("tipo_aprendizaje_eva_cua")

        if Evaluacion_Cuarto.objects.filter(titulo_eva_cua__iexact=titulo).exclude(id=evaluacion.id).exists():
            error_titulo = f'El título "{titulo}" ya está registrado.'
        else:
            evaluacion.titulo_eva_cua = titulo
            evaluacion.descripcion_eva_cua = descripcion
            evaluacion.nivel_escolar_eva_cua = nivel_escolar
            evaluacion.estado_eva_cua = estado
            evaluacion.tipo_aprendizaje_eva_cua = ",".join(tipos)
            evaluacion.save()
            messages.success(request, "Evaluación actualizada exitosamente.")
            return redirect("lista_evaluaciones_cuarto")

    evaluacion.tipos_lista = [t.strip() for t in evaluacion.tipo_aprendizaje_eva_cua.split(",")] if evaluacion.tipo_aprendizaje_eva_cua else []

    return render(request, "Administrador/Evaluaciones/Cuarto/editar_evaluacion_cuarto.html", {
        "evaluacion": evaluacion,
        "tipos_aprendizaje": TIPOS_APRENDIZAJE,
        "error_titulo": error_titulo
    })


# ELIMINAR EVALUACION CUARTO
def eliminar_evaluacion_cuarto(request, id):
    evaluacion = get_object_or_404(Evaluacion_Cuarto, id=id)
    evaluacion.delete()
    messages.success(request, "Evaluación eliminada correctamente.")
    return redirect("lista_evaluaciones_cuarto")


#---------------EVALUACION TERCERO-------------------
from django.utils import timezone

TIPOS_APRENDIZAJE = [
    ("objetos", "Objetos"),
    ("meses", "Meses"),
    ("numeros", "Números"),
    ("dias", "Días"),
    ("saludos", "Saludos"),
    ("animales", "Animales"),
    ("colores", "Colores"),
    ("cuerpo_humano", "Cuerpo Humano"),
    ("parentesco", "Parentesco"),
    ("naturaleza", "Elementos de la Naturaleza"),
]

def agregar_evaluacion_tercero(request):
    error_titulo = None
    max_evaluaciones = 3
    total_evaluaciones = Evaluacion_Tercero.objects.count()

    if total_evaluaciones >= max_evaluaciones:
        messages.warning(request, "Ya has alcanzado el límite de 3 evaluaciones para Tercero.")
        return redirect("lista_evaluaciones_tercero")

    if request.method == "POST":
        titulo = request.POST.get("titulo_eva_ter", "").strip()
        descripcion = request.POST.get("descripcion_eva_ter", "")
        nivel_escolar = request.POST.get("nivel_escolar_eva_ter", "").strip()
        estado = request.POST.get("estado_eva_ter") == "on"
        tipos = request.POST.getlist("tipo_aprendizaje_eva_ter")

        if Evaluacion_Tercero.objects.filter(titulo_eva_ter__iexact=titulo).exists():
            error_titulo = f'El título "{titulo}" ya está registrado.'
        else:
            Evaluacion_Tercero.objects.create(
                titulo_eva_ter=titulo,
                descripcion_eva_ter=descripcion,
                nivel_escolar_eva_ter=nivel_escolar,
                estado_eva_ter=estado,
                tipo_aprendizaje_eva_ter=",".join(tipos),
            )
            messages.success(request, "Evaluación agregada exitosamente.")
            return redirect("lista_evaluaciones_tercero")

    return render(request, "Administrador/Evaluaciones/Tercero/agregar_evaluacion_tercero.html", {
        "tipos_aprendizaje": TIPOS_APRENDIZAJE,
        "error_titulo": error_titulo
    })

# LISTAR
def lista_evaluaciones_tercero(request):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')

    evaluaciones = Evaluacion_Tercero.objects.all()
    for eva in evaluaciones:
        eva.tipos_lista = [t.strip() for t in eva.tipo_aprendizaje_eva_ter.split(",")] if eva.tipo_aprendizaje_eva_ter else []

    total_evaluaciones = evaluaciones.count()

    return render(request, 'Administrador/Evaluaciones/Tercero/lista_evaluacion_tercero.html', {
        'evaluaciones': evaluaciones,
        'total_evaluaciones': total_evaluaciones
    })

# EDITAR
def editar_evaluacion_tercero(request, id):
    evaluacion = get_object_or_404(Evaluacion_Tercero, id=id)
    error_titulo = None

    if request.method == "POST":
        titulo = request.POST.get("titulo_eva_ter", "").strip()
        descripcion = request.POST.get("descripcion_eva_ter", "")
        nivel_escolar = request.POST.get("nivel_escolar_eva_ter", "").strip()
        estado = request.POST.get("estado_eva_ter") == "on"
        tipos = request.POST.getlist("tipo_aprendizaje_eva_ter")

        if Evaluacion_Tercero.objects.filter(titulo_eva_ter__iexact=titulo).exclude(id=evaluacion.id).exists():
            error_titulo = f'El título "{titulo}" ya está registrado.'
        else:
            evaluacion.titulo_eva_ter = titulo
            evaluacion.descripcion_eva_ter = descripcion
            evaluacion.nivel_escolar_eva_ter = nivel_escolar
            evaluacion.estado_eva_ter = estado
            evaluacion.tipo_aprendizaje_eva_ter = ",".join(tipos)
            evaluacion.save()
            messages.success(request, "Evaluación actualizada exitosamente.")
            return redirect("lista_evaluaciones_tercero")

    evaluacion.tipos_lista = [t.strip() for t in evaluacion.tipo_aprendizaje_eva_ter.split(",")] if evaluacion.tipo_aprendizaje_eva_ter else []

    return render(request, "Administrador/Evaluaciones/Tercero/editar_evaluacion_tercero.html", {
        "evaluacion": evaluacion,
        "tipos_aprendizaje": TIPOS_APRENDIZAJE,
        "error_titulo": error_titulo
    })

# ELIMINAR
def eliminar_evaluacion_tercero(request, id):
    evaluacion = get_object_or_404(Evaluacion_Tercero, id=id)
    evaluacion.delete()
    messages.success(request, "Evaluación eliminada correctamente.")
    return redirect("lista_evaluaciones_tercero")



def seleccion_calificaiones(request):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')
    
    calificaciones = Profesor.objects.all()
    return render(request, 'Administrador/Calificaciones/seleccion_calificaciones.html', {'calificaciones': calificaciones})




# ---------------------------------CALIFICACIONES---------------------
from django.db.models import Max

def lista_calificaciones_cuarto(request):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')

    evaluaciones = Evaluacion_Cuarto.objects.all().order_by('id')
    calificaciones = Resultado_Evaluacion_Cuarto.objects.select_related('fk_estudiante_cua', 'fk_evaluacion_cua').all()

    estudiantes_ids = set(calificaciones.values_list('fk_estudiante_cua__id', flat=True))

    estudiantes = []
    for est_id in estudiantes_ids:
        estudiante = calificaciones.filter(fk_estudiante_cua=est_id).first().fk_estudiante_cua
        estudiantes.append(estudiante)

    notas_por_estudiante = {}
    for cal in calificaciones:
        est_id = cal.fk_estudiante_cua.id
        eva_id = cal.fk_evaluacion_cua.id
        if est_id not in notas_por_estudiante:
            notas_por_estudiante[est_id] = {}
        notas_por_estudiante[est_id][eva_id] = float(cal.nota_res_cua)

    promedios = {}
    total_evaluaciones = evaluaciones.count()
    for est_id in estudiantes_ids:
        notas = notas_por_estudiante.get(est_id, {})
        suma_notas = sum(notas.get(eva.id, 0) for eva in evaluaciones)
        promedios[est_id] = (suma_notas / total_evaluaciones) if total_evaluaciones > 0 else None

    fechas_ultimo_registro = {}
    for est_id in estudiantes_ids:
        ultima_fecha = calificaciones.filter(fk_estudiante_cua=est_id).aggregate(Max('fecha_res_cua'))['fecha_res_cua__max']
        fechas_ultimo_registro[est_id] = ultima_fecha

    context = {
        'evaluaciones': evaluaciones,
        'estudiantes': estudiantes,
        'notas_por_estudiante': notas_por_estudiante,
        'promedios': promedios,
        'fechas_ultimo_registro': fechas_ultimo_registro,
    }
    return render(request, 'Administrador/Calificaciones/lista_calificaciones_cuarto.html', context)


def lista_calificaciones_tercero(request):
    if not request.session.get('profesor_id'):
        return redirect('login_profesor')

    evaluaciones = Evaluacion_Tercero.objects.all().order_by('id')
    calificaciones = Resultado_Evaluacion_Tercero.objects.select_related('fk_estudiante_ter', 'fk_evaluacion_ter').all()

    estudiantes_ids = set(calificaciones.values_list('fk_estudiante_ter__id', flat=True))

    estudiantes = []
    for est_id in estudiantes_ids:
        estudiante = calificaciones.filter(fk_estudiante_ter=est_id).first().fk_estudiante_ter
        estudiantes.append(estudiante)

    notas_por_estudiante = {}
    for cal in calificaciones:
        est_id = cal.fk_estudiante_ter.id
        eva_id = cal.fk_evaluacion_ter.id
        if est_id not in notas_por_estudiante:
            notas_por_estudiante[est_id] = {}
        notas_por_estudiante[est_id][eva_id] = float(cal.nota_res_ter)

    promedios = {}
    total_evaluaciones = evaluaciones.count()
    for est_id in estudiantes_ids:
        notas = notas_por_estudiante.get(est_id, {})
        suma_notas = sum(notas.get(eva.id, 0) for eva in evaluaciones)
        promedios[est_id] = (suma_notas / total_evaluaciones) if total_evaluaciones > 0 else None

    fechas_ultimo_registro = {}
    for est_id in estudiantes_ids:
        ultima_fecha = calificaciones.filter(fk_estudiante_ter=est_id).aggregate(Max('fecha_res_ter'))['fecha_res_ter__max']
        fechas_ultimo_registro[est_id] = ultima_fecha

    context = {
        'evaluaciones': evaluaciones,
        'estudiantes': estudiantes,
        'notas_por_estudiante': notas_por_estudiante,
        'promedios': promedios,
        'fechas_ultimo_registro': fechas_ultimo_registro,
    }
    return render(request, 'Administrador/Calificaciones/lista_calificaciones_tercero.html', context)

# -------------------REPORTE EN PDF----------------------------
# TERCERO
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from io import BytesIO

def generar_pdf_calificaciones_tercero(request):
    estudiantes = Estudiante_Tercero.objects.all()
    evaluaciones = Evaluacion_Tercero.objects.all()

    notas_por_estudiante = {}
    promedios = {}
    fechas_ultimo_registro = {}

    total_evaluaciones = evaluaciones.count()

    for est in estudiantes:
        notas_est = {}
        suma = 0
        ultima_fecha = None

        for eva in evaluaciones:
            nota_obj = Resultado_Evaluacion_Tercero.objects.filter(
                fk_estudiante_ter=est,
                fk_evaluacion_ter=eva
            ).last()

            if nota_obj:
                nota_valor = float(nota_obj.nota_res_ter)
                notas_est[eva.id] = nota_valor
                suma += nota_valor
                if not ultima_fecha or nota_obj.fecha_res_ter > ultima_fecha:
                    ultima_fecha = nota_obj.fecha_res_ter
            else:
                notas_est[eva.id] = 0.0

        notas_por_estudiante[est.id] = notas_est
        promedios[est.id] = (suma / total_evaluaciones) if total_evaluaciones > 0 else 0
        fechas_ultimo_registro[est.id] = ultima_fecha

    template = get_template('Administrador/Calificaciones/Reportes/reporte_calificaciones_tercero.html')
    html = template.render({
        'estudiantes': estudiantes,
        'evaluaciones': evaluaciones,
        'notas_por_estudiante': notas_por_estudiante,
        'promedios': promedios,
        'fechas_ultimo_registro': fechas_ultimo_registro,
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="calificaciones_tercero.pdf"'

    pisa_status = pisa.CreatePDF(BytesIO(html.encode('utf-8')), dest=response)

    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)

    return response

# CUARTO
def generar_pdf_calificaciones_cuarto(request):
    estudiantes = Estudiante_Cuarto.objects.all()
    evaluaciones = Evaluacion_Cuarto.objects.all()

    notas_por_estudiante = {}
    promedios = {}
    fechas_ultimo_registro = {}

    total_evaluaciones = evaluaciones.count()

    for est in estudiantes:
        notas_est = {}
        suma = 0
        ultima_fecha = None

        for eva in evaluaciones:
            nota_obj = Resultado_Evaluacion_Cuarto.objects.filter(
                fk_estudiante_cua=est,
                fk_evaluacion_cua=eva
            ).last()

            if nota_obj:
                nota_valor = float(nota_obj.nota_res_cua)
                notas_est[eva.id] = nota_valor
                suma += nota_valor
                if not ultima_fecha or nota_obj.fecha_res_cua > ultima_fecha:
                    ultima_fecha = nota_obj.fecha_res_cua
            else:
                notas_est[eva.id] = 0.0

        notas_por_estudiante[est.id] = notas_est
        promedios[est.id] = (suma / total_evaluaciones) if total_evaluaciones > 0 else 0
        fechas_ultimo_registro[est.id] = ultima_fecha

    # Renderizar plantilla
    template = get_template('Administrador/Calificaciones/Reportes/reporte_calificaciones_cuarto.html')
    html = template.render({
        'estudiantes': estudiantes,
        'evaluaciones': evaluaciones,
        'notas_por_estudiante': notas_por_estudiante,
        'promedios': promedios,
        'fechas_ultimo_registro': fechas_ultimo_registro,
    })

    # Generar PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="calificaciones_cuarto.pdf"'
    pisa_status = pisa.CreatePDF(BytesIO(html.encode('utf-8')), dest=response)

    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)

    return response

############################### LADO DEL USUARIO #################################

# LOGIN ESTUDIANTE
def login_estudiante(request):
    if request.method == 'POST':
        nombres = request.POST.get('nombres').strip()
        apellidos = request.POST.get('apellidos').strip()
        cedula = request.POST.get('cedula').strip()

        # Buscar en estudiantes de tercero
        estudiante_ter = Estudiante_Tercero.objects.filter(
            nombres_est_ter__iexact=nombres,
            apellidos_est_ter__iexact=apellidos,
            cedula_est_ter=cedula
        ).first()

        if estudiante_ter:
            request.session['estudiante_id'] = estudiante_ter.id
            request.session['nivel'] = 'tercero'
            return redirect('ver_evaluacion_tercero')

        # Buscar en estudiantes de cuarto
        estudiante_cua = Estudiante_Cuarto.objects.filter(
            nombres_est_cua__iexact=nombres,
            apellidos_est_cua__iexact=apellidos,
            cedula_est_cua=cedula
        ).first()

        if estudiante_cua:
            request.session['estudiante_id'] = estudiante_cua.id
            request.session['nivel'] = 'cuarto'
            return redirect('ver_evaluacion_cuarto')

        messages.error(request, 'Datos incorrectos. Verifica tu cédula, nombres o apellidos.')

    return render(request, 'Login/login_estudiante.html')

def logout_estudiante(request):
    request.session.flush()
    return redirect('login_estudiante')

# --------------VER TIPO EVALUACION -----------------
def ver_evaluacion_tercero(request):
    estudiante_id = request.session.get('estudiante_id')
    if not estudiante_id or request.session.get('nivel') != 'tercero':
        return redirect('login_estudiante')

    estudiante = Estudiante_Tercero.objects.filter(id=estudiante_id).first()
    if not estudiante:
        return redirect('login_estudiante')

    # Corrección aquí
    evaluaciones = Evaluacion_Tercero.objects.filter(estado_eva_ter=True)

    return render(request, 'Evaluacion/ver_evaluacion_tercero.html', {
        'estudiante': estudiante,
        'evaluaciones': evaluaciones
    })


def ver_evaluacion_cuarto(request):
    estudiante_id = request.session.get('estudiante_id')
    if not estudiante_id or request.session.get('nivel') != 'cuarto':
        return redirect('login_estudiante')

    estudiante = Estudiante_Cuarto.objects.filter(id=estudiante_id).first()
    if not estudiante:
        return redirect('login_estudiante')

    # Corrección aquí
    evaluaciones = Evaluacion_Cuarto.objects.filter(estado_eva_cua=True)

    return render(request, 'Evaluacion/ver_evaluacion_cuarto.html', {
        'estudiante': estudiante,
        'evaluaciones': evaluaciones
    })

#--------------------VER EVALUACION 10 PREGUNTAS-------------------------

def mostrar_evaluacion_tercero(request, evaluacion_id):
    estudiante_id = request.session.get('estudiante_id')
    if not estudiante_id:
        return redirect('login_estudiante')

    estudiante = Estudiante_Tercero.objects.filter(id=estudiante_id).first()
    if not estudiante:
        return redirect('login_estudiante')

    evaluacion = get_object_or_404(Evaluacion_Tercero, id=evaluacion_id)
    tipos = evaluacion.tipo_aprendizaje_eva_ter.split(',')

    if request.method == 'POST':
        nota = request.POST.get('nota')
        try:
            nota_decimal = float(nota)
        except:
            nota_decimal = 0.0

        Resultado_Evaluacion_Tercero.objects.create(
            fk_estudiante_ter=estudiante,
            fk_evaluacion_ter=evaluacion,
            nota_res_ter=nota_decimal,
            fecha_res_ter=timezone.now()
        )


        return render(request, 'Evaluacion/mostrar_evaluacion_tercero.html', {
            'evaluacion': evaluacion,
            'mostrar_resultado': True,
            'puntaje': nota_decimal,
        })

    # Preparar preguntas
    modelos = {
        'objetos': Aprender_Objetos,
        'meses': Aprender_Meses,
        'numeros': Aprender_Numeros,
        'dias': Aprender_Dias,
        'saludos': Aprender_Saludos,
        'animales': Aprender_Animales,
        'colores': Aprender_Colores,
        'cuerpo_humano': Aprender_Cuerpo_Humano,
        'parentesco': Aprender_Parentesco,
        'elemento_naturaleza': Aprender_Elemento_Naturaleza,
    }

    preguntas_unificadas = []

    for tipo in tipos:
        modelo = modelos.get(tipo.strip())
        if modelo:
            datos = list(modelo.objects.all())
            for d in datos:
                base = tipo[:3]
                correcta = getattr(d, f'palabra_{base}', str(d))
                imagen = getattr(d, f'imagen_{base}', None)
                otras_opciones = random.sample([getattr(x, f'palabra_{base}', str(x)) for x in datos if x != d], k=2) if len(datos) > 2 else []
                opciones = [{'texto': o, 'es_correcta': False} for o in otras_opciones]
                opciones.append({'texto': correcta, 'es_correcta': True})
                random.shuffle(opciones)

                preguntas_unificadas.append({
                    'palabra_correcta': correcta,
                    'imagen': imagen,
                    'opciones': opciones,
                })

    preguntas_random = random.sample(preguntas_unificadas, min(10, len(preguntas_unificadas)))

    return render(request, 'Evaluacion/mostrar_evaluacion_tercero.html', {
        'evaluacion': evaluacion,
        'preguntas': preguntas_random,
        'mostrar_resultado': False,
    })


# EVALUACION CUARTO
def mostrar_evaluacion_cuarto(request, evaluacion_id):
    estudiante_id = request.session.get('estudiante_id')
    if not estudiante_id:
        return redirect('login_estudiante')

    estudiante = Estudiante_Cuarto.objects.filter(id=estudiante_id).first()
    if not estudiante:
        return redirect('login_estudiante')

    evaluacion = get_object_or_404(Evaluacion_Cuarto, id=evaluacion_id)
    tipos = evaluacion.tipo_aprendizaje_eva_cua.split(',')

    if request.method == 'POST':
        nota = request.POST.get('nota')
        try:
            nota_decimal = float(nota)
        except:
            nota_decimal = 0.0

        Resultado_Evaluacion_Cuarto.objects.create(
            fk_estudiante_cua=estudiante,
            fk_evaluacion_cua=evaluacion,
            nota_res_cua=nota_decimal,
            fecha_res_cua=timezone.now()
        )


        return render(request, 'Evaluacion/mostrar_evaluacion_cuarto.html', {
            'evaluacion': evaluacion,
            'mostrar_resultado': True,
            'puntaje': nota_decimal,
        })

    modelos = {
        'objetos': Aprender_Objetos,
        'meses': Aprender_Meses,
        'numeros': Aprender_Numeros,
        'dias': Aprender_Dias,
        'saludos': Aprender_Saludos,
        'animales': Aprender_Animales,
        'colores': Aprender_Colores,
        'cuerpo_humano': Aprender_Cuerpo_Humano,
        'parentesco': Aprender_Parentesco,
        'elemento_naturaleza': Aprender_Elemento_Naturaleza,
    }

    preguntas_unificadas = []

    for tipo in tipos:
        modelo = modelos.get(tipo.strip())
        if modelo:
            datos = list(modelo.objects.all())
            for d in datos:
                base = tipo[:3]
                correcta = getattr(d, f'palabra_{base}', str(d))
                imagen = getattr(d, f'imagen_{base}', None)
                otras_opciones = random.sample([getattr(x, f'palabra_{base}', str(x)) for x in datos if x != d], k=2) if len(datos) > 2 else []
                opciones = [{'texto': o, 'es_correcta': False} for o in otras_opciones]
                opciones.append({'texto': correcta, 'es_correcta': True})
                random.shuffle(opciones)

                preguntas_unificadas.append({
                    'palabra_correcta': correcta,
                    'imagen': imagen,
                    'opciones': opciones,
                })

    preguntas_random = random.sample(preguntas_unificadas, min(10, len(preguntas_unificadas)))

    return render(request, 'Evaluacion/mostrar_evaluacion_cuarto.html', {
        'evaluacion': evaluacion,
        'preguntas': preguntas_random,
        'mostrar_resultado': False,
    })




#-------------------------------ARENDER  ---------------------
# MESES
def ver_meses(request):
    if not request.session.get('estudiante_nombre') or not request.session.get('estudiante_apellido'):
        return redirect('login_estudiante_aprender')

    meses = Aprender_Meses.objects.all()
    return render(request, 'Aprender/meses.html', {'meses': meses})

# OBJETOS
def ver_objetos(request):
    if not request.session.get('estudiante_nombre') or not request.session.get('estudiante_apellido'):
        return redirect('login_estudiante_aprender')
    
    objetos = Aprender_Objetos.objects.all()
    return render(request, 'Aprender/objetos.html', {'objetos': objetos})

# NUMEROS
def ver_numeros(request):
    if not request.session.get('estudiante_nombre') or not request.session.get('estudiante_apellido'):
        return redirect('login_estudiante_aprender')
    
    numeros = Aprender_Numeros.objects.all()
    return render(request, 'Aprender/numeros.html', {'numeros': numeros})

# DIAS DE LA SEMANA
def ver_dias(request):
    if not request.session.get('estudiante_nombre') or not request.session.get('estudiante_apellido'):
        return redirect('login_estudiante_aprender')
    
    dias = Aprender_Dias.objects.all()
    return render(request, 'Aprender/dias.html', {'dias': dias})

# ANIMALES
def ver_animales(request):
    if not request.session.get('estudiante_nombre') or not request.session.get('estudiante_apellido'):
        return redirect('login_estudiante_aprender')
    
    animales = Aprender_Animales.objects.all()
    return render(request, 'Aprender/animales.html', {'animales': animales})

# SALUDOS
def ver_saludos(request):
    if not request.session.get('estudiante_nombre') or not request.session.get('estudiante_apellido'):
        return redirect('login_estudiante_aprender')
    
    saludos = Aprender_Saludos.objects.all()
    return render(request, 'Aprender/saludos.html', {'saludos': saludos})

# COLORES
def ver_colores(request):
    if not request.session.get('estudiante_nombre') or not request.session.get('estudiante_apellido'):
        return redirect('login_estudiante_aprender')

    colores = Aprender_Colores.objects.all()
    return render(request, 'Aprender/colores.html', {'colores': colores})

# CUERPO HUMANO
def ver_cuerpo_humano(request):
    if not request.session.get('estudiante_nombre') or not request.session.get('estudiante_apellido'):
        return redirect('login_estudiante_aprender')
    
    cuerpo_humano = Aprender_Cuerpo_Humano.objects.all()
    return render(request, 'Aprender/cuerpo_humano.html', {'cuerpo_humano': cuerpo_humano})

# PARENTESCO
def ver_parentesco(request):
    if not request.session.get('estudiante_nombre') or not request.session.get('estudiante_apellido'):
        return redirect('login_estudiante_aprender')
    
    parentescos = Aprender_Parentesco.objects.all()
    return render(request, 'Aprender/parentesco.html', {'parentescos': parentescos})

# ELEMENTO NATURALEZA
def ver_elemento_naturaleza(request):
    if not request.session.get('estudiante_nombre') or not request.session.get('estudiante_apellido'):
        return redirect('login_estudiante_aprender')
    
    elemento_naturaleza = Aprender_Elemento_Naturaleza.objects.all()
    return render(request, 'Aprender/elemento_naturaleza.html', {'elemento_naturaleza': elemento_naturaleza})

#-----------------------JUGAR ------------------------------
# MESES
def jugar_meses(request):
    if not request.session.get('estudiante_nombre') or not request.session.get('estudiante_apellido'):
        return redirect('login_estudiante_aprender')
    
    meses = Aprender_Meses.objects.all()
    return render(request, 'Juegos/jugar_meses.html', {'meses': meses})

# OBJETOS
import random
def jugar_objetos(request):
    if not request.session.get('estudiante_nombre') or not request.session.get('estudiante_apellido'):
        return redirect('login_estudiante_aprender')
    
    objetos = list(Aprender_Objetos.objects.all())
    random.shuffle(objetos)
    objetos = objetos[:10]  # Selecciona 10 aleatorios

    return render(request, 'Juegos/jugar_objetos.html', {'objetos': objetos})

# NUMEROS
def jugar_numeros(request):
    if not request.session.get('estudiante_nombre') or not request.session.get('estudiante_apellido'):
        return redirect('login_estudiante_aprender')
    
    numeros = Aprender_Numeros.objects.all()
    return render(request, 'Juegos/jugar_numeros.html', {'numeros': numeros})

# DIAS DE LA SEMANA
def jugar_dias(request):
    if not request.session.get('estudiante_nombre') or not request.session.get('estudiante_apellido'):
        return redirect('login_estudiante_aprender')
    
    dias = Aprender_Dias.objects.all()
    return render(request, 'Juegos/jugar_dias.html', {'dias': dias})

# ANIMALES
def jugar_animales(request):
    if not request.session.get('estudiante_nombre') or not request.session.get('estudiante_apellido'):
        return redirect('login_estudiante_aprender')
    
    todos = list(Aprender_Animales.objects.all())
    seleccionados = random.sample(todos, min(15, len(todos)))  # 15 al azar o menos si hay pocos
    return render(request, 'Juegos/jugar_animales.html', {'animales': seleccionados})

# COLORES
def jugar_colores(request):
    if not request.session.get('estudiante_nombre') or not request.session.get('estudiante_apellido'):
        return redirect('login_estudiante_aprender')
    
    colores = Aprender_Colores.objects.all()
    return render(request, 'Juegos/jugar_colores.html', {'colores': colores})

# SALUDOS
def jugar_saludos(request):
    if not request.session.get('estudiante_nombre') or not request.session.get('estudiante_apellido'):
        return redirect('login_estudiante_aprender')
    
    saludos = list(Aprender_Saludos.objects.all())  
    random.shuffle(saludos) 
    return render(request, 'Juegos/jugar_saludos.html', {'saludos': saludos})

# CUERPO HUMANO
def jugar_cuerpo_humano(request):
    if not request.session.get('estudiante_nombre') or not request.session.get('estudiante_apellido'):
        return redirect('login_estudiante_aprender')
    
    cuerpo_humano = Aprender_Cuerpo_Humano.objects.all()
    return render(request, 'Juegos/jugar_cuerpo_humano.html', {'cuerpo_humano': cuerpo_humano})

# PARENTESCO
def jugar_parentesco(request):
    if not request.session.get('estudiante_nombre') or not request.session.get('estudiante_apellido'):
        return redirect('login_estudiante_aprender')
    
    parentescos = list(Aprender_Parentesco.objects.all())
    random.shuffle(parentescos)
    return render(request, 'Juegos/jugar_parentesco.html', {'parentescos': parentescos})

# ELEMENTOS NATURALEZA
def jugar_elementos_naturaleza(request):
    if not request.session.get('estudiante_nombre') or not request.session.get('estudiante_apellido'):
        return redirect('login_estudiante_aprender')
    
    elementos = Aprender_Elemento_Naturaleza.objects.all()
    return render(request, 'Juegos/jugar_elementos_naturaleza.html', {'elementos': elementos})


#--------------------------APRENDER LOGIN ESTUDIANTES-------------------------------
def login_estudiante_aprender(request):
    if request.method == 'POST':
        nombres = request.POST.get('nombres').strip()
        apellidos = request.POST.get('apellidos').strip()
        cedula = request.POST.get('cedula').strip()

        # Buscar en Estudiante_Cuarto
        try:
            estudiante = Estudiante_Cuarto.objects.get(
                nombres_est_cua=nombres,
                apellidos_est_cua=apellidos,
                cedula_est_cua=cedula
            )
            if estudiante.estado_est_cua.upper() != 'ACTIVO':
                messages.error(request, 'Tu cuenta está inactiva. Contacta al docente.')
            else:
                request.session['estudiante_nombre'] = estudiante.nombres_est_cua
                request.session['estudiante_apellido'] = estudiante.apellidos_est_cua
                return redirect('aprender')
        except Estudiante_Cuarto.DoesNotExist:
            pass

        # Buscar en Estudiante_Tercero
        try:
            estudiante = Estudiante_Tercero.objects.get(
                nombres_est_ter=nombres,
                apellidos_est_ter=apellidos,
                cedula_est_ter=cedula
            )
            if estudiante.estado_est_ter.upper() != 'ACTIVO':
                messages.error(request, 'Tu cuenta está inactiva. Contacta al docente.')
            else:
                request.session['estudiante_nombre'] = estudiante.nombres_est_ter
                request.session['estudiante_apellido'] = estudiante.apellidos_est_ter
                return redirect('aprender')
        except Estudiante_Tercero.DoesNotExist:
            messages.error(request, 'Datos incorrectos. Intenta nuevamente.')

    return render(request, 'Login/login_EstudianteAprender.html')


# PAGUNA INICIO ALUMNO AL APRENDIZAJE
def aprender(request):
    if not request.session.get('estudiante_nombre') or not request.session.get('estudiante_apellido'):
        return redirect('login_estudiante_aprender')

    aprender_items = Aprender_Objetos.objects.all()
    nombre_completo = f"{request.session['estudiante_nombre']} {request.session['estudiante_apellido']}"
    return render(request, 'Aprender/aprender.html', {
        'aprender_items': aprender_items,
        'nombre_completo': nombre_completo
    })

# SALIR
def logout_estudiante_aprender(request):
    request.session.flush()
    return redirect('login_estudiante_aprender')
#---------------------HISTORIA--------------------
def historia(request):
    return render(request, 'Historia/historia.html')


#----------------------RECUPERAR CONTRASEÑA---------------------
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib import messages
from .models import Profesor

def recuperar_contrasena(request):
    if request.method == 'POST':
        cedula = request.POST.get('cedula').strip()
        email = request.POST.get('email').strip()

        try:
            profesor = Profesor.objects.get(cedula=cedula, email=email)

            # Cargar plantilla HTML del correo
            mensaje = render_to_string('correos/recuperar_contrasena.html', {
                'nombre': profesor.nombres,
                'usuario': profesor.usuario,
                'contrasena': profesor.contrasena,
            })

            send_mail(
                '🔐 Recuperación de Contraseña',
                '',
                settings.EMAIL_HOST_USER,
                [email],
                html_message=mensaje,
                fail_silently=False,
            )

            messages.success(request, 'La contraseña ha sido enviada a tu correo electrónico.')
            return redirect('login_profesor')

        except Profesor.DoesNotExist:
            messages.error(request, 'No se encontró un profesor con esa cédula y correo.')

    return render(request, 'Login/recuperar_contrasena.html')
