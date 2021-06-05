from django.conf import settings

from edc_model_wrapper import ModelWrapper


class ContactInformationModelWrapper(ModelWrapper):

    model = 'esr21_subject.personalcontactinfo'
    querystring_attrs = ['screening_identifier', 'subject_identifier',
                         'first_name', 'last_name']
    next_url_attrs = ['screening_identifier', 'subject_identifier']
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'subject_dashboard_url')
