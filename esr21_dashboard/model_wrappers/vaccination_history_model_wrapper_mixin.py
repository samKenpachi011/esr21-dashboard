from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from edc_constants.constants import YES

from .vaccination_history_model_wrapper import VaccinationHistoryModelWrapper


class VaccinationHistoryModelWrapperMixin:

    vaccination_history_cls = VaccinationHistoryModelWrapper
    vaccination_details_model = 'esr21_subject.vaccinationdetails'

    @property
    def vaccination_details_cls(self):
        return django_apps.get_model(self.vaccination_details_model)

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

        vd = self.vaccination_details_cls.objects.filter(
            subject_visit__subject_identifier=self.subject_identifier)

        if vd:
            options.update(received_vaccine=YES, dose_quantity=vd.count())
        for detail in vd:
            dose = self.selected_dose(vacc_detail=detail)
            options.update(
                {f'dose{dose}_product_name': 'azd_1222',
                 f'dose{dose}_date': detail.vaccination_date.date().strftime('%d %B %Y')})
        return options

    @property
    def vaccination_history_options(self):
        """ Returns a dictionary of options to get an existing
            vaccination history model instance.
        """
        options = dict(
            subject_identifier=self.subject_identifier)
        return options

    def selected_dose(self, vacc_detail=None):
        if vacc_detail.received_dose_before == 'first_dose':
            return '1'
        elif vacc_detail.received_dose_before == 'second_dose':
            return '2'
        elif vacc_detail.received_dose_before == 'booster_dose':
            return '3'
