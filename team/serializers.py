from django.contrib.auth import get_user_model
from rest_framework import serializers

from team.models import Team
from user.serializers import UserSerializer

User = get_user_model()


class TeamSerializer(serializers.ModelSerializer):
    """
    Serializer class for Team objects.

    Attributes:
        leader (UserSerializer): A read-only field to serialize the team leader.
        member (UserSerializer): A read-only field to serialize the team members as a list.
    """
    leader = UserSerializer(read_only=True)
    member = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Team
        fields = '__all__'

    def create(self, validated_data):
        """
        Create a new Team object.

        Args:
            validated_data (dict): The validated data from the serialized request.
        Returns:
            Team: The newly created Team object.
        """
        # add an authorized user as a leader
        validated_data['leader'] = self.context['request'].user

        # create a new team
        team = Team.objects.create(**validated_data)

        return team
