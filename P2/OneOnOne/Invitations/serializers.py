from rest_framework import serializers
from .models import Invitation
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.exceptions import PermissionDenied


class InvitationSerializer(serializers.ModelSerializer):
    invitee_username = serializers.SerializerMethodField()
    inviter = serializers.HiddenField(default=serializers.CurrentUserDefault())
    inviter_username = serializers.SerializerMethodField()
    calendar_id = serializers.PrimaryKeyRelatedField(read_only=True)
    status = serializers.CharField(read_only=True)

    def get_inviter_username(self, obj) -> str:
        return obj.inviter.username

    def get_invitee_username(self, obj) -> str:
        return obj.invitee.username

    def validate_status(self, value):
        if value not in ["pending", "accepted", "rejected"]:
            raise serializers.ValidationError("Invalid status")
        return value

    def validate_invitee_username(self, value):
        # Find the User instance based on the username provided
        try:
            user = User.objects.get(username=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist")
        return user

    def create(self, validated_data):
        invitee_username = validated_data.pop("invitee_username")
        invitee = get_object_or_404(User, username=invitee_username)
        calendar = validated_data["calendar"]

        # Check if the current user is the creator of the calendar
        if validated_data["inviter"] != calendar.creator:
            raise PermissionDenied("Only the calendar creator can send invitations.")
        if calendar.creator == invitee:
            raise PermissionDenied("You cannot send an invitation to yourself.")

        invitation = Invitation.objects.create(**validated_data, invitee=invitee)
        return invitation

    def update(self, instance, validated_data):
        if instance.invitee != self.context["request"].user:
            raise PermissionDenied(
                "You do not have permission to change the status of this invitation."
            )

        instance.status = validated_data.get("status", instance.status)
        instance.save()
        return instance

    class Meta:
        model = Invitation
        fields = [
            "id",
            "calendar_id",
            "invitee_username",
            "inviter_username",
            "inviter",
            "status",
        ]
