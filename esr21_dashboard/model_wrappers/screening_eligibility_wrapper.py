from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from edc_base.utils import get_uuid
from edc_model_wrapper import ModelWrapper

from edc_consent import ConsentModelWrapperMixin

from .informed_consent_model_wrapper import InformedConsentModelWrapper
import logging


class ScreeningEligibilityModelWrapper(ModelWrapper):

    model = 'esr21_subject.screeningeligibility'
    next_url_attrs = ['subject_identifier']
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'screening_listboard_url')
    querystring_attrs = ['subject_identifier']
