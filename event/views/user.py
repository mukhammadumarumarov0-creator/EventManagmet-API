from rest_framework.views import APIView
from rest_framework.response import Response
from event.models import User,UserConfirmation,VERIFIED,DONE
from event.utils import MyResponce,send_code_to_email
from event.serializers import RegistrationSerializer,ValidationSerializer,FullUpdateSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import UpdateAPIView
from event.permissions import IsAuthDoneOrVerified

class StartRegistration(APIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')
        user=User.objects.create(email=email)
        send_code_to_email(user.email,user.get_verify_code())
        
        return MyResponce.success(
            message="Code has been sent to your email address",
            data=user.get_token()
        )


class VerificationProccess(APIView):
    serializer_class = ValidationSerializer
    permission_classes = [IsAuthenticated]

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation=UserConfirmation.objects.filter(user=request.user).order_by("-created_at").first()
        code=serializer.validated_data.get('code')

        if code == confirmation.code and confirmation.is_expired():
          request.user.status=VERIFIED
          request.user.save()
          return MyResponce.success(
              message="Code Verified successfully",
              data=request.user.get_token()
              )
        
        return MyResponce.error("Code is invalid or expired")
        

class FullUpadteUser(UpdateAPIView):
    queryset=User.objects.all()
    permission_classes=[IsAuthDoneOrVerified]
    serializer_class=FullUpdateSerializer

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        user = serializer.save(updated_by=self.request.user)

        if user.status != DONE:
            user.status = DONE
            user.save()

    




    
    

