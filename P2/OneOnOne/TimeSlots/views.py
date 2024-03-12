from drf_spectacular.utils import extend_schema
from rest_framework import permissions
from drf_spectacular.utils import OpenApiResponse
from .serializers import TimeSlotSerializer
from .models import TimeSlot
from rest_framework import generics
from Calendars.models import Day
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied


@extend_schema(
    methods=["post"],
    request=TimeSlotSerializer,
)
class TimeSlotListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TimeSlotSerializer
    queryset = TimeSlot.objects.all()

    def perform_create(self, serializer):
        day_id = self.kwargs.get("day_id")
        print(day_id)
        day = get_object_or_404(Day, id=day_id)
        print(day)
        print("user: ", self.request.user)
        serializer.save(day=day, owner=self.request.user)

    @extend_schema(
        description="Create a new time slot",
        responses={201: OpenApiResponse(response=TimeSlotSerializer)},
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @extend_schema(
        description="List all timeslots",
        responses={200: OpenApiResponse(response=TimeSlotSerializer(many=True))},
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


@extend_schema(
    methods=["get", "put", "delete"],
    request=TimeSlotSerializer,
)
@extend_schema(
    methods=["patch"],
    exclude=True,
)
class TimeSlotRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TimeSlotSerializer
    queryset = TimeSlot.objects.all()

    def get_queryset(self):
        """
        This view should return a list of all the time slots
        for the currently authenticated user.
        """
        user = self.request.user
        return TimeSlot.objects.filter(owner=user)

    def perform_update(self, serializer):
        """
        Check if the user is the owner of the time slot before updating.
        """
        timeslot = self.get_object()
        if timeslot.owner != self.request.user:
            raise PermissionDenied("You do not have permission to edit this time slot.")
        serializer.save()

    def perform_destroy(self, instance):
        """
        Check if the user is the owner of the time slot before deleting.
        """
        if instance.owner != self.request.user:
            raise PermissionDenied(
                "You do not have permission to delete this time slot."
            )
        instance.delete()

    @extend_schema(
        description="Retrieve a time slot",
        responses={200: OpenApiResponse(response=TimeSlotSerializer)},
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        description="Update a time slot",
        responses={204: OpenApiResponse(response=TimeSlotSerializer)},
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(
        description="Delete a time slot",
        responses={204: OpenApiResponse(response=TimeSlotSerializer)},
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
