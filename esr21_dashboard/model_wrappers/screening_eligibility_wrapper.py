from django.conf import settings
from edc_model_wrapper import ModelWrapper


class ScreeningEligibilityModelWrapper(ModelWrapper):

    model = 'esr21_subject.screeningeligibility'
    next_url_attrs = ['subject_identifier']
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'screening_listboard_url')
    querystring_attrs = ['subject_identifier']
