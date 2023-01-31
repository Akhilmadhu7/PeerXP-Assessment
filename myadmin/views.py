from django.shortcuts import render, redirect
from users.models import Accounts
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . models import Department
from django.contrib.auth.decorators import login_required
import requests
import json
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
            return redirect('department-list')
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

        if name == "":
            messages.error(request,'Department name required')
            return redirect('create-department')
        if description == '':
            messages.error(request,'Description required')
            return redirect('create-department')    

        #getting the email of the admin from session
        email = request.session['email']
        user = Accounts.objects.get(email=email)    #getting the instance of the creator
        created_by = user
        department = Department.objects.create(name=name,description=description,created_by=created_by)
        department.save()
        messages.success(request,'Department added succesfully')
        return redirect('department-list')

    return render(request,'myadmin/add_department.html')


#List all users function
@login_required(login_url='admin-login')
def users_list(request):
    email = request.session['email']
    users = Accounts.objects.exclude(email=email).order_by('id')
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

        d_obj = Department.objects.get(id=department_obj) #getting instance of department

        creator_email = request.session['email']
        created_by = Accounts.objects.get(email=creator_email)  #getting the instance of creator account


        if username == '':
            messages.error(request,'Username required')
            return redirect('create-user')
        if email == '':
            messages.error(request,'Email required')
            return redirect('create-user')
        if phone_number == '':
            messages.error(request,'Phone number required')
            return redirect('create-user')
        if role == '':
            messages.error(request,'Role required')
            return redirect('create-user')

        if len(password)<4:
            messages.error(request,'Password length should be greater than 4')
            return redirect('create-user')

        if password != password2:
            messages.error(request,'Password and confirm password should match')
            return redirect('create-user')

        user_data = {"user": {"name": username, "email": email}}   #for creating an user account  
        data = json.dumps(user_data)

        url = 'https://test1681.zendesk.com/api/v2/users.json'  #api to create new user in zendesk
        api_token = 'NWDBIu52oRWOj6PcX78HF3dmUviHHpkJGIZPbxvc'  
        headers = {'content-type': 'application/json'} 
        user = creator_email + '/token'
        response = requests.post(
            url,
            auth=(user,api_token),
            headers=headers,
            data=data
        )

        if response.status_code != 201:
            print('messages of response',response)
            for i in response:
                print('response loop', i)
            messages.success(request,'Invalid data zendesk')
            return redirect('create-user')  
        else:
            print('user is ',user)
            for i in response:
                print('response loop', i)
            response_obj = response.json()    
            user_id = response_obj['user']['id']    #getting the user id from response
            user = Accounts.objects.create_user(username=username,email=email,phone_number=phone_number,created_by=created_by,
                    user_id=user_id,password=password,department=d_obj,role=role)
            user.save()     
            messages.success(request,'User created succesfully')
            return redirect('users-list')      
        
    return render(request,'myadmin/createusers.html',context)


#edit department function.
@login_required(login_url='admin-login')
def edit_department(request,id):

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
            messages.error(request,'Department name field required')
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
    except:
        messages.error(request,'Department does not exist')
        return redirect('department-list')
    if (Accounts.objects.filter(department=department)): #if department associated with any user, then show error.
        messages.error(request,'Department associated with user, cannot delete')   
        return redirect('department-list') 
    department.delete()
    messages.success(request,'Department deleted succesfully')  
    return redirect('department-list')   


#create tickets by admin funciton
@login_required(login_url='admin-login')
def create_ticket(request):

    email = request.session['email']
    user_data = Accounts.objects.get(email=email)
    context = {
        'user_data':user_data
    }

    if request.method == 'POST':
        subject = request.POST['subject']
        body = request.POST['body']
        priority = request.POST['priority']

        if subject == '':
            messages.error(request,'subject required')
            return redirect('create-ticket')
        if body == '':
            messages.error(request,'body required') 
            return redirect('create-ticket')
        if priority == '':
            messages.error(request,'priority required')
            return redirect('create-ticket')

        ticket_data = {
                "request": {
                    "comment": {
                    "body": body
                    },
                    "priority": priority,
                    "subject": subject
                }
                }
        ticket = json.dumps(ticket_data)
        url = 'https://test1681.zendesk.com/api/v2/requests.json'   
        headers = {'content-type': 'application/json'}
        api_token = 'NWDBIu52oRWOj6PcX78HF3dmUviHHpkJGIZPbxvc'

        user = email + '/token'
        print('here ise user',user)
        response= requests.post(
            url,
            data=ticket,
            headers=headers,
            auth =(user,api_token)
        )    

        if response.status_code != 201:
            print('is that come here',response)
            for i in response:
                print('for loop for reqobj',i)
            messages.error(request,'Something went wrong')
            return redirect('create-ticket')
        else:
            print('here it is')
            messages.success(request,'Ticket created succesfully')
            return redirect('tickets-list')


    return render(request,'myadmin/create_ticket.html',context)


#function for listing all tickets created by admin and users
@login_required(login_url='admin-login')
def tikcets_list(request):

    email = request.session['email']
    context = {}
    user = email + '/token'
    url = 'https://test1681.zendesk.com/api/v2/tickets.json' 
    api_token = 'NWDBIu52oRWOj6PcX78HF3dmUviHHpkJGIZPbxvc'

    response = requests.get(
        url, auth=(user, api_token)
    )
    for i in response:
        print('data are',i)
    if response:
        ticket_data = response.json()
        for i in ticket_data:
            print('i is ',i)
            print()
            print()
        data = ticket_data['tickets']
        context['data'] = data

    return render(request,'myadmin/ticketslist.html',context)


#delete ticket function
@login_required(login_url='admin-login')
def delete_ticket(request,id):

    
    ticket_id = str(id)
    email = request.session['email']

    user = email + '/token'

    url = 'https://test1681.zendesk.com/api/v2/tickets/'+ticket_id
    api_token = 'NWDBIu52oRWOj6PcX78HF3dmUviHHpkJGIZPbxvc'

    response = requests.delete(
        url, auth=(user,api_token)
    )

    print('here is the reponse',response)
    for i in response:
        print('resssss',i)
    if response.status_code == 204:
        messages.success(request,'Ticket deleted succesfully')
        return redirect('tickets-list')
    else:
        messages.error(request,'something went wrong')
        return redirect('tickets-list')    

