from django.shortcuts import render
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from useraccount.serializer import UserSerializer,AgentUserSerializer
from rest_framework.views import APIView
from useraccount.models import User
from rest_framework.response import Response
from django.template.loader import render_to_string
from django.core.mail import send_mail
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from ticket.models import Organization
import random 
from string import digits,punctuation,ascii_letters

def username_generator(email):
    #generating username from the email itself provided by the user
    email = email.split('@')[0]
    return email


def password_generator():
    symbols = ascii_letters + digits + punctuation
    secure_random = random.SystemRandom()
    passwd = "".join(secure_random.choice(symbols)for i in range(8))
    return passwd
    


class UserModelViewset(ModelViewSet):
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    queryset = User.objects.filter(is_admin = True)

    def create(self,request,*args,**kwargs):
        ser_data = self.get_serializer(data = request.data)
        if ser_data.is_valid():
            org=Organization.objects.create(name = request.data.get('org_name'))
            user = User.objects.create_user(request.data.get('username'), request.data.get('email'),
                request.data.get('password'),is_admin = True,organization = org)
            usr = request.data['username']
            msg_html = render_to_string('email_template.html',{'usr':usr})
            send_mail('Subject here','Here is the message.','chouhansagar131@gmail.com',
                    [request.data['email'],'chouhansagar131@gmail.com'],html_message=msg_html,
                    fail_silently=False,
            )
            token = str(Token.objects.create(user=user))
            return Response({'token':token,'user':ser_data.data})
        else:
            return Response(ser_data.errors,status = status.HTTP_400_BAD_REQUEST)


class AgentUserViewSet(ModelViewSet):
    serializer_class = AgentUserSerializer
    queryset = User.objects.filter(is_admin = False)

    def create(self,request,*args,**kwargs):
        ser_data = self.get_serializer(data = request.data)
        if ser_data.is_valid():
            email = request.data.get('email')
            username = username_generator(email)
            password = password_generator()
            org = Organization.objects.get(name = request.data.get('org_name'))
            user = User.objects.create_user(username=username,password= password,email = email,organization = org)
            token = str(Token.objects.create(user=user))
            msg_html = render_to_string('email_agent.html',{'org':request.data.get('org_name'),'username':username,'password':password})
            send_mail('Invitation TMS','','chouhansagar131@gmail.com',
                    [request.data['email'],'chouhansagar131@gmail.com'],
                    fail_silently=False,
                    html_message=msg_html,
            )
            return Response({'token':token,'username':username})
        else:
            return Response(ser_data.errors,status = status.HTTP_400_BAD_REQUEST)













