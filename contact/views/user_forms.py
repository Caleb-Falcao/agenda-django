from django.shortcuts import render, redirect
from django.contrib import messages, auth
from contact.forms import RegisterForm, RegisterUpdateForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

def register(request):
    form= RegisterForm()
    #messages.info(request, 'Um texto qualquer')
    #messages.success(request, 'Um texto qualquer')
    #messages.warning(request, 'Um texto qualquer')
    #messages.error(request, 'Um texto qualquer')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário registrado')
            return redirect('contact:login')
    return render(
        request, 
        'contact/register.html',
        {
            'form': form,
        }
    )

@login_required(login_url='contact:login')
def user_update(request):
    form = RegisterUpdateForm(instance=request.user)
    
    if request.method != 'POST':        
        return render(
            request, 
            'contact/user_update.html',
            {
                'form': form,
            }
        )
    form = RegisterUpdateForm(data=request.POST, instance=request.user)

    if not form.is_valid():
        return render(
            request, 
            'contact/user_update.html',
            {
                'form': form,
            }
        )
    form.save()
    return redirect('contact:user_update')
    


def login_view(request):
    form = AuthenticationForm(request)
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            user = form.get_user()
            auth.login(request,user)
            messages.success(request, 'Logado com sucesso')
            return redirect('contact:index')
        messages.error(request,'Login Inválido')
    return render(
        request, 
        'contact/login.html',
        {
            'form': form,
        }
    )

@login_required(login_url='contact:login')  
def logout_view(request):
    auth.logout(request)
    return redirect('contact:login')