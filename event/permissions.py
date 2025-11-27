from rest_framework.permissions import BasePermission
from event.models import VERIFIED,DONE

class IsAuthDoneOrVerified(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
              return False
        if not request.method in ["GET", "PUT", "DELETE", "POST", "PATCH"]:
              return False
        
        return request.user.status in [VERIFIED,DONE]

class IsAuthAndDone(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
              return False
        if not request.method in ["GET", "PUT", "DELETE", "POST", "PATCH"]:
              return False
        
        return request.user.status == DONE

class IsAuthAndDoneAndOwner(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
              return False
        if not request.method in ["GET", "PUT", "DELETE", "POST", "PATCH"]:
              return False
        
        return request.user.status == DONE
    
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class IsAuthAndDoneAndOwnerForTicketClass(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
              return False
        if not request.method in ["GET", "PUT", "DELETE", "POST", "PATCH"]:
              return False
        
        return request.user.status == DONE
    
    def has_object_permission(self, request, view, obj):
        return obj.event.user == request.user
    
    
        