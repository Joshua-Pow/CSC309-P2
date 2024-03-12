from django.db import models


class Calendar(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]


class Day(models.Model):
    calendar = models.ForeignKey(
        Calendar, related_name="days", on_delete=models.CASCADE
    )
    date = models.DateField()
    ranking = models.IntegerField()

    class Meta:
        ordering = ["date"]
        unique_together = (
            "calendar",
            "ranking",
        )  # Enforcing unique ranking within a calendar
