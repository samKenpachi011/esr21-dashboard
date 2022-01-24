from django.conf import settings
from edc_model_wrapper import ModelWrapper


class SubjectOffStudyModelWrapper(ModelWrapper):
    model = 'esr21_prn.subjectoffstudy'
    querystring_attrs = ['subject_identifier', ]
    next_url_attrs = ['subject_identifier',]
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'subject_dashboard_url')
