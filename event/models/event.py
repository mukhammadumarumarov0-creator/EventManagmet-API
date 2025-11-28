from django.db import models
from .user import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models import F

category=SOCIAL,EDUCATIONAL,BUSINESS,ONLINE,OTHER = ("social","educational","business","online","other")

def not_past(value):
    if value < timezone.now():
        raise ValidationError("Data is expired")


class Event(models.Model):
    category_choice = [
        (SOCIAL, SOCIAL),
        (EDUCATIONAL, EDUCATIONAL),
        (BUSINESS, BUSINESS),
        (ONLINE, ONLINE),
        (OTHER , OTHER),
        ]
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='events')
    title=models.CharField(max_length=200,null=True)
    description=models.CharField(max_length=500,null=True,blank=True)
    date=models.DateTimeField(validators=[not_past],null=True,blank=True)
    address=models.CharField(max_length=500)
    category=models.CharField(max_length=20,choices=category_choice,default=SOCIAL)
    seats_count=models.PositiveIntegerField(null=True,blank=True)

    updated_at=models.DateTimeField(auto_now=True)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s event"  
    
    def is_expired(self):
        if self.date > timezone.now():
            return False #vaqti bor 
        return True #vaqti otib keti expired bolib keti
  
    
class Ticket(models.Model):
    event=models.ForeignKey(Event,on_delete=models.CASCADE,related_name="tickets")
    price=models.IntegerField()
    count=models.PositiveIntegerField(default=0)

    updated_at=models.DateTimeField(auto_now=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event}'s ticket"
     
    def is_tickets_availbale(self):
        if self.count > 0 :
            return True # agar bosa True qaytadi
        return False # agar yoq bosa False qaytadi
    
    def decrease_count(self,count=1):
        if self.count >= count:
            self.count -= count
            self.save(update_fields=['count'])
            return True # agar True qaytsa seat minus boldi  
        return False
    
    def is_expired(self):
        if not self.event.is_expired():
            return True #vaqti bor
        return False # otib keti


class Booking(models.Model):
    ticket=models.ForeignKey(Ticket,on_delete=models.CASCADE,related_name="bookings")
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='bookings')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.ticket.user.username}'s booking"
    
    def decrease_seats_count(self, n=1):
        return self.ticket.decrease_count(n)
    
    def is_expired_booking(self):
        if self.ticket.is_expired():
            return True #vaqti bor
        return False #vaqti otib keti

