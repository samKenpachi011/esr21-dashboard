from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from edc_model_wrapper import ModelWrapper

from .contact_information_model_wrapper_mixin import ContactInformationWrapperMixin


class InformedConsentModelWrapper(ContactInformationWrapperMixin, ModelWrapper):

    model = 'esr21_subject.informedconsent'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'screening_listboard_url')
    next_url_attrs = ['screening_identifier']
    querystring_attrs = ['screening_identifier', 'subject_identifier']

    @property
    def screening_cls(self):
        return django_apps.get_model('esr21_subject.screeningeligibility')

    @property
    def screening_model_obj(self):
        """Returns a caregiver locator model instance or None.
        """
        try:
            return self.screening_cls.objects.get(
                **self.screening_options)
        except ObjectDoesNotExist:
            return None

    @property
    def screening_options(self):
        """Returns a dictionary of options to get an existing
        caregiver locator model instance.
        """
        options = dict(
            subject_identifier=self.subject_identifier)
        return options

    @property
    def is_eligible(self):
        if self.screening_model_obj:
            return self.screening_model_obj.is_eligible
        return False

    @property
    def reasons_ineligible(self):
        if self.screening_model_obj:
            return self.screening_model_obj.ineligibility
        return False
