from django.urls import path, include

from . import views 
urlpatterns = [
    path('',views.inicio, name='inicio'),

    ########################### LADO DEL ADMINISTRADOR ##############################

    #---------------PROFESORES----------------
    path('superadmin/profesor/', views.lista_profesor, name='lista_profesor'),
    path('ajax/cambiar_estado_profesor/', views.ajax_cambiar_estado_profesor, name='ajax_cambiar_estado_profesor'),
    path('superadmin/profesor/agregar/', views.agregar_profesor, name='agregar_profesor'),
    path('profesor/editar/<int:id>/', views.editar_profesor, name='editar_profesor'),
    path('profesor/eliminar/<int:id>/', views.eliminar_profesor, name='eliminar_profesor'),


    # APRENDER

    #-----------------------OBJETOS--------------------
    path('objetos/', views.lista_objetos, name='lista_objetos'),
    path('objetos/agregar/', views.agregar_objeto, name='agregar_objeto'),
    path('objetos/editar/<int:id>/', views.editar_objeto, name='editar_objeto'),
    path('objeto/eliminar/<int:id>/', views.eliminar_objeto, name='eliminar_objeto'),
    path('reporte_objetos/', views.generar_pdf_objetos, name='reporte_objetos'),

    #-------------------------MESES------------------------
    path('meses/', views.lista_meses, name='lista_meses'),
    path('meses/agregar/', views.agregar_mes, name='agregar_mes'),
    path('mes/editar/<int:id>/', views.editar_mes, name='editar_mes'),
    path('mes/eliminar/<int:id>/', views.eliminar_mes, name='eliminar_mes'),
    path('reporte_meses/', views.generar_pdf_meses, name='reporte_meses'),

    #-------------------------NUMEROS---------------------------
    path('numeros/', views.lista_numeros, name='lista_numeros'),
    path('numeros/agregar/', views.agregar_numero, name='agregar_numero'),
    path('numero/editar/<int:id>/', views.editar_numero, name='editar_numero'),
    path('numero/eliminar/<int:id>/', views.eliminar_numero, name='eliminar_numero'),
    path('reporte_numeros/', views.generar_pdf_numeros, name='reporte_numeros'),

    #-------------------------DIAS-----------------------
    path('dias/', views.lista_dias, name='lista_dias'),
    path('dia/agregar', views.agregar_dia, name='agregar_dia'),
    path('dia/editar/<int:id>/', views.editar_dia, name='editar_dia'),
    path('dia/eliminar/<int:id>/', views.eliminar_dia, name='eliminar_dia'),
    path('reporte_dias/', views.generar_pdf_dias, name='reporte_dias'),


    #--------------------------SALUDOS----------------------
    path('saludos/', views.lista_saludos, name='lista_saludos'),
    path('saludo/agregar', views.agregar_saludo, name='agregar_saludo'),
    path('saludo/editar/<int:id>/', views.editar_saludo, name='editar_saludo'),
    path('saludo/eliminar/<int:id>/', views.eliminar_saludo, name='eliminar_saludo'),
    path('reporte_saludos/', views.generar_pdf_saludos, name='reporte_saludos'),

    #--------------------------ANIMALES-------------------------------
    path('animales/', views.lista_animales, name='lista_animales'),
    path('animal/agregar', views.agregar_animal, name='agregar_animal'),
    path('animales/editar/<int:id>/', views.editar_animal, name='editar_animal'),
    path('animales/eliminar/<int:id>/', views.eliminar_animal, name='eliminar_animal'),
    path('reporte_animales/', views.generar_pdf_animales, name='reporte_animales'),

    #--------------------------COLORES---------------------------
    path('colores/', views.lista_colores, name='lista_colores'),
    path('color/agregar', views.agregar_color, name='agregar_color'),
    path('color/editar/<int:id>/', views.editar_color, name='editar_color'),
    path('color/eliminar/<int:id>/', views.eliminar_color, name='eliminar_color'),
    path('reporte_colores/', views.generar_pdf_colores, name='reporte_colores'),

    #---------------------------CUERPO HUMANO----------------------
    path('cuerpo_humano/', views.lista_cuerpo_humano, name='lista_cuerpo_humano'),
    path('cuerpo_humano/agregar/', views.agregar_cuerpo_humano, name='agregar_cuerpo_humano'),
    path('cuerpo_humano/editar/<int:id>/', views.editar_cuerpo_humano, name='editar_cuerpo_humano'),
    path('cuerpo_humano/eliminar/<int:id>/', views.eliminar_cuerpo_humano, name='eliminar_cuerpo_humano'),
    path('reporte_cuerpo_humano/', views.generar_pdf_cuerpo_humano, name='reporte_cuerpo_humano'),

    #------------------------------PARENTESCO---------------------------------
    path('parentesco/', views.lista_parentesco, name='lista_parentesco'),
    path('parentesco/agregar', views.agregar_parentesco, name='agregar_parentesco'),
    path('parentesco/editar/<int:id>/', views.editar_parentesco, name='editar_parentesco'),
    path('parentesco/eliminar/<int:id>/', views.eliminar_parentesco, name='eliminar_parentesco'),
    path('reporte_parentescos/', views.generar_pdf_parentescos, name='reporte_parentescos'),

    #----------------------------ELEMENTOS NATURALEZA--------------------------
    path('elemento_naturaleza/', views.lista_elemento_naturaleza, name='lista_elemento_naturaleza'),
    path('elemnto_naturaleza/agregar', views.agregar_elemento_naturaleza, name='agregar_elemento_naturaleza'),
    path('elemento_naturaleza/editar/<int:id>/', views.editar_elemento_naturaleza, name='editar_elemento_naturaleza'),
    path('elemento_naturaleza/eliminar/<int:id>/', views.eliminar_elemento_naturaleza, name='eliminar_elemento_naturaleza'),
    path('reporte_elementos/', views.generar_pdf_elementos, name='reporte_elementos'),


    #---------------------------ESTUDIANTES CUARTO-----------------------------
    path('estudiantes_cuarto/', views.lista_estudiantes_cuarto, name='lista_estudiantes_cuarto'),
    path('ajax/cambiar-estado-estudiante-cuarto/', views.ajax_cambiar_estado_estudiante_cuarto, name='ajax_cambiar_estado_estudiante_cuarto'),
    path('estudiante_cuarto/agregar', views.agregar_estudiante_cuarto, name='agregar_estudiante_cuarto'),
    path('estudiante_cuarto/editar/<int:id_est>/', views.editar_estudiante_cuarto, name='editar_estudiante_cuarto'),
    path('estudiante_cuarto/eliminar/<int:id>/', views.eliminar_estudiante_cuarto, name='eliminar_estudiante_cuarto'),

        #---------------------------ESTUDIANTES TERCERO-----------------------------
    path('estudiantes_tercero/', views.lista_estudiantes_tercero, name='lista_estudiantes_tercero'),
    path('ajax/cambiar-estado-estudiante-tercero/', views.ajax_cambiar_estado_estudiante_tercero, name='ajax_cambiar_estado_estudiante_tercero'),
    path('estudiante_tercero/agregar', views.agregar_estudiante_tercero, name='agregar_estudiante_tercero'),
    path('estudiante_tercero/editar/<int:id_est>/', views.editar_estudiante_tercero, name='editar_estudiante_tercero'),
    path('estudiante_tercero/eliminar/<int:id>/', views.eliminar_estudiante_tercero, name='eliminar_estudiante_tercero'),


    #-------------------------PROFESORES-------------------------------------
    path('profesores/', views.lista_profesores, name='lista_profesores'),
    path('profesor/configuracion/', views.configuracion_profesor, name='configuracion_profesor'),

    #----------------------------SELECCION DE EVALUACIONES----------------
    path('evaluacion/seleccion', views.seleccion_evaluacion, name='seleccion_evaluacion'),
    #----------------------------SELECCIOND DE ESTUDIANTES----------------
    path('estudiantes/seleccion', views.seleccion_estudiantes, name='seleccion_estudiantes'),
    #---------------------------SELECCION DE CALIFICACIOES-------------------
    path('calificaiones/seleccion', views.seleccion_calificaiones, name='seleccion_calificaciones'),

    #--------------------------EVALUACIONES CUARTO---------------------------
    path('evaluaciones/cuarto/', views.lista_evaluaciones_cuarto, name='lista_evaluaciones_cuarto'),
    path('ajax/cambiar-estado-evaluacion/', views.ajax_cambiar_estado_evaluacion, name='ajax_cambiar_estado_evaluacion'),
    path('evaluaciones/cuarto/agregar/', views.agregar_evaluacion_cuarto, name='agregar_evaluacion_cuarto'),
    path('evaluaciones/cuarto/editar/<int:id>/', views.editar_evaluacion_cuarto, name='editar_evaluacion_cuarto'),
    path('evaluaciones/cuarto/eliminar/<int:id>/', views.eliminar_evaluacion_cuarto, name='eliminar_evaluacion_cuarto'),

    #-------------------------------EVALUACIONES TERCERO-------------------------------
    path('evaluaciones/tercero/', views.lista_evaluaciones_tercero, name='lista_evaluaciones_tercero'),
    path('ajax/cambiar-estado-evaluacion-cuarto/', views.ajax_cambiar_estado_evaluacion_cuarto, name='ajax_cambiar_estado_evaluacion_cuarto'),
    path('evaluaciones/tercero/agregar/', views.agregar_evaluacion_tercero, name='agregar_evaluacion_tercero'),
    path('evaluaciones/tercero/editar/<int:id>/', views.editar_evaluacion_tercero, name='editar_evaluacion_tercero'),
    path('evaluaciones/tercero/eliminar/<int:id>/', views.eliminar_evaluacion_tercero, name='eliminar_evaluacion_tercero'),


    #-------------------------CALIFICACIONES-----------------------------
    path('calificaciones/cuarto/', views.lista_calificaciones_cuarto, name='lista_calificaciones_cuarto'),
    path('calificaciones/tercero/', views.lista_calificaciones_tercero, name='lista_calificaciones_tercero'),

    #---------------------------DESCARGA PDF----------------------
    path('reporte_pdf_calificaciones_tercero/', views.generar_pdf_calificaciones_tercero, name='reporte_pdf_calificaciones_tercero'),
    path('reporte_pdf_calificaciones_cuarto/', views.generar_pdf_calificaciones_cuarto, name='reporte_pdf_calificaciones_cuarto'),


    ###################### LADO DEL USUSARIO #######################

    # -------------------------------EVALUACION------------------
    path('login_estudiante/', views.login_estudiante, name='login_estudiante'),
    path('logout_estudiante/', views.logout_estudiante, name='logout_estudiante'),
    
    # SELECCION DE EVALUACION
    path('ver_evaluaciones/tercero/', views.ver_evaluacion_tercero, name='ver_evaluacion_tercero'),
    path('ver_evaluaciones/cuarto/', views.ver_evaluacion_cuarto, name='ver_evaluacion_cuarto'),
    # VER EVALUACINES 
    path('evaluacion/tercero/<int:evaluacion_id>/', views.mostrar_evaluacion_tercero, name='mostrar_evaluacion_tercero'),
    path('evaluacion/cuarto/<int:evaluacion_id>/', views.mostrar_evaluacion_cuarto, name='mostrar_evaluacion_cuarto'),


    #---------------------------------APRENDER---------------------------
    path('login-estudiante-aprender/', views.login_estudiante_aprender, name='login_estudiante_aprender'),
    path('aprender/',views.aprender, name='aprender'),
    path('logout_estudiante_aprender/', views.logout_estudiante_aprender, name='logout_estudiante_aprender'),
    
    # APRENDER MESES
    path('modulos/meses/', views.ver_meses, name='ver_meses'),
    # APRENDER OBJETOS
    path('modulos/objetos/', views.ver_objetos, name='ver_objetos'),
    # APRENDER NUMEROS
    path('modulos/numeros/', views.ver_numeros, name='ver_numeros'),
    # APRENDER DIAS
    path('modulos/dias/', views.ver_dias, name='ver_dias'),
    # ANIMALES
    path('modulos/animales/', views.ver_animales, name='ver_animales'),
    # SALUDOS
    path('modulos/saludos/', views.ver_saludos, name='ver_saludos'),
    # COLORES
    path('modulos/colores/', views.ver_colores, name='ver_colores'),
    # CUERPO HUMANO
    path('modulos/cuerpo_humano/', views.ver_cuerpo_humano, name='ver_cuerpo_humano'),
    # PARENTESCO
    path('modulos/parentesco/', views.ver_parentesco, name='ver_parentesco'),
    # ELEMENTO NATURALEZA
    path('modulos/elemento_naturaleza/', views.ver_elemento_naturaleza, name='ver_elemento_naturaleza'),

    #-------------------------------JUGAR----------------------------------
    # MESES
    path('jugar/meses/', views.jugar_meses, name='jugar_meses'),
    # OBJETOS
    path('jugar/objetos/', views.jugar_objetos, name='jugar_objetos'),
    # NUMEROS
    path('jugar/numeros/', views.jugar_numeros, name='jugar_numeros'),
    # DIAS
    path('jugar/dias/', views.jugar_dias, name='jugar_dias'),
    # ANIMALES
    path('jugar/animales/', views.jugar_animales, name='jugar_animales'),
    # COLORES
    path('jugar/colores/', views.jugar_colores, name='jugar_colores'),
    # SALUDOS
    path('jugar/saludos/', views.jugar_saludos, name='jugar_saludos'),
    # CUERPO HUMANO
    path('jugar/cuerpo_humano/', views.jugar_cuerpo_humano, name='jugar_cuerpo_humano'),
    # PARENTESCO
    path('jugar/parentesco/', views.jugar_parentesco, name='jugar_parentesco'),
    # ELEMENTO NATURALEZA
    path('jugar/elemento_naturaleza/', views.jugar_elementos_naturaleza, name='jugar_elementos_naturaleza'),

    #---------------LOGIN-----------------
    path('login/', views.login_profesor, name='login_profesor'),
    path('bienvenida/', views.profesor_bienvenida, name='profesor_bienvenida'),
    path('logout/', views.logout_profesor, name='logout_profesor'),

    # ---------------ADMIN-----------------------
    path('login_admin/', views.login_admin, name='login_admin'),
    path('admin_bienvenida/', views.admin_bienvenida, name='admin_bienvenida'),
    path('logout_admin/', views.logout_admin, name='logout_admin'),

    #--------------------IDIOMA---------------------
    path('i18n/', include('django.conf.urls.i18n')),

    #------------------RECUPERRAR CONTRASEÑA---------------
    path('recuperar-contrasena/', views.recuperar_contrasena, name='recuperar_contrasena'),


]