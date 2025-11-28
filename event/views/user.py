from rest_framework.views import APIView
from event.models import User,UserConfirmation,VERIFIED,DONE
from event.utils import MyResponce,send_code_to_email
from event.serializers import RegistrationSerializer,ValidationSerializer,FullUpdateSerializer,LoginSerializer,UpdatePasswordSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import UpdateAPIView
from event.permissions import IsAuthDoneOrVerified
from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Authentication"])
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

@extend_schema(tags=["Authentication"])
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
        
@extend_schema(tags=["Authentication"])
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

@extend_schema(tags=["Authentication"])
class LoginUser(APIView):
    serializer_class=LoginSerializer
    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user=authenticate(
            username=serializer.validated_data.get("username"),
            password=serializer.validated_data.get("password")
        )
        if user:
            return MyResponce.success(
                message="You logged in to your account",
                data=user.get_token()
            )
        return MyResponce.error("Invalid password or email or username was entered")

@extend_schema(tags=["Authentication"])
class UpdatePassword(APIView):
    serializer_class=UpdatePasswordSerializer
    permission_classes=[IsAuthDoneOrVerified ,]

    def patch(self,request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=User.objects.filter(username=request.user.username).first()

        if user.status != DONE:
            user.status=DONE
        user.set_password(serializer.validated_data.get('password'))
        user.save()
        
        return MyResponce.success(
            message="Password updated successfully",
        )

@extend_schema(tags=["Authentication"])
class ResendVerificationCode(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user=request.user
        user_conf=UserConfirmation.objects.filter(user=user).order_by('-created_at').first()
        if not user_conf.is_expired():
            user.get_verify_code()
            return MyResponce.success(
                message='Confirmation code has been resent to your emial',
                data=user.get_token()
            )
        return MyResponce.error('Confirmation code has not been expired yet')
 


    
    

