from django.conf import settings
from edc_model_wrapper import ModelWrapper

from .subject_consent_wrapper_mixin import SubjectConsentWrapperMixin

from .informed_consent_model_wrapper import InformedConsentModelWrapper
from .screening_model_wrapper_mixin import ScreeningModelWrapperMixin
from .vaccination_history_model_wrapper_mixin import VaccinationHistoryModelWrapperMixin
from .screen_out_wrapper_mixin import ScreeningOutWrapperMixin
from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from edc_base.utils import get_uuid


class SubjectScreeningModelWrapper(ScreeningModelWrapperMixin,
                                   SubjectConsentWrapperMixin,
                                   VaccinationHistoryModelWrapperMixin,
                                   ScreeningOutWrapperMixin,
                                   ModelWrapper):

    consent_model_wrapper_cls = InformedConsentModelWrapper
    model = 'esr21_subject.eligibilityconfirmation'
    next_url_attrs = ['screening_identifier', 'subject_identifier']
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'screening_listboard_url')

    @property
    def consented(self):
        return self.object.subject_identifier

    @property
    def consent_model_obj(self):
        """Returns a consent model instance or None.
        """
        consent_model_cls = django_apps.get_model(self.consent_model_wrapper_cls.model)
        try:
            return consent_model_cls.objects.get(**self.consent_options)
        except ObjectDoesNotExist:
            return None

    @property
    def create_consent_options(self):
        options = super().create_consent_options

        options.update(
            screening_identifier=self.screening_identifier,
            consent_identifier=get_uuid(),
            version=self.consent_version)

        return options

    @property
    def subject_identifier(self):
        consent_model = self.consent_model_obj
        if consent_model:
            return consent_model.subject_identifier
        return None
