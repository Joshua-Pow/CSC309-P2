from django.urls import path
from .views import CalendarListCreateAPIView, CalendarRetrieveUpdateDestroyAPIView

urlpatterns = [
    path("", CalendarListCreateAPIView.as_view(), name="calendars_list_create"),
    path(
        "<int:pk>/",
        CalendarRetrieveUpdateDestroyAPIView.as_view(),
        name="calendars_retrieve_update_delete",
    ),
]
