from rest_framework import serializers
from event.models import User

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