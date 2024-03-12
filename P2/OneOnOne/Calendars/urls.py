from django.urls import path
from .views import CalendarListCreateAPIView, CalendarRetrieveUpdateDestroyAPIView
from TimeSlots.views import (
    TimeSlotListCreateAPIView,
    TimeSlotRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path("", CalendarListCreateAPIView.as_view(), name="calendars_list_create"),
    path(
        "<int:pk>/",
        CalendarRetrieveUpdateDestroyAPIView.as_view(),
        name="calendars_retrieve_update_delete",
    ),
    path(
        "<int:calendar_id>/day/<int:day_id>/timeslot/",
        TimeSlotListCreateAPIView.as_view(),
        name="timeslot_list_create",
    ),
    path(
        "<int:calendar_id>/day/<int:day_id>/timeslot/<int:pk>/",
        TimeSlotRetrieveUpdateDestroyAPIView.as_view(),
        name="timeslot_detail",
    ),
]
