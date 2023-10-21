from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer class for User objects.

    Attributes:
        password (CharField): A write-only field for user password.
        confirm_password (CharField): A write-only field to confirm the user password.
    """
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'avatar', 'password', 'confirm_password')

    def create(self, validated_data):
        """
        Create a new User object.

        Args:
            validated_data (dict): The validated data from the serialized request.
        Returns:
            User: The newly created User object.
        Raises:
            serializers.ValidationError: If the password is missing or does not match the confirm_password field.
        """
        # extract the fields from validated_data or set it to None if absent
        password = validated_data.pop('password', None)
        confirm_password = validated_data.pop('confirm_password', None)

        # check that the 'password' field is not empty
        if password is None:
            raise serializers.ValidationError(
                {'password': 'Password is required for user creation.'}
            )
        # check that the 'password' matches the 'confirm_password' field
        if password != confirm_password:
            raise serializers.ValidationError(
                {'confirm_password': 'Password and confirm_password are different.'}
            )

        # create a new user
        user = User.objects.create_user(**validated_data, password=password)

        return user

    def update(self, instance, validated_data):
        if self.context['request'].data.get('avatar') == '':
            validated_data['avatar'] = None

        return super().update(instance, validated_data)

    def to_representation(self, instance):
        # Initialize the data dictionary with the default representation
        data = super().to_representation(instance)

        # !!!there is no error here, all checks are necessary.
        # instance.avatar checks whether the field is empty,
        # otherwise hasattr(instance.avatar, 'file') will have an execution
        if hasattr(instance, 'avatar') and instance.avatar and hasattr(instance.avatar, 'file'):
            data['avatar'] = instance.avatar.url
        else:
            # if the image does not exist, we send the image for the user by default
            data['avatar'] = settings.DEFAULT_USER_AVATAR_URL

        return data

    @staticmethod
    def validate_avatar(value):
        """
        Validate the size of the avatar image.
        """
        if value and value.size > (settings.USER_AVATAR_MAX_SIZE_MB * 1024 * 1024):
            raise serializers.ValidationError(f'Maximum image size allowed is {settings.USER_AVATAR_MAX_SIZE_MB} Mb')
        return value
