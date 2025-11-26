from django.contrib import admin
from .models import User,UserConfirmation,Event,Ticket,Booking

admin.site.register([User,UserConfirmation,Event,Ticket,Booking])
