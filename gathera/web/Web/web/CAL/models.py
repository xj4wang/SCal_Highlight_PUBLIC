from config.settings.base import AUTH_USER_MODEL as User

from django.contrib.postgres.fields import JSONField
from django.db import models

from web.core.models import Session


class Stratum(models.Model):
    class Meta:
        unique_together = ['user', 'stratum_num', 'session']
        index_together = ['user', 'stratum_num', 'session']

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)

    stratum_size = models.IntegerField(null=False, blank=False)
    stratum_num = models.IntegerField(null=False, blank=False)
    sample_size = models.IntegerField(null=False, blank=False)

    T = models.IntegerField(null=False, blank=False)
    N = models.IntegerField(null=False, blank=False)
    R = models.IntegerField(null=False, blank=False)

    sampled_docs = JSONField(null=False, blank=True, default=list)
    stratum_docs = JSONField(null=False, blank=True, default=dict)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __unicode__(self):
        return "Session: {} - Stratum Number: {}".format(self.session, self.stratum_num)

    def __str__(self):
        return self.__unicode__()
