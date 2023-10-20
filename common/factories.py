from django.contrib.auth import get_user_model
from factory import LazyAttribute, PostGenerationMethodCall, Sequence
from factory.django import DjangoModelFactory

User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = Sequence(lambda n: f'test_user_{n}')
    first_name = Sequence(lambda n: f'Test_{n}')
    last_name = Sequence(lambda n: f'User_{n}')
    email = LazyAttribute(lambda obj: f'test_{obj.username}@example.com')
    password = PostGenerationMethodCall('set_password', 'test_password')
