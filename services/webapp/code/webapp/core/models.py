import uuid
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User, Group
from django.utils import timezone

if 'sqlite' in settings.DATABASES['default']['ENGINE']:
    from .fields import JSONField
else:
    from django.contrib.postgres.fields import JSONField

# Setup logging
import logging
logger = logging.getLogger(__name__)


# All char model attributes are based on a 36 chars field. This is for making it easy to switch
# using an UUID pointing to some other model instead of the value in future, should this be necessary.

#=========================
#  Profile 
#=========================

class Profile(models.Model):

    uuid      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user      = models.OneToOneField(User, on_delete=models.CASCADE)
    auth      = models.CharField('User auth mode', max_length=36)
    timezone  = models.CharField('User Timezone', max_length=36, default='UTC')
    authtoken = models.CharField('User auth token', max_length=36, blank=True, null=True) # This is used for testing, not a login token.
    is_power_user = models.BooleanField('Power user status', default=False)
    extra_confs   = JSONField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.authtoken:
            self.authtoken = str(uuid.uuid4())
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return str('Profile of user "{}"'.format(self.user.email))

    def add_extra_conf(self, conf_type, object=None, value=None):
        if value in [None, '']: # TODO: improve me?
            raise ValueError('Empty value')
        if self.extra_confs is None:
            self.extra_confs = {}
        self.extra_confs[str(uuid.uuid4())] = {'type': conf_type, 'object_uuid': str(object.uuid), 'value': value}
        self.save()

    def get_extra_conf(self, conf_type, object=None):

        if self.extra_confs:
            for extra_conf in self.extra_confs:
                if conf_type == self.extra_confs[extra_conf]['type']:
                    if object:
                        #logger.debug("{} vs {}".format(self.extra_confs[extra_conf]['object_uuid'], str(object.uuid)))
                        if self.extra_confs[extra_conf]['object_uuid'] == str(object.uuid):
                            return self.extra_confs[extra_conf]['value']                        
                    else:
                        return self.extra_confs[extra_conf]['value']
        return None


#=========================
#  Login Token 
#=========================

class LoginToken(models.Model):

    uuid  = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user  = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField('Login token', max_length=36)

    def __str__(self):
        return str('Login token of user "{}"'.format(self.user.email))

