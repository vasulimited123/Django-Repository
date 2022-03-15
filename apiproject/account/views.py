from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
import uuid
from urllib.parse import urlencode
from rest_framework.authtoken.models import Token
# from django.core.signing import Signer
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.conf import settings
from account.models import UserDetails
from django.contrib.auth import authenticate
import datetime
# signer = Signer()
User = get_user_model()

@api_view(['POST'])
def signup(request):

    token=request.auth.key
    usermailbytoken = Token.objects.get(key=token).user
    userauth = User.objects.get(email=usermailbytoken)
    if userauth.groups.filter(name='Broker').exists() or userauth.groups.filter(name='Client').exists() or userauth.groups.filter(name='Insurer').exists():
            return Response({'status':'fail','message':'Does not permission to update'}, status = status.HTTP_404_NOT_FOUND)

    if userauth.groups.filter(name='SuperAdmin').exists() or userauth.groups.filter(name='Admin').exists() :        
        try:
            email = request.POST['email']
        except:
             return Response({'status':'fail','message':'Email required'}, status = status.HTTP_404_NOT_FOUND)
        
        try:
            gtype= request.POST['gtype']
        except:
             return Response({'status':'fail','message':'Group required'}, status = status.HTTP_404_NOT_FOUND)
        
        firstname = request.POST.get('firstname', False)
        lastname = request.POST.get('lastname', False)
        company = request.POST.get('comapny', False)
        profileimage = request.POST.get('profileimage',False)
        email_verify = User.objects.filter(email=email)
        if len(email_verify)<=0:
            try:
                Group.objects.get(name=gtype)
            except:
                return Response({'status':'fail','message':'Group does not exist'}, status = status.HTTP_404_NOT_FOUND)    
                
            user = User.objects.create_user(email = email)
            if firstname is False:
                pass
            else:
                User.objects.filter(email=email).update(first_name=firstname)
            if lastname is False:
                pass
            else:
                User.objects.filter(email=email).update(last_name=lastname)
            if company is False:
                pass
            else:
                User.objects.filter(email=email).update(company=company)
            if profileimage is False:
                pass
            else:
                UserDetails.objects.create(user=user,profile_image=profileimage)
            
            group = Group.objects.get(name=gtype)
            user.groups.add(group)
            user.set_unusable_password() 
            user.save()
            token_obj = Token.objects.create(user=user)
            send_email(email,firstname,token_obj)
            return Response({'status':'Success','message':'Mail has been sent to your account'}, status = status.HTTP_404_NOT_FOUND)
            
        else:
            return Response({'status':'fail','message':'Email already exist'}, status = status.HTTP_404_NOT_FOUND)


def send_email(email,firstname,token_obj):
    subject = "Mail Regarding Set Password "
    email_template_name = 'email.txt'
    token = str(token_obj)
    parameter = {
        'user' : firstname,
        'domain' : '127.0.0.1:8000',
        'token' : token,
        'protocol' : 'http',
        }
    email_body = render_to_string(email_template_name,parameter)    
    email_from = settings.EMAIL_HOST_USER
    rece = [email]
    send_mail(subject, email_body, email_from, rece,fail_silently= False)  

@api_view(['POST'])
def setpassword(request,token):
    token =token
    password = request.POST['password']
    confirmpassword= request.data['confirmpassword']
    if password == confirmpassword:
        try:
            usermail = Token.objects.get(key=token).user
            user= User.objects.get(email=usermail)
            user.set_password(password)
            user.save()
            t = Token.objects.get(user=user)
            t.delete()
            Token.objects.create(user=user)  
            return Response({'status':'Success','message':'Password Set'}, status = status.HTTP_200_OK)
        except:
            return Response({'status':'Failed','message':'Link is Expire'}, status = status.HTTP_404_NOT_FOUND)
    else:
        return Response({'status':'Failed','message':'Password did not match'}, status = status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def update(request,email):
    # data = dict(request.POST.items())
    # print(data)
    firstname = request.POST.get('firstname', False)
    lastname = request.POST.get('lastname', False)
    company = request.POST.get('company', False)
    profileimage = request.POST.get('profileimage',False)
    email_verify = User.objects.filter(email=email)
    if len(email_verify)<=0:
        return Response({'status':'fail','message':'Email does not Exist'}, status = status.HTTP_404_NOT_FOUND)
    else:
        try:
            print("Hello")
            token=request.auth.key
            usermailbytoken = Token.objects.get(key=token).user
            print(usermailbytoken)
        except:
            return Response({'status':'fail','message':'Invalid Token'}, status = status.HTTP_404_NOT_FOUND)

        userauth = User.objects.get(email=usermailbytoken)
        
        if str(usermailbytoken) == str(email):
            if profileimage is False:
                pass
            else:
                user=User.objects.get(email = email)
                UserDetails.objects.filter(user = user).update(profile_image=profileimage)
            if firstname is False:
                pass
            else:    
                User.objects.filter(email = email).update(first_name=firstname)
            if lastname is False:
                pass
            else:    
                User.objects.filter(email= email).update(last_name=lastname)
            if company is False:
                pass
            else:    
                User.objects.filter(email = email).update(company=company)  

            return Response({'status':'Success','message':'Data updated'}, status = status.HTTP_200_OK)      

        if userauth.groups.filter(name='Broker').exists() or userauth.groups.filter(name='Client').exists() or userauth.groups.filter(name='Insurer').exists():
            return Response({'status':'fail','message':'Does not permission to update'}, status = status.HTTP_404_NOT_FOUND)

        if userauth.groups.filter(name='SuperAdmin').exists() or userauth.groups.filter(name='Admin').exists() :
            if profileimage is False:
                pass
            else:
                user=User.objects.get(email = email)
                UserDetails.objects.filter(user = user).update(profile_image=profileimage)
            if firstname is False:
                pass
            else:    
                User.objects.filter(email = email).update(first_name=firstname)
            if lastname is False:
                pass
            else:    
                User.objects.filter(email= email).update(last_name=lastname)
            if company is False:
                pass
            else:    
                User.objects.filter(email = email).update(company=company)  

            return Response({'status':'Success','message':'Data updated'}, status = status.HTTP_200_OK)      
       
@api_view(['GET'])
def getall(request):
    token=request.auth.key
    usermailbytoken = Token.objects.get(key=token).user
    userauth = User.objects.get(email=usermailbytoken)
    if userauth.groups.filter(name='Broker').exists() or userauth.groups.filter(name='Client').exists() or userauth.groups.filter(name='Insurer').exists():
            return Response({'status':'fail','message':'Does not permission to update'}, status = status.HTTP_404_NOT_FOUND)
    
    if userauth.groups.filter(name='SuperAdmin').exists() or userauth.groups.filter(name='Admin').exists() : 
        listall=[]
        userdetails = UserDetails.objects.all()
        for ud in userdetails:
            dict_of_patient = {'email': ud.user.email,'group':ud.user.groups.all()[0].name,'First Name':ud.user.first_name,'Last Name':ud.user.last_name,'Company':ud.user.company,'image':ud.profile_image.url}
            listall.append(dict_of_patient)

        return Response({'status':'success','data':listall}, status = status.HTTP_200_OK)
        
@api_view(['DELETE'])
def delete(request,email):
    token=request.auth.key
    usermailbytoken = Token.objects.get(key=token).user
    userauth = User.objects.get(email=usermailbytoken)
    if userauth.groups.filter(name='Broker').exists() or userauth.groups.filter(name='Client').exists() or userauth.groups.filter(name='Insurer').exists():
        return Response({'status':'fail','message':'Does not permission to delete'}, status = status.HTTP_404_NOT_FOUND)

    if userauth.groups.filter(name='SuperAdmin').exists() or userauth.groups.filter(name='Admin').exists():
        try:
            user = User.objects.get(email=email)
            user.delete()
            return Response({'status':'Success','message':'User Deleted'}, status = status.HTTP_200_OK)    
        except:
            return Response({'status':'fail','message':'Inavlid Email'}, status = status.HTTP_404_NOT_FOUND)    

@api_view(['POST'])
def login(request):
    try:
        email = request.POST['email']
    except:
        return Response({'status':'fail','message':'Please enter Email'}, status = status.HTTP_404_NOT_FOUND)        
    
    password = request.POST.get('password', False)
    if User.objects.filter(email=email).exists():
        user = User.objects.get(email=email)
        if password is False:
            password = str(user.password)
            if password[0] == "!":
                return Response({'status':'fail','message':'Please set the password'}, status = status.HTTP_404_NOT_FOUND)
            else:
                return Response({'status':'fail','message':'Please enter password'}, status = status.HTTP_404_NOT_FOUND)
        else:
            userlogin = authenticate(email=email,password=password) 
            if userlogin is None:
                return Response({'status':'fail','message':'Invalid E-Mail id password'}, status = status.HTTP_404_NOT_FOUND)
            else:
                t = Token.objects.get(user=user)
                t.delete()
                Token.objects.create(user=user)  
                return Response({'status':'success','message':'Login Successfull'}, status = status.HTTP_200_OK)       
    else:
        return Response({'status':'fail','message':'Invalid E-Mail'}, status = status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def showdatacurrentlastmonth(request):
    token=request.auth.key
    usermailbytoken = Token.objects.get(key=token).user
    userauth = User.objects.get(email=usermailbytoken)
    if userauth.groups.filter(name='Broker').exists() or userauth.groups.filter(name='Client').exists() or userauth.groups.filter(name='Insurer').exists():
        return Response({'status':'fail','message':'Does not permission to see data'}, status = status.HTTP_404_NOT_FOUND)

    if userauth.groups.filter(name='SuperAdmin').exists() or userauth.groups.filter(name='Admin').exists():    
        users = User.objects.all()
        listdatejoined = []
        current_time = datetime.datetime.now() 
        for user in users: 
            num_months = (current_time.year - user.date_joined.year)*12 + (current_time.month - user.date_joined.month )
            if num_months==0:
                data_dict = {'user': user.email, 'company':user.company}
                listdatejoined.append(data_dict) 

        return Response({'status':'success','data': listdatejoined}, status = status.HTTP_200_OK)        

           
        
    
    
    

        


 # token = "f" + str(uuid.uuid4()) 
            # signed_obj = signer.sign_object({'key1':email, 'key2':gtype, 'key3':firstname,'key4':lastname,'key5':company,'key6':token})
            # string_data = str(signed_obj)