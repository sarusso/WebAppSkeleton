from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ...models import Profile

class Command(BaseCommand):
    help = 'Adds the admin superuser with \'a\' password.'

    def handle(self, *args, **options):

        try:
            testuser = User.objects.get(username='testuser')
            print('Not creating test user as it already exists')

        except User.DoesNotExist:
            print('Creating test user with default password')
            testuser = User.objects.create_user('testuser', 'testuser@web.app', 'testpass')
            print('Making testuser admin')
            testuser.is_staff = True
            testuser.is_admin=True
            testuser.is_superuser=True
            testuser.save() 
            print('Creating testuser profile')
            Profile.objects.create(user=testuser, auth='local', authtoken='361cab94-124a-4476-947c-aaa4349b4a91')
