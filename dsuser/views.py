from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormView
from django.contrib.auth.hashers import make_password
from .forms import RegisterForm, LoginForm
from .models import Dsuser

# Create your views here.

def index(request):
    return render(request, 'index.html', { 'userid': request.session.get('user') })

class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = '/'

    def form_valid(self, form):
        dsuser = Dsuser(
            userid=form.data.get('userid'),
            email=form.data.get('email'),
            password=make_password(form.data.get('password')),
        )
        dsuser.save()

        return super().form_valid(form)


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):
        self.request.session['user'] = form.data.get('userid')

        return super().form_valid(form)

def logout(request):
    if 'user' in request.session:
        del(request.session['user'])

    return redirect('/')

