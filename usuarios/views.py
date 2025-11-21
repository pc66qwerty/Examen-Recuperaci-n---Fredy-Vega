from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import PerfilUsuario

def login_view(request):
    if request.user.is_authenticated:
        return redirect('usuarios')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('usuarios')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'usuarios/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def usuarios_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        telefono = request.POST.get('telefono', '')
        departamento = request.POST.get('departamento', '')
        
        if username and password:
            try:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
                
                PerfilUsuario.objects.create(
                    usuario=user,
                    telefono=telefono,
                    departamento=departamento
                )
                
                messages.success(request, f'Usuario {username} creado exitosamente')
            except Exception as e:
                messages.error(request, f'Error al crear usuario: {str(e)}')
        else:
            messages.error(request, 'Usuario y contraseña son requeridos')
        
        return redirect('usuarios')
    
    usuarios = User.objects.all().order_by('-date_joined')
    return render(request, 'usuarios/usuarios.html', {'usuarios': usuarios})

@login_required
def eliminar_usuario(request, user_id):
    if request.method == 'POST':
        usuario = get_object_or_404(User, id=user_id)
        
        if usuario.id == request.user.id:
            messages.error(request, 'No puedes eliminar tu propio usuario')
        else:
            username = usuario.username
            usuario.delete()
            messages.success(request, f'Usuario {username} eliminado exitosamente')
    
    return redirect('usuarios')

@login_required
def creditos_view(request):
    return render(request, 'usuarios/creditos.html')