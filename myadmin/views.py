from django.shortcuts import render, redirect
from users.models import Accounts
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . models import Department
from django.contrib.auth.decorators import login_required
# Create your views here.


#Admin login function
def admin_login(request):

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user  = authenticate(email=email, password=password)

        if user is not None:
            request.session['email'] = email
            login(request, user)
            return redirect('create-user')
        else:
            messages.error(request,'Invalid data')
            return redirect('admin-login')
                
    return render(request,'myadmin/adminlogin.html')


#Admin logout function
def admin_logout(request):
    if 'email' in request.session:
        request.session.flush()
        logout(request)
        return redirect('admin-login')


#List all department function
@login_required(login_url='admin-login')
def department_list(request):

    department = Department.objects.all()
    context = {
        'department':department
    }
    return render(request,'myadmin/departmentlist.html',context)


#Create a new department function
@login_required(login_url='admin-login')
def create_department(request):
    
    if request.method == 'POST':
        
        name = request.POST['name']
        description = request.POST['description']

        #getting the email of the admin from session
        email = request.session['email']
        user = Accounts.objects.get(email=email)

        created_by = user
        department = Department.objects.create(name=name,description=description,created_by=created_by)
        department.save()
        messages.success(request,'Department added succesfully')
        return redirect('department-list')

    return render(request,'myadmin/add_department.html')


#List all users function
@login_required(login_url='admin-login')
def users_list(request):

    users = Accounts.objects.exclude(email=request.user)
    context = {
        'users':users
    }
    return render(request,'myadmin/userslist.html',context)


#Create a new user function
@login_required(login_url='admin-login')
def create_user(request):

    department = Department.objects.all()
    context = {
        'department':department
    }

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        password2 = request.POST['password2']
        department_obj = request.POST['department']
        role = request.POST['role']
        print('request.user is ',request.user)
        d_obj = Department.objects.get(id=department_obj) #getting instance of department

        created_id = request.session['email']
        user = Accounts.objects.get(email=created_id)
        print('user is',user)

        if len(password)<4:
            messages.error(request,'Password length should be greater than 4')
            return redirect('create-user')

        if password != password2:
            messages.error(request,'Password and confirm password should match')
            return redirect('create-user')

        user = Accounts.objects.create_user(username=username,email=email,phone_number=phone_number,created_by=user,
                password=password,department=d_obj,role=role)
        user.save()     
        messages.success(request,'User created succesfully')
        return redirect('users-list')   
        
    return render(request,'myadmin/createusers.html',context)


#edit department function.
@login_required(login_url='admin-login')
def edit_department(request,id):
    print('here is the id',id)
    try:
        department = Department.objects.get(id=id)
    except:
        messages.error(request,'Department does not exist')
        return redirect('department-list')

    context = {
        'department':department
    }  

    if request.method == 'POST':
        department.name = request.POST['name']
        department.description = request.POST['description']    
        if department.name == '':
            messages.error(request,'Name field required')
            return redirect('edit-department',id)
        department.save()
        messages.success(request,'Department edited succesfully')
        return redirect('department-list')    

    return render(request,'myadmin/add_department.html',context)     


#delete department
@login_required(login_url='admin-login')
def delete_department(request,id):
    try:
        department = Department.objects.get(id=id)
        print('deparmetn is',department)
    except:
        messages.error(request,'Department does not exist')
        return redirect('department-list')
    if (Accounts.objects.filter(department=department)): #if department associated with any user, then show error.
        messages.error(request,'Department associated with user, cannot delete')   
        return redirect('department-list') 
    department.delete()
    messages.success(request,'Department deleted succesfully')  
    return redirect('department-list')      