from django.contrib.auth import login, logout
from django.shortcuts import redirect, render

from accounts.forms import LoginForm, SignupForm


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('homepage')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST['next'])
            return redirect('homepage')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {"form": form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('/articles')