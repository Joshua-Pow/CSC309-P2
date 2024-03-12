from django.urls import path
from .views import TimeSlotListCreateAPIView, TimeSlotRetrieveUpdateDestroyAPIView

urlpatterns = [
    path("", TimeSlotListCreateAPIView.as_view(), name="C_timeslot"),
    path("<int:pk>/", TimeSlotRetrieveUpdateDestroyAPIView.as_view(), name="RUD_timeslot")
]
