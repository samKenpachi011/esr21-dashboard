from django.conf import settings
from edc_model_wrapper import ModelWrapper

from .contact_information_model_wrapper_mixin import ContactInformationWrapperMixin


class InformedConsentModelWrapper(ContactInformationWrapperMixin, ModelWrapper):

    model = 'esr21_subject.informedconsent'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'screening_listboard_url')
    next_url_attrs = ['screening_identifier']
    querystring_attrs = ['screening_identifier', 'subject_identifier']
