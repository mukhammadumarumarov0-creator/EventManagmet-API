from rest_framework import serializers
from event.models import Event,Ticket,Booking

class EventManagementSerialzier(serializers.ModelSerializer):
    class Meta:
        model=Event
        fields=["title","description","date","address","category","seats_count"]

class TicketSerialzier(serializers.ModelSerializer):
    class Meta:
        model=Ticket
        fields = ["price","count"]

    def validate(self, attrs):
        if attrs.get("price") < 0 :
            raise serializers.ValidationError("Price cant't be nagative")
        if Ticket.objects.filter(event = self.context.get("pk")).exists():
             raise serializers.ValidationError("You have already created the ticket")
        return attrs




class MiniSerializer(serializers.ModelSerializer):
    class Meta:
        model=Event
        fields="__all__"

class UserMiniSerialzier(serializers.ModelSerializer):
    event=MiniSerializer()
    class Meta:
        model=Ticket
        fields="__all__"

class BookingDetailedSerializer(serializers.ModelSerializer):
    ticket=UserMiniSerialzier()
    class Meta:
        model=Booking
        fields="__all__"



 