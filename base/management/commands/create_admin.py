from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates an admin user with the specified username and password'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Username for the admin user')
        parser.add_argument('--password', type=str, help='Password for the admin user')

    def handle(self, *args, **options):
        username = options.get('username') or 'trpadmin'
        password = options.get('password') or 'trp12345'

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'User "{username}" already exists.')
            )
            # Update the existing user to be admin
            user = User.objects.get(username=username)
            user.set_password(password)
            user.is_staff = True
            user.is_superuser = True
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f'Updated existing user "{username}" to admin with new password.')
            )
        else:
            User.objects.create_superuser(
                username=username,
                email='',  # Django requires email but can be empty
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created admin user "{username}"')
            )

