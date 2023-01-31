from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . models import Accounts
import requests
import json

# Create your views here.

#user login function
def user_login(request):

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(email=email,password=password)

        if user is not None:
            print(user)
            user_email = Accounts.objects.get(username=user)
            print('user email',user_email)
            request.session['email'] = user_email.email
            login(request,user)
            return redirect('home-page')
        else:
            messages.error(request,'Invalid data')
            return redirect('user-login')
                
    return render(request,'users/login.html')

#user logout function
def user_logout(request):

    if 'email' in request.session:
        request.session.flush()
        logout(request)
        return redirect('user-login')  


#index page function (list all tickets function)
@login_required(login_url='user-login')
def home_page(request):

    user_email = request.session['email']
    print(user_email)
    user = Accounts.objects.get(email=user_email)
    user_id = user.user_id
    print('user id is ',user_id)
    email = 'akhilaki028@gmail.com'
    context = {}
    user = email + '/token'
    url = 'https://test1681.zendesk.com/api/v2/users/'+user_id+'/tickets/requested' 
    api_token = 'NWDBIu52oRWOj6PcX78HF3dmUviHHpkJGIZPbxvc'

    response = requests.get(
        url, auth=(user, api_token)
    )
    print('here is the response',response)
    for i in response:
        print('her is the',i)
    if response:
        ticket_data = response.json()
        data = ticket_data['tickets']
        context['data'] = data

        print('data are',data)

    return render(request,'users/ticketlist.html',context)


#user ticket create function
@login_required(login_url='user-login')
def create_userTicket(request):

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
            return redirect('create-userticket')
        if body == '':
            messages.error(request,'body required') 
            return redirect('create-userticket')
        if priority == '':
            messages.error(request,'priority required')
            return redirect('create-userticket')   

        ticket_data = {
                "request": {
                    "comment": {
                    "body": body
                    },
                    "priority": priority,
                    "subject": subject,
                    "requester":{
                        "name":user_data.username,
                        "email":email
                    }
                }
                }
        ticket = json.dumps(ticket_data)
        
        url = 'https://test1681.zendesk.com/api/v2/requests.json'   
        headers = {'content-type': 'application/json'}
        api_token = 'NWDBIu52oRWOj6PcX78HF3dmUviHHpkJGIZPbxvc'

        user = 'akhilaki028@gmail.com' + '/token'

        
        print('here is user',user)
        response = requests.post(
            url,
            data=ticket,
            headers=headers,
            auth =(user,api_token)
        )   
        print('here is the response',response)
        for i in response:
            print('i',i)
        if response.status_code != 201:
            messages.error(request,'something went wrong',response)
            return redirect('create-userticket')
        else:
            messages.success(request,'Ticket created succesfully')
            return redirect('home-page')

    return render(request,'users/createticket.html',context)

#user created ticket delete function 
login_required(login_url='user-login')
def delete_userticket(request,id):

    ticket_id = str(id)
    email = 'akhilaki028@gmail.com'

    user = email + '/token'

    url = 'https://test1681.zendesk.com/api/v2/tickets/'+ticket_id
    api_token = 'NWDBIu52oRWOj6PcX78HF3dmUviHHpkJGIZPbxvc'

    response = requests.delete(
        url, auth=(user,api_token)
    )
    if response.status_code == 204:
        messages.success(request,'Ticket deleted succesfully')
        return redirect('home-page')
    else:
        messages.error(request,'something went wrong')

        return redirect('home-page')
