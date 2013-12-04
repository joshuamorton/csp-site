
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from register.forms import RegistrationForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
# Create your views here.

def index(request):
    return HttpResponse("This is the homepage. <br> You can <a href='/login'>login</a> or <a href='/register'>register</a>.")
    print("Someone went to the homepage.")

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username = username, password = password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/welcome/')
                else:
                    return HttpResponse("Error, you aren't registered. Register <a href='/register'>here</a>.")
    else:
        form = LoginForm()
    return render(request, 'login/login.html', {'form' : form})

def logout_view(request):
    logout(request)
    return HttpResponse("you have been logged out.  You can login <a href='/login'>here</a>.")

#THIS IS HACKY AS HELL!
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            first = form.cleaned_data['first_name']
            last = form.cleaned_data['last_name']
            pass1 = form.cleaned_data['password']
            pass2 = form.cleaned_data['confirm_password']
            email1 = form.cleaned_data['email']
            email2 = form.cleaned_data['confirm_email']
            if User.objects.filter(username=username).count():
                return HttpResponseRedirect('/register/')
            if pass1 == pass2 and email1 == email2:
                user = User.objects.create_user(username, email1, pass1)
                try:
                    user.first_name = first
                except:
                    pass
                try:
                    user.last_name = last
                except:
                    pass
             
                user.save()
                return HttpResponseRedirect('/success/')
            else:
                return HttpResponseRedirect('/register/')
        else:
            return HttpResponseRedirect('/register/')
    else:
        form = RegistrationForm()
    return render(request, 'register/register.html', {'form' : form})

def welcome(request):
    if not request.user.is_authenticated():
        return HttpResponse("access denied")
    return HttpResponse("Welcome.  You can logout <a href = '/logout'>here</a>.\n.  Our app is <a href='/app'>here.")

def thanks(request):
    return HttpResponse("thanks for registering!  You can now login <a href = '/login'>here</a>")