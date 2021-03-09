from config.settings.base import AUTH_USER_MODEL as User

from django.contrib.postgres.fields import JSONField
from django.db import models

from web.core.models import Session


class Judgment(models.Model):
    class Meta:
        unique_together = ['user', 'doc_id', 'session']
        index_together = ['user', 'doc_id', 'session']

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)

    doc_id = models.CharField(null=False, blank=False, max_length=512)
    doc_title = models.TextField(null=False, blank=False)
    doc_CAL_snippet = models.TextField(null=True, blank=True)
    doc_search_snippet = models.TextField(null=True, blank=True)
    query = models.TextField(null=True, blank=True)

    # 2 indicates high level,
    # 1 for medium/low,
    # and 0 for not matching the judging criteria.
    class JudgingChoices(models.IntegerChoices):
        HIGHLY_RELEVANT = (2, 'Highly Relevant')
        RELEVANT = (1, 'Relevant')
        NON_RELEVANT = (0, 'Non-Relevant')

    # A judgment can have null fields if its only been viewed but not judged.
    # This field is the main judging criteria used to update the ML models
    relevance = models.IntegerField(verbose_name='Relevance',
                                    choices=JudgingChoices.choices,
                                    null=True, blank=True)
    # Field to store other criteria specified by user
    additional_judging_criteria = JSONField(null=True, blank=True, default=dict)

    # method used to make the judgment: click/keyboard
    method = models.CharField(null=True, blank=True, max_length=64)

    # source of judgment: search/searchModal/CAL/...
    source = models.CharField(null=True, blank=True, max_length=64)
    # was this document part of the seed judgments file
    is_seed = models.BooleanField(default=False)

    # Search query and Ctrl+F terms related fields
    search_query = models.TextField(null=True, blank=True)
    ctrl_f_terms_input = models.TextField(null=True, blank=True)
    found_ctrl_f_terms_in_title = JSONField(null=True, blank=True, default=list)
    found_ctrl_f_terms_in_summary = JSONField(null=True, blank=True, default=list)
    found_ctrl_f_terms_in_full_doc = JSONField(null=True, blank=True, default=list)

    # history of active and away time spent on the document
    historyVerbose = JSONField(null=True, blank=True, default=list, verbose_name="History")

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "{} on {}: {}".format(self.user, self.doc_id, self.relevance)

    def __str__(self):
        return self.__unicode__()
