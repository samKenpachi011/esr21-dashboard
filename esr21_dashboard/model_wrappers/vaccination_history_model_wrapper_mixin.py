from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .vaccination_history_model_wrapper import VaccinationHistoryModelWrapper


class VaccinationHistoryModelWrapperMixin:

    vaccination_history_cls = VaccinationHistoryModelWrapper

    @property
    def vaccination_history_model_obj(self):
        """Returns a vaccination history model instance or None.
        """
        try:
            return self.vaccination_history_model_cls.objects.get(
                **self.vaccination_history_options)
        except ObjectDoesNotExist:
            return None

    @property
    def vaccination_history(self):
        """"Returns a wrapped saved or unsaved vaccination history
        """
        model_obj = self.vaccination_history_model_obj or self.vaccination_history_model_cls(
            **self.create_vaccination_history_options)
        return self.vaccination_history_cls(model_obj=model_obj)

    @property
    def vaccination_history_model_cls(self):
        return django_apps.get_model('esr21_subject.vaccinationhistory')

    @property
    def create_vaccination_history_options(self):
        """ Returns a dictionary of options to create a new
            unpersisted vaccination history model instance.
        """
        options = dict(
            subject_identifier=self.subject_identifier)
        return options

    @property
    def vaccination_history_options(self):
        """ Returns a dictionary of options to get an existing
            vaccination history model instance.
        """
        options = dict(
            subject_identifier=self.subject_identifier)
        return options
