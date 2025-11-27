from rest_framework import serializers
from event.models import User,DONE
from event.utils import username_emial

class RegistrationSerializer(serializers.Serializer):
    email=serializers.CharField(required=True)

class ValidationSerializer(serializers.Serializer):
    code=serializers.CharField(required=True,max_length=4)

class FullUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ["first_name","last_name","username","address","phone"]

    def validate_first_name(self,value):
        if not value.isalpha():
            raise serializers.ValidationError('Invalid first name, first name should contain only letters')
        return value
    
    def validate_last_name(self,value):
        if not value.isalpha():
            raise serializers.ValidationError('Invalid last name, last name should contain only letters')
        return value
    
    def validate_username(self, value):
        user = self.context["request"].user

        if not value.isalpha():
            raise serializers.ValidationError("Username must contain letters only")

        if User.objects.filter(username=value).exclude(id=user.id).exists():
            raise serializers.ValidationError("This username is already taken by another user")

        return value

    def validate_phone(self,value):
        if len(value) != 13 and not value.startswith("+998"):
            raise serializers.ValidationError('Invalid phone number')
        return value
    
class LoginSerializer(serializers.Serializer):
    user_input = serializers.CharField(required=True)
    username = serializers.CharField(read_only=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        user_input = attrs.get("user_input")

        if username_emial(user_input):
            try:
                user = User.objects.get(email=user_input, status=DONE)
                attrs["username"] = user.username  
                return attrs

            except User.DoesNotExist:
                raise serializers.ValidationError("Bunday emailli foydalanuvchi topilmadi")

        attrs["username"] = user_input
        return attrs

class UpdatePasswordSerializer(serializers.Serializer):
    password=serializers.CharField(required=True,min_length=6)
    reset_password=serializers.CharField(required=True,min_length=6)

    def validate(self, attrs):
        password=attrs.get("password")
        password2=attrs.get("reset_password")

        if password != password2:
            raise serializers.ValidationError('Passwords must be the same')
        return attrs
    

