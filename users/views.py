from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
# Create your views here.
def Register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password1']
            user = authenticate(request, username=username, email=email, password=password)
            messages.success(request, f'Welcome {username}!')
            login(request, user)
            return redirect('courses:list')
    else:
        form = RegisterForm()
    context = {
        'form': form
    }
    return render(request, 'users/register.html', context)