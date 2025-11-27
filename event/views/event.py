from rest_framework.generics import RetrieveUpdateDestroyAPIView,DestroyAPIView,ListAPIView,RetrieveAPIView
from rest_framework.views import APIView
from event.serializers import EventManagementSerialzier,TicketSerialzier,BookingDetailedSerializer
from event.permissions import IsAuthAndDone,IsAuthAndDoneAndOwner,IsAuthAndDoneAndOwnerForTicketClass
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from event.models import Event,Ticket,Booking
from event.utils import MyResponce
from drf_spectacular.utils import extend_schema
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


@extend_schema(tags=["Event Managements"])
class MangeEventAPIView(RetrieveUpdateDestroyAPIView):
    queryset=Event.objects.all()
    serializer_class = EventManagementSerialzier
    permission_classes = [IsAuthAndDoneAndOwner,IsAuthenticatedOrReadOnly]

@extend_schema(tags=["Event Managements"])
class CreateEventAPIView(APIView):
    serializer_class = EventManagementSerialzier
    permission_classes = [IsAuthAndDone,]
    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        return MyResponce.success(
            message="Event created successfully",
            data=serializer.data
        )

@extend_schema(
    tags=["Event Managements"],
    parameters=[
        {
            "name": "search",
            "description": "Search in title and description",
            "required": False,
            "type": "string",
            "in": "query"
        },
        {
            "name": "category",
            "description": "Filter by category",
            "required": False,
            "type": "string",
            "in": "query"
        },
        {
            "name": "address",
            "description": "Filter by address",
            "required": False,
            "type": "string",
            "in": "query"
        },
        {
            "name": "ordering",
            "description": "Order by date or created_at",
            "required": False,
            "type": "string",
            "in": "query",
            "example": "date"
        },
    ]
)
class AllEventsAPIView(ListAPIView):
    queryset = Event.objects.all()
    permission_classes = [IsAuthAndDone]
    serializer_class = EventManagementSerialzier

    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]

    filterset_fields = ['category', 'address']
    search_fields = ['title', 'description']

    ordering_fields = ['date', 'created_at']


    
@extend_schema(tags=["Tickets"])
class CreateTicket(APIView):
    serializer_class = TicketSerialzier
    permission_classes = [IsAuthAndDone,]
    def post(self,request,pk):
        event=Event.objects.filter(pk=pk).filter(user=request.user).first()
        if event:
            serializer=self.serializer_class(data=request.data,context={"pk":pk})
            serializer.is_valid(raise_exception=True)
            serializer.save(event=event)
            return MyResponce.success(
                message="Ticket created successfully",
                data=serializer.data
            )
        return MyResponce.error(f"There is not event with this id, or you don't have permission to perform this action")

@extend_schema(tags=["Tickets"])
class DeleteTicket(DestroyAPIView):
    permission_classes = [IsAuthAndDoneAndOwnerForTicketClass]
    queryset=Ticket.objects.all()
    serializer_class = TicketSerialzier
        
 

@extend_schema(tags=["Booking"])
class BookingAPIView(APIView):
    permission_classes=[IsAuthAndDone]
    def post(self,request,pk):
        ticket=Ticket.objects.filter(pk=pk).first()
        if ticket:
            if ticket.is_tickets_availbale() and ticket.is_expired():
                booking=Booking.objects.create(user=request.user,ticket=ticket)
                booking.decrease_seats_count()

                return MyResponce.success("Ticket Booked successfully")
            return MyResponce.error("No tickets available or expired")
        return MyResponce.error("No tickets found")             
    
@extend_schema(tags=["Booking"])
class MyBookings(APIView):
    permission_classes=[IsAuthAndDone]
    serializer_class=BookingDetailedSerializer
    def get(self,request):
        bookings=Booking.objects.filter(user=request.user)
        serializer=self.serializer_class(bookings,many=True)
       
        return MyResponce.success(
            message="all your bookings",
            data=serializer.data
        )

@extend_schema(tags=["Booking"])
class GetMybooking(RetrieveAPIView):
    queryset=Booking.objects.all()
    serializer_class=BookingDetailedSerializer
    permission_classes=[IsAuthAndDoneAndOwner]

@extend_schema(tags=["Booking"])
class DeleteMyBooking(DestroyAPIView):
    queryset=Booking.objects.all()
    serializer_class=BookingDetailedSerializer
    permission_classes=[IsAuthAndDoneAndOwner]








