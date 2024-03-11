from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import permission_classes
from drf_spectacular.utils import OpenApiResponse
from .serializers import TimeSlotSerializer
from .models import TimeSlot


# @extend_schema(
#     methods=["post"],
#     request=TimeSlotSerializer,
#     description="Create a new time slot",
#     responses={
#         status.HTTP_201_CREATED: OpenApiResponse(
#             description="Timeslot created successfully"
#         ),
#         status.HTTP_400_BAD_REQUEST: OpenApiResponse(description="Invalid data"),
#     },
# )
# @permission_classes([permissions.AllowAny])
# class RegisterUserAPIView(APIView):
#     permission_classes = [permissions.AllowAny]

#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 {"message": "User created successfully"}, status=status.HTTP_201_CREATED
#             )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([permissions.AllowAny])   
class AllTimeSlotView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        # calendar = Calendar.objects.get(id=kwargs['calendar_id'])
        # timeslots = calendar.timeslot_set.all().filter(calendar = calendar)
        #   OR
        # timeslots = TimeSlot.objects.all().filter(calendar=calendar)
        # need a try/except for two queries above
        # return Response(
        #       {"message": timeslots, status=status.HTTP_200_CREATED
        # )
        pass
    
    
@permission_classes([permissions.AllowAny])   
class CreateTimeSlotView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        # need to insert calendar and owner to data
        # request.data
        serializer = TimeSlotSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Time slot created successfully"}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
