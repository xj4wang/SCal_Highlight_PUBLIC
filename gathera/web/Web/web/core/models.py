from config.settings.base import AUTH_USER_MODEL as User
import uuid

from django.apps import apps
from django.db import models

from web.CAL.exceptions import CALError
from web.interfaces.CAL import functions as CALFunctions
from web.topic.models import Topic

class Consent(models.Model):    
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    consent = models.CharField(null=False, blank=False, max_length=512)

    def __unicode__(self):
        return "{} {}".format(self.consent, self.username)

    def __str__(self):
        return self.__unicode__()
        
class Demographics(models.Model):    
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    age = models.CharField(null=False, blank=False, max_length=512)
    gender = models.CharField(null=False, blank=False, max_length=512)
    education = models.CharField(null=False, blank=False, max_length=512)
    study = models.CharField(null=False, blank=False, max_length=512)
    
    age_other = models.CharField(null=False, blank=False, max_length=512)
    gender_other = models.CharField(null=False, blank=False, max_length=512)
    education_other = models.CharField(null=False, blank=False, max_length=512)
    study_other = models.CharField(null=False, blank=False, max_length=512)
        
    def __unicode__(self):
        return "{} {} {} {} {} {} {} {} {}".format(self.study_other, self.education_other, self.gender_other, self.age_other, self.study, self.education, self.gender, self.age, self.username)

    def __str__(self):
        return self.__unicode__()  

class Questions(models.Model):    
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    q1 = models.CharField(null=False, blank=False, max_length=512)
    q2 = models.CharField(null=False, blank=False, max_length=512)
    q3 = models.CharField(null=False, blank=False, max_length=512) 
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    
    def __unicode__(self):
        return "{} {} {} {} {}".format(self.q3, self.q2, self.q1, self.topic, self.username)

    def __str__(self):
        return self.__unicode__()        

class Session(models.Model):
    STRATEGY_CHOICES = (
        # ('doc', 'Document (CAL)'),
        # ('para', 'Paragraph (CAL)'),
        ('doc_scal', 'Document (S-CAL)'),
        # ('para_scal', 'Paragraph (S-CAL)'),
    )

    username = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4,
                            editable=False)

    # max number of judgments you wish for this task. 0 or negative to have no max.
    max_number_of_judgments = models.IntegerField(null=False, blank=False)
    max_number_of_judgments_reached = models.BooleanField(default=False)

    strategy = models.CharField(max_length=64,
                                choices=STRATEGY_CHOICES,
                                null=False,
                                blank=False,
                                default='doc_scal')
    # For paragraphs strategies
    show_full_document_content = models.BooleanField(null=False,
                                                     blank=False)
    # whether this session is being shared with other people
    is_shared = models.BooleanField(null=True, blank=True, default=False)
    # current task active time (in seconds)
    timespent = models.FloatField(default=0)
    # last activity timestamp
    last_activity = models.FloatField(default=None, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True,
                                      editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def begin_session_in_cal(self):
        try:
            judgments = self.judgment_set.all()
            judgments_list = [(j.doc_id, j.relevance) for j in judgments]
            CALFunctions.add_session(str(self.uuid),
                                     self.topic.seed_query,
                                     self.strategy,
                                     judgments_list)
        except (CALError, ConnectionRefusedError, Exception) as e:
            # TODO: log error
            pass

    def is_summary(self):
        return "para" in self.strategy

    def get_judgments(self):
        return apps.get_model('judgment.Judgment').objects.filter(session__uuid=self.uuid)

    def __unicode__(self):
        return "<User:{}, Num:{}>".format(self.username, self.topic.number)

    def __str__(self):
        return self.__unicode__()


class SharedSession(models.Model):

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    refers_to = models.ForeignKey(Session, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator')
    shared_with = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_with')

    disallow_search = models.BooleanField(null=True, blank=True, default=False)
    disallow_CAL = models.BooleanField(null=True, blank=True, default=False)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "<Shared by:{} to {}>".format(self.creator, self.shared_with)

    def __str__(self):
        return self.__unicode__()
