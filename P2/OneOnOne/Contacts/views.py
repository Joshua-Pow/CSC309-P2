from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Contact
from .serializers import ContactSerializer
from django.db.models import Q

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['post'], url_path='add')
    def add(self, request):
        userA = request.user
        userB_username = request.data.get('username', None)
        if not userB_username:
            return Response({"error": "Username is required."}, status=status.HTTP_400_BAD_REQUEST)
        userB = get_object_or_404(User, username=userB_username)
        if userA == userB:
            return Response({"error": "You cannot add yourself."}, status=status.HTTP_400_BAD_REQUEST)
        contact_exists = Contact.objects.filter(Q(userA=userA, userB=userB)|Q(userA=userB, userB=userA)).exists()
        if contact_exists:
            contact_blocked = Contact.objects.filter(Q(userA=userA, userB=userB, status=4)|Q(userA=userB, userB=userA, status=4)).exists()
            if contact_blocked:
                return Response({"error": "This contact is blocked and cannot be added."}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({"error": "This contact already exists."}, status=status.HTTP_409_CONFLICT)
        contact = Contact(userA=userA, userB=userB, status=2)
        contact.save()
        serializer = self.get_serializer(contact)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'], url_path='friends')
    def friends(self, request):
        user = request.user
        contacts = Contact.objects.filter(Q(userA=user)|Q(userB=user),status=1)
        

        #clean up data to easier to work with in frontend
        friend_ids = set()
        for contact in contacts:
            if contact.userA == user:
                friend_ids.add(contact.userB_id)
            elif contact.userB == user:
                friend_ids.add(contact.userA_id)
        friends = User.objects.filter(id__in=friend_ids)
        friends_cleaned = [{"id": friend.id, "username": friend.username} for friend in friends]
        return Response(friends_cleaned)
    
    @action(detail=False, methods=['get'], url_path='incoming')
    def incoming(self, request):
        user = request.user
        contacts = Contact.objects.filter(userB=user, status=2)

        #clean up data to easier to work with in frontend
        incoming_ids = [contact.userA_id for contact in contacts]
        incoming_users = User.objects.filter(id__in=incoming_ids)
        incoming_cleaned = [{"id": user.id, "username": user.username} for user in incoming_users]
        return Response(incoming_cleaned)
    
    @action(detail=False, methods=['get'], url_path='outgoing')
    def outgoing(self, request):
        user = request.user
        contacts = Contact.objects.filter(userA=user, status=2)

        #clean up data to easier to work with in frontend
        incoming_ids = [contact.userB_id for contact in contacts]
        incoming_users = User.objects.filter(id__in=incoming_ids)
        incoming_cleaned = [{"id": user.id, "username": user.username} for user in incoming_users]
        return Response(incoming_cleaned)

    @action(detail=False, methods=['post'], url_path='accept')
    def accept(self, request):
        userB_username = request.data.get('username', None)
        if not userB_username:
            return Response({"error": "Username is required."}, status=status.HTTP_400_BAD_REQUEST)
        userBlookup = get_object_or_404(User, username=userB_username)
        contact = Contact.objects.filter(userA=userBlookup, userB=request.user, status=2).first() # will only be one but errors if not a check to make sure its 1
        if not contact:
            return Response({"error": "No pending request from this user."}, status=status.HTTP_404_NOT_FOUND)
        contact.status = 1
        contact.save()
        return Response({"message": "Friend request accepted."})
    
    @action(detail=False, methods=['post'], url_path='reject')
    def reject(self, request):
        userB_username = request.data.get('username', None)
        if not userB_username:
            return Response({"error": "Username is required."}, status=status.HTTP_400_BAD_REQUEST)
        userBlookup = get_object_or_404(User, username=userB_username)
        contact = Contact.objects.filter(userA=userBlookup, userB=request.user, status=2).first() # will only be one but errors if not a check to make sure its 1
        if not contact:
            return Response({"error": "No pending request from this user."}, status=status.HTTP_404_NOT_FOUND)
        contact.status = 3
        contact.save()
        return Response({"message": "Friend request rejected."})