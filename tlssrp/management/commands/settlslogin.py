from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, UNUSABLE_PASSWORD

from safebook.tlssrp.models import SRPUserInfo

class Command(BaseCommand):
    args = '<username> <password>'
    help = 'Sets the TLS login for the specified user ' \
           '(creating the user if it does not exist)'

    def handle(self, *args, **options):
        if len(args) != 2:
            raise CommandError("must specify username and password")
        username = args[0]
        password = args[1]
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User(username=username, password=UNUSABLE_PASSWORD)
            user.save()
        try:
            srpinfo = SRPUserInfo.objects.get(user=user)
        except SRPUserInfo.DoesNotExist:
            srpinfo = SRPUserInfo(user=user)
        srpinfo.set_from_password(password)
        srpinfo.save()
        
        
