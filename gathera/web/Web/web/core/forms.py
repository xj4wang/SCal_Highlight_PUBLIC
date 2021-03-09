from crispy_forms.bootstrap import StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Column, Row, Field, Div
from django import forms
from django.db.models.fields import BLANK_CHOICE_DASH
from django.db.models import Q
from web.core.models import Session, SharedSession, Consent, Demographics, Questions
from web.topic.models import Topic
from web.users.models import User
from dal import autocomplete


class ConsentForm(forms.ModelForm):
    """
    Form for consenting to the experiment

    """
    submit_name = 'submit-consent-form'
    CONSENT_CHOICES = [('yes', 'YES'), ('no', 'NO')]
    consent = forms.ChoiceField(choices=CONSENT_CHOICES, widget=forms.RadioSelect(), label="", required=True) 
    
    class Meta:
        model = Consent        
        fields = ['consent']   
               

    def __init__(self, *args, **kwargs):
        super(ConsentForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout.append(
            Submit(self.submit_name, u'Submit',
                   css_class='btn btn-primary')
        )
        
class DemographicsForm(forms.ModelForm):
    """
    Form for consenting to the experiment

    """
    submit_name = 'submit-demographics-form'
    
    AGE_CHOICES = [('19 or younger', '19 or younger'), ('20 - 29', '20 - 29'), ('30 - 39', '30 - 39'), ('40 - 49', '40 - 49'), ('50 - 59', '50 - 59'), ('60 or older', '60 or older'), ('other', 'Other (please specify):'), ('na', 'I prefer not to answer.')]
    age_other = forms.CharField(label='Other (please specify):', required=False)
    age = forms.ChoiceField(choices=AGE_CHOICES, widget=forms.RadioSelect(), label="", required=True) 
    
    GENDER_CHOICES = [('female', 'Female'), ('male', 'Male'), ('other', 'Other (please specify):'), ('na', 'I prefer not to answer.')]
    gender_other = forms.CharField(label='Other (please specify):', required=False)
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect(), label="", required=True) 
    
    EDUCATION_CHOICES = [('lhs', 'Less than high school degree'), ('hs', 'High school degree or equivalent (e.g., GED)'), ('c', 'Some college but no degree'), ('a', 'Associate degree'), ('b', 'Bachelor degree'), ('m', 'Master degree'), ('p', 'Professional degree'), ('d', 'Doctorate degree'),('other', 'Other (please specify):'), ('na', 'I prefer not to answer.')]
    education_other = forms.CharField(label='Other (please specify):', required=False)
    education = forms.ChoiceField(choices=EDUCATION_CHOICES, widget=forms.RadioSelect(), label="", required=True)
    
    STUDY_CHOICES = [('anthropology', 'Anthropology'), ('archaeology','Archaeology'), ('history','History'), ('linguistics','Linguistics and languages'), ('philosophy','Philosophy'), ('religion','Religion'), ('culinary','Culinary arts'), ('literature','Literature'), ('performing','Performing arts'), ('visual','Visual arts'), ('economics','Economics'), ('geography','Geography'), ('interdisciplinary','Interdisciplinary studies'), ('area','Area studies'), ('ethic','Ethic and cultural studies'), ('gender','Gender and sexuality studies'), ('organizational','Organizational studies'), ('political','Political science'), ('psychology','Psychology'), ('sociology','Sociology'), ('biology','Biology'), ('chemistry','Chemistry'), ('earth','Earth sciences'), ('physics','Physics'), ('space','Space sciences'), ('cs','Computer sciences'), ('logic','Logic'), ('math','Mathematics'), ('pmath','Pure mathematics'), ('amath','Applied mathematics'), ('statistics','Statistics'), ('ss','System science'), ('other', 'Other (please specify):'), ('na', 'I prefer not to answer.')]
	
    study_other = forms.CharField(label='Other (please specify):', required=False)
    study = forms.MultipleChoiceField(choices=STUDY_CHOICES, widget=forms.CheckboxSelectMultiple(), label="", required=True)
    
    
    class Meta:
        model = Demographics        
        fields = ['age', 'age_other', 'gender', 'gender_other', 'education', 'education_other', 'study', 'study_other']   
               

    def __init__(self, *args, **kwargs):
        super(DemographicsForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout.append(
            Submit(self.submit_name, u'Submit',
                   css_class='btn btn-primary')
        )        

class QuestionsForm(forms.ModelForm):
    """
    Form for consenting to the experiment

    """
    submit_name = 'submit-questions-form'  
    QUESTION_CHOICES = [('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D'), ('e', 'E'), ('na', 'I prefer not to answer.')]
    q1 = forms.CharField(widget=forms.Select(choices=BLANK_CHOICE_DASH+QUESTION_CHOICES), label="", required=True)
    q2 = forms.CharField(widget=forms.Select(choices=BLANK_CHOICE_DASH+QUESTION_CHOICES), label="", required=True)
    q3 = forms.CharField(widget=forms.Select(choices=BLANK_CHOICE_DASH+QUESTION_CHOICES), label="", required=True)
    
    class Meta:
        model = Questions        
        fields = ['q1', 'q2', 'q3']   
               

    def __init__(self, *args, **kwargs):
        super(QuestionsForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout.append(
            Submit(self.submit_name, u'Submit',
                   css_class='btn btn-primary')
        )
        
class SessionPredefinedTopicForm(forms.ModelForm):
    """
    Form for creating Task with pre-defined topic

    """
    submit_name = 'submit-session-predefine-topic-form'
    prefix = "predefined"

    class Meta:
        model = Session
        exclude = ["username", "setting", "timespent", "last_activity"]
        help_texts = {
            'max_number_of_judgments': '(Optional) Set max number of judgments.',
            'strategy': "Discovery's strategy of retrieval.",
        }

    strategy = forms.ChoiceField(choices=Session.STRATEGY_CHOICES,
                                 label="Discovery's strategy",
                                 required=True)
    max_number_of_judgments = forms.IntegerField(required=False,
                                                 label="Effort",
                                                 help_text=Meta.help_texts.get(
                                                     'max_number_of_judgments'))

    def __init__(self, *args, **kwargs):
        super(SessionPredefinedTopicForm, self).__init__(*args, **kwargs)
        self.fields['topic'].queryset = Topic.objects.filter(~Q(number=None)).order_by('number')
        self.helper = FormHelper(self)

        self.helper.layout = Layout(
            'topic',
            Row(
                Column('max_number_of_judgments', css_class='form-group col-md-6 mb-0'),
                Column('strategy', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Div(
                Field('show_full_document_content'),
                css_class='d-none',
                css_id="predefined-show_full_document_content"
            ),
            StrictButton(u'Create session',
                         name=self.submit_name,
                         type="submit",
                         css_class='btn btn-outline-secondary')
        )

    def clean_max_number_of_judgments(self):
        data = self.cleaned_data['max_number_of_judgments']
        if not data:
            data = 0
        return data


class SessionForm(forms.ModelForm):
    """
    Form for creating Session

    """
    submit_name = 'submit-session-form'
    prefix = "topic"

    class Meta:
        model = Topic
        exclude = ["number", "display_description", "narrative"]

    max_number_of_judgments = forms.IntegerField(required=False,
                                                 label="Effort",
                                                 help_text=SessionPredefinedTopicForm.Meta.help_texts.get('max_number_of_judgments'))
    strategy = forms.ChoiceField(choices=Session.STRATEGY_CHOICES,
                                 label="Discovery's strategy",
                                 required=True,
                                 help_text=SessionPredefinedTopicForm.Meta.help_texts.get('strategy'))
    show_full_document_content = forms.BooleanField(required=False)
    judgments_file = forms.FileField(required=False, label='Optional seed judgments (csv file)')

    def __init__(self, *args, **kwargs):
        super(SessionForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs['rows'] = 4
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group col-md-4 mb-0'),
                Column('seed_query', css_class='form-group col-md-8 mb-0'),
                css_class='form-row'
            ),
            'description',
            Row(
                Column('max_number_of_judgments', css_class='form-group col-md-6 mb-0'),
                Column('strategy', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Div(
                Field('show_full_document_content'),
                css_class='d-none',
                css_id="topic-show_full_document_content"
            ),
            'judgments_file',
            StrictButton(u'Create session',
                         name=self.submit_name,
                         type="submit",
                         css_class='btn btn-outline-secondary')
            # Alternative to StrictButton
            # Submit(self.submit_name, u'Create topic and start judging',
            #       css_class='btn')
        )

    def clean_max_number_of_judgments(self):
        data = self.cleaned_data['max_number_of_judgments']
        if not data:
            data = 0
        return data


class ShareSessionForm(forms.ModelForm):
    """
    Form for sharing a session

    """
    submit_name = 'submit-share-session-form'
    prefix = "share"

    class Meta:
        model = SharedSession
        exclude = ["refers_to", "creator"]

    disallow_search = forms.BooleanField(required=False,
                                         label="Hide search from user")
    disallow_CAL = forms.BooleanField(required=False,
                                      label="Hide Discovery from user")

    def __init__(self, user, *args, **kwargs):
        super(ShareSessionForm, self).__init__(*args, **kwargs)
        self.fields['shared_with'] = forms.ModelChoiceField(
            label="Share with",
            queryset=User.objects.filter(~Q(pk=user.pk)),
            widget=autocomplete.ModelSelect2(url='users:user-autocomplete',
                                             attrs={
                                                 'data-placeholder': "username",
                                                 'data-minimum-input-length': 1,
                                             },
                                             )
        )
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'shared_with',
            'disallow_search',
            'disallow_CAL'
        )
