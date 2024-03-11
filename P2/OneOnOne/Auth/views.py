from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import permission_classes
from drf_spectacular.utils import OpenApiResponse


@extend_schema(
    methods=["post"],
    request=UserSerializer,
    description="Register a new user",
    responses={
        status.HTTP_201_CREATED: OpenApiResponse(
            description="User created successfully"
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(description="Invalid data"),
    },
)
@permission_classes([permissions.AllowAny])
class RegisterUserAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User created successfully"}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
