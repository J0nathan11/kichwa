from django.db import models

class Aprender_Objetos(models.Model):
    imagen_obj = models.ImageField(upload_to='imagenes_aprender_objetos/', null=True, blank=True)
    palabra_obj = models.CharField(max_length=100)
    audio_kichwa_obj = models.FileField(upload_to='audios_kichwa_objetos/', null=True, blank=True)

    def __str__(self):
        return self.palabra_obj

class Aprender_Meses(models.Model):
    imagen_mes = models.ImageField(upload_to='imagenes_aprender_meses/', null=True, blank=True)
    palabra_mes = models.CharField(max_length=100)
    audio_kichwa_mes = models.FileField(upload_to='audios_kichwa_meses/', null=True, blank=True)

    def __str__(self):
        return self.palabra_mes

class Aprender_Numeros(models.Model):
    imagen_num = models.ImageField(upload_to='imagenes_aprender_numeros/', null=True, blank=True)
    palabra_num = models.CharField(max_length=100)
    audio_kichwa_num = models.FileField(upload_to='audios_kichwa_numeros/', null=True, blank=True)

    def __str__(self):
        return self.palabra_num
    
class Aprender_Dias(models.Model):
    imagen_dia = models.ImageField(upload_to='imagenes_aprender_dia/', null=True, blank=True)
    palabra_dia = models.CharField(max_length=100)
    audio_kichwa_dia = models.FileField(upload_to='audios_kichwa_dia/', null=True, blank=True)

    def __str__(self):
        return self.palabra_dia
    
class Aprender_Saludos(models.Model):
    imagen_sal = models.ImageField(upload_to='imagenes_aprender_saludos/', null=True, blank=True)
    palabra_sal = models.CharField(max_length=100)
    audio_kichwa_sal = models.FileField(upload_to='audios_kichwa_saludos/', null=True, blank=True)

    def __str__(self):
        return self.palabra_sal
    
class Aprender_Animales(models.Model):
    imagen_ani = models.ImageField(upload_to='imagenes_aprender_animales/', null=True, blank=True)
    palabra_ani = models.CharField(max_length=100)
    audio_kichwa_ani = models.FileField(upload_to='audios_kichwa_animales/', null=True, blank=True)

    def __str__(self):
        return self.palabra_ani
    
class Aprender_Colores(models.Model):
    imagen_col = models.ImageField(upload_to='imagenes_aprender_colores/', null=True, blank=True)
    palabra_col = models.CharField(max_length=100)
    audio_kichwa_col = models.FileField(upload_to='audios_kichwa_colores/', null=True, blank=True)

    def __str__(self):
        return self.palabra_col

class Aprender_Cuerpo_Humano(models.Model):
    imagen_cue = models.ImageField(upload_to='imagenes_aprender_cuerpo_humano/', null=True, blank=True)
    palabra_cue = models.CharField(max_length=100)
    audio_kichwa_cue = models.FileField(upload_to='audios_kichwa_cuerpo_humano/', null=True, blank=True)

    def __str__(self):
        return self.palabra_cue
    
class Aprender_Parentesco(models.Model):
    imagen_par = models.ImageField(upload_to='imagenes_aprender_parentesco/', null=True, blank=True)
    palabra_par = models.CharField(max_length=100)
    audio_kichwa_par = models.FileField(upload_to='audios_kichwa_parentesco/', null=True, blank=True)

    def __str__(self):
        return self.palabra_par
    
class Aprender_Elemento_Naturaleza(models.Model):
    imagen_ele = models.ImageField(upload_to='imagenes_aprender_elementos_naturaleza/', null=True, blank=True)
    palabra_ele = models.CharField(max_length=100)
    audio_kichwa_ele = models.FileField(upload_to='audios_kichwa_elementos_naturaleza/', null=True, blank=True)

    def __str__(self):
        return self.palabra_ele
    
class Estudiante(models.Model):
    nombres_est = models.CharField(max_length=100)
    apellidos_est = models.CharField(max_length=100)
    cedula_est = models.CharField(max_length=10, unique=True)
    genero_est = models.CharField(max_length=20)
    nivel_escolar_est = models.CharField(max_length=50)
    estado_est = models.CharField(max_length=10) 
    fecha_registro_est = models.DateField(auto_now_add=True)
    fecha_actualizacion_est = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.nombres_est} {self.apellidos_est}"

#------------------------LOGIN------------------------------

class Profesor(models.Model):
    usuario = models.CharField(max_length=150, unique=True)
    contrasena = models.CharField(max_length=128)

    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    cedula = models.CharField(max_length=10, unique=True)
    foto = models.ImageField(upload_to='foto_profesor/', null=True, blank=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True)
    sexo = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"
    
