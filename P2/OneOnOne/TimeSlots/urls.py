from django.urls import path
from .views import AllTimeSlotView, CreateTimeSlotView

urlpatterns = [
    path("all/", AllTimeSlotView.as_view(), name="all_timeslots"),
    path("create/", CreateTimeSlotView.as_view(), name="create_timeslot")
]
