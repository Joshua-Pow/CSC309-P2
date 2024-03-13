from rest_framework import generics
from .models import Invitation
from .serializers import InvitationSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from Calendars.models import Calendar
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiResponse
from Calendars.models import Participant


@extend_schema(
    methods=["get", "post"],
    request=InvitationSerializer,
)
class InvitationListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InvitationSerializer

    def get_queryset(self):
        return Invitation.objects.all()

    def perform_create(self, serializer):
        calendar_id = self.kwargs.get("calendar_id")
        calendar = get_object_or_404(Calendar, id=calendar_id)

        serializer.save(
            calendar=calendar,
            inviter=self.request.user,
            invitee_username=self.request.data["invitee_username"],
        )

    @extend_schema(
        description="Retrieve an invitations",
        responses={200: OpenApiResponse(response=InvitationSerializer(many=True))},
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        description="Create an invitation",
        responses={201: OpenApiResponse(response=InvitationSerializer)},
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class InvitationChangeStatusAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InvitationSerializer

    def get_queryset(self):
        user = self.request.user

        queryset = Invitation.objects.filter(Q(invitee=user) | Q(inviter=user))
        return queryset

    def perform_update(self, serializer):
        invitation = self.get_object()

        serializer.update(invitation, self.request.data)
        if invitation.status == "accepted":
            # Add invitee as a participant to the calendar
            Participant.objects.create(
                user=self.request.user, calendar=invitation.calendar
            )

    def destroy(self, request, *args, **kwargs):
        invitation = self.get_object()
        print(invitation)

        if invitation.inviter != request.user:
            raise PermissionDenied(
                "You do not have permission to delete this invitation."
            )

        return super().destroy(request, *args, **kwargs)

    @extend_schema(
        description="Retrieve an invitation",
        request=InvitationSerializer,
        responses={200: OpenApiResponse(response=InvitationSerializer)},
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        description="Delete an invitation",
        request=InvitationSerializer,
        responses={204: OpenApiResponse(response=InvitationSerializer)},
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    @extend_schema(
        description="Update an invitation",
        request=InvitationSerializer,
        responses={204: OpenApiResponse(response=InvitationSerializer)},
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
