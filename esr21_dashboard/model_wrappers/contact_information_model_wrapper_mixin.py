from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .contact_information_model_wrapper import ContactInformationModelWrapper


class ContactInformationWrapperMixin:

    contact_information_model_wrapper_cls = ContactInformationModelWrapper

    @property
    def contact_information_model_obj(self):
        """Returns a personal contact information model instance or None.
        """
        try:
            return self.contact_information_cls.objects.get(
                **self.contact_information_options)
        except ObjectDoesNotExist:
            return None

    @property
    def contact_information(self):
        """Returns a wrapped saved or unsaved personal contact information.
        """
        model_obj = self.contact_information_model_obj or self.contact_information_cls(
            **self.create_contact_information_options)
        return self.contact_information_model_wrapper_cls(model_obj=model_obj)

    @property
    def contact_information_cls(self):
        return django_apps.get_model('esr21_subject.personalcontactinfo')

    @property
    def create_contact_information_options(self):
        """ Returns a dictionary of options to create a new
            unpersisted personal contact information model instance.
        """
        options = dict(
            subject_identifier=self.subject_identifier)
        return options

    @property
    def contact_information_options(self):
        """ Returns a dictionary of options to get an existing
            personal contact information instance.
        """
        options = dict(
            subject_identifier=self.subject_identifier)
        return options
