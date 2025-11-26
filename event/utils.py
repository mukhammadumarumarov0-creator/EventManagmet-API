from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import status
from config.settings import EMAIL_HOST_USER

def send_code_to_email(email,code):
    text = f"Hi, This is your Confirmation code for Registration to Event Managment System : {code}"
    send_mail(
        subject="Confirmation Code",
        message=text,
        from_email=EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False
    )


class MyResponce():
    def success(message,data=None):
        response={
            "message": message,
            "status": True,
            "data": data
        }
        return Response(data=response,status=status.HTTP_200_OK)
    
    def error(message,data=None):
        response={
            "message": message,
            "status": False,
            "data": data
        }
        return Response(data=response,status=status.HTTP_400_BAD_REQUEST)