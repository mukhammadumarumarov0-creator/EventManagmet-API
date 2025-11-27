from django.urls import path
from event.views import StartRegistration,VerificationProccess,FullUpadteUser,LoginUser,UpdatePassword,ResendVerificationCode,\
MangeEventAPIView,CreateEventAPIView,CreateTicket,DeleteTicket,AllEventsAPIView,BookingAPIView,MyBookings,DeleteMyBooking,GetMybooking


urlpatterns = [
    path("registration/",StartRegistration.as_view()),
    path("verification/",VerificationProccess.as_view()),
    path("update_user/",FullUpadteUser.as_view()),
    path("login/",LoginUser.as_view()),
    path("update_password/",UpdatePassword.as_view()),
    path("resend_code/",ResendVerificationCode.as_view()),


    path("create_event/",CreateEventAPIView.as_view()),
    path("event_management/<int:pk>",MangeEventAPIView.as_view()),
    path("api/events/", AllEventsAPIView.as_view(), name="search-events"),
   

    path("create_ticket/<int:pk>",CreateTicket.as_view()),
    path("delete_ticket/<int:pk>",DeleteTicket.as_view()),


    path("booking_ticket/<int:pk>/",BookingAPIView.as_view()),
    path("my_bookings/",MyBookings.as_view()),
    path("my_booking/<int:pk>",GetMybooking.as_view()),
    path("delete_booking/<int:pk>",DeleteMyBooking.as_view()),

]
