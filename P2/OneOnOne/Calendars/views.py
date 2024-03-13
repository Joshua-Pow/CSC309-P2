from rest_framework import generics
from .models import Calendar
from .serializers import CalendarSerializer
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema_view, extend_schema
from drf_spectacular.utils import OpenApiResponse
from rest_framework.exceptions import PermissionDenied


@extend_schema_view(
    list=extend_schema(
        description="List all calendars",
        responses={200: OpenApiResponse(response=CalendarSerializer(many=True))},
    ),
    create=extend_schema(
        description="Create a new calendar",
        responses={201: OpenApiResponse(response=CalendarSerializer)},
    ),
)
class CalendarListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CalendarSerializer
    queryset = Calendar.objects.all()

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


@extend_schema_view(
    retrieve=extend_schema(
        description="Retrieve a calendar",
        responses={200: OpenApiResponse(response=CalendarSerializer)},
    ),
    update=extend_schema(
        description="Update a calendar",
        responses={204: OpenApiResponse(response=CalendarSerializer)},
    ),
    destroy=extend_schema(
        description="Delete a calendar",
        responses={204: OpenApiResponse(response=CalendarSerializer)},
    ),
)
@extend_schema(
    methods=["patch"],
    exclude=True,
)
class CalendarRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CalendarSerializer
    queryset = Calendar.objects.all()

    def update(self, request, *args, **kwargs):
        calendar = self.get_object()
        if calendar.creator != request.user:
            raise PermissionDenied("You do not have permission to edit this calendar.")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        calendar = self.get_object()
        if calendar.creator != request.user:
            raise PermissionDenied(
                "You do not have permission to delete this calendar."
            )
        return super().destroy(request, *args, **kwargs)
