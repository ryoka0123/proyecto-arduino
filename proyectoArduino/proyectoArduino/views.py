from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.models import Arduino
from django.http import HttpResponseNotFound

def inicio_sesion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('microcontrolador')  # Cambia 'dashboard' por la vista principal tras login
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
            return render(request, 'forms/inicioSesion.html')
    return render(request, 'forms/inicioSesion.html')


def registro(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            messages.error(request, "Las contraseñas no coinciden.")
            return render(request, 'forms/registro.html')
        if User.objects.filter(username=username).exists():
            messages.error(request, "El usuario ya existe.")
            return render(request, 'forms/registro.html')
        user = User.objects.create_user(username=username, password=password1)
        login(request, user)
        return redirect('microcontrolador')
    return render(request, 'forms/registro.html')


def cerrar_sesion(request):
    logout(request)
    return redirect('inicioSesion')

@login_required
def registroArduino(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        ip = request.POST.get('ip')
        # Solo verifica si la IP ya está registrada por cualquier usuario
        if Arduino.objects.filter(ip=ip).exists():
            messages.error(request, "La IP ya está registrada por otro Arduino.")
            return render(request, 'forms/registroArduino.html')
        Arduino.objects.create(user=request.user, nombre=nombre, ip=ip)
        return redirect('microcontrolador')
    return render(request, 'forms/registroArduino.html')

@login_required
def registroTriggers(request):
    return render(request, 'forms/registroTriggers.html')

@login_required
def microcontrolador(request):
    arduinos = Arduino.objects.filter(user=request.user)
    return render(request, 'dashboard/microcontrolador.html', {
        'username': request.user.username,
        'arduinos': arduinos
    })

@login_required
def triggers(request):
    return render(request, 'dashboard/triggers.html')

@login_required
def eliminar_arduino(request, arduino_id):
    arduino = Arduino.objects.get(id=arduino_id, user=request.user)
    if request.method == 'POST':
        arduino.delete()
        return redirect('microcontrolador')
    return redirect('microcontrolador')

def pagina_no_encontrada(request, exception):
    return render(request, '404.html', status=404)