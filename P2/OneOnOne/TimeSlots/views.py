from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import permission_classes
from drf_spectacular.utils import OpenApiResponse
from .serializers import TimeSlotSerializer
from .models import TimeSlot
from rest_framework import generics

@extend_schema(
    methods=["post"],
    request=TimeSlotSerializer,
)
class TimeSlotListCreateAPIView(APIView):
    serializer_class = TimeSlotSerializer
    queryset = TimeSlot.objects.all()

    @extend_schema(
        description="Create a new time slot",
        responses={201: OpenApiResponse(response=TimeSlotSerializer)},
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

@extend_schema(
    methods=["get", "put", "delete"],
    request=TimeSlotSerializer,
)
class TimeSlotRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TimeSlotSerializer
    queryset = TimeSlot.objects.all()

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
    
# @permission_classes([permissions.AllowAny])   
# class CreateTimeSlotView(APIView):
#     permission_classes = [permissions.AllowAny]

#     def post(self, request):
#         # need to insert calendar and owner to data
#         # request.data
#         serializer = TimeSlotSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 {"message": "Time slot created successfully"}, status=status.HTTP_201_CREATED
#             )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
