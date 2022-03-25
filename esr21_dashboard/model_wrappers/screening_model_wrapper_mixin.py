from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .screening_eligibility_wrapper import ScreeningEligibilityModelWrapper


class ScreeningModelWrapperMixin:

    screening_model_wrapper_cls = ScreeningEligibilityModelWrapper

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
    def screening(self):
        """"Returns a wrapped saved or unsaved caregiver locator
        """
        model_obj = self.screening_model_obj or self.screening_cls(
            **self.create_screening_cls_options)
        return ScreeningEligibilityModelWrapper(model_obj=model_obj)

    @property
    def screening_cls(self):
        return django_apps.get_model('esr21_subject.screeningeligibility')

    @property
    def create_screening_cls_options(self):
        """Returns a dictionary of options to create a new
        unpersisted caregiver locator model instance.
        """
        options = dict(
            subject_identifier=self.subject_identifier)
        return options

    @property
    def screening_options(self):
        """Returns a dictionary of options to get an existing
        caregiver locator model instance.
        """
        options = dict(
            subject_identifier=self.subject_identifier)
        return options
