import factory
from django.contrib.auth import get_user_model
from factory import Faker, LazyAttribute, PostGenerationMethodCall, Sequence, SubFactory
from factory.django import DjangoModelFactory

from team.models import Team

User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = Sequence(lambda n: f'test_user_{n}')
    first_name = Sequence(lambda n: f'Test_{n}')
    last_name = Sequence(lambda n: f'User_{n}')
    email = LazyAttribute(lambda obj: f'test_{obj.username}@example.com')
    password = PostGenerationMethodCall('set_password', 'test_password')


class TeamFactory(DjangoModelFactory):
    class Meta:
        model = Team

    leader = SubFactory(UserFactory)
    name = Sequence(lambda n: f'Team_{n}')
    description = Faker('text')

    @factory.post_generation
    def member(self, create, extracted, **kwargs):
        if not create or not extracted:
            # Simple build, or nothing to add, do nothing.
            return

        # Add the iterable of groups using bulk addition
        self.member.add(*extracted)
