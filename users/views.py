from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

# Create your views here.

def user_login(request):

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(email=email,password=password)

        if user is not None:
            request.session['email'] = email
            login(request,user)
            return redirect('index')
        else:
            messages.error(request,'Invalid data')
            return redirect('user-login')
                
    return render(request,'users/login.html')

def user_logout(request):

    if 'email' in request.session:
        request.session.flush()
        logout(request)
        return redirect('user-login')    


def index(request):
    return render(request,'users/userHeader.html')

