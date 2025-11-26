from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
import random
import uuid

status=NEW,VERIFIED,DONE = ("new" , "verifed" , "done")


class User(AbstractUser):
    status_choice = (
        (NEW,NEW),
        (VERIFIED,VERIFIED),
        (DONE,DONE)
    )
    phone=models.CharField(max_length=13,null=True,blank=True)
    address=models.CharField(max_length=200,null=True,blank=True)
    status=models.CharField(max_length=15,choices=status_choice,default=NEW)
    image=models.ImageField(upload_to="users_photo/",validators=[FileExtensionValidator(allowed_extensions=["jpg","png","jpeg"])],null=True,blank=True) 
   
    def __str__(self):
        return self.username

    def get_token(self):
        token=RefreshToken.for_user(self)

        tokens={
            "refresh_token":str(token),
            "access_token":str(token.access_token)
        }
        return tokens

    def get_verify_code(self):
        code = "".join(str(random.randint(0,10000) % 10)for _ in range(4))
        UserConfirmation.objects.create(
            user_id=self.id,
            code=code
        )
        return code
        
    def save(self,*args, **kwargs):
        if not self.username:
            username=f"username-{uuid.uuid4()}"
            self.username=username
        if not self.password:
            password=f"password-{uuid.uuid4()}"
            self.password=password
            self.set_password(self.password)

        return super(User,self).save(*args, **kwargs)


class UserConfirmation(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="confirmations")
    code=models.CharField(max_length=4)
    expired_time=models.DateTimeField()
    
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s code"

    def save(self,*args, **kwargs):
        self.expired_time=timezone.now()+timezone.timedelta(minutes=4)
        return super().save(*args, **kwargs)
    
    def is_expired(self):
        if self.expired_time > timezone.now():
            return True #vaqti bor
        return False #vaqti otib keti
