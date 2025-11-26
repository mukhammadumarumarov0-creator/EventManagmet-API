from django.urls import path
from event.views import StartRegistration,VerificationProccess,FullUpadteUser

urlpatterns = [
    path("registration/",StartRegistration.as_view()),
    path("verification/",VerificationProccess.as_view()),
    path("update_user/",FullUpadteUser.as_view()),

]
