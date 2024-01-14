"""
Generate a fake user for testing purposes.
"""
from django.core.management.base import BaseCommand
from post.models import Post
from authentication.models import User

from faker import Faker

fake = Faker()

class Command(BaseCommand):
    help = 'Generate a fake user for testing purposes.'

    def add_arguments(self, parser):
        parser.add_argument(
            'num', type=int, help='Number of post to create (default: 50)',
            default=50
        )

    def handle(self, *args, **options):
        num = options.get('num') or 50
        users = User.objects.all()
        for _ in range(num):
            post = Post.objects.create(
                author=users[fake.random_int(0, len(users) - 1)],
                body=fake.text()
            )
            post.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully created post {post.body}'))