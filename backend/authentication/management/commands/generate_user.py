"""
Generate a fake user for testing purposes.
"""
from django.core.management.base import BaseCommand
from authentication.models import User

from faker import Faker

fake = Faker()

class Command(BaseCommand):
    help = 'Generate a fake user for testing purposes.'

    def add_arguments(self, parser):
        parser.add_argument('num', type=int, help='Number of users to create (default: 10)', default=10)

    def handle(self, *args, **options):
        num = options.get('num') or 10
        for _ in range(num):
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password=fake.password(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                is_active=True,
                bio=fake.text()[:100],
                birth_date=fake.date_of_birth(),
                location=fake.country(),
                is_private=fake.boolean(),
            )
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully created user {user.username}'))