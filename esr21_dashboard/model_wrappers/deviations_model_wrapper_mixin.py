from asyncio import protocols
from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .deviations_model_wrapper import ProtocolDeviationsModelWrapper

class ProtocolDeviationsWrapperMixin:
    
    protocol_deviations_model_wrapper_cls = ProtocolDeviationsModelWrapper
    
    
    @property
    def protocol_deviations_model_obj(self):
        """Returns a protocol deviations model instance or None.
        """
        try:
            return self.protocol_deviations_cls.objects.get(
                **self.protocol_deviations_options)
        except ObjectDoesNotExist:
            return None    
        
        
    @property
    def protocol_deviations(self):
        """Returns a wrapped saved or unsaved protocol deviation.
        """
        model_obj = self.protocol_deviations_model_obj or self.protocol_deviations_cls(
            **self.create_protocol_deviations_options
        )
        return self.protocol_deviations_model_wrapper_cls(model_obj=model_obj)
            
        
    @property
    def protocol_deviations_cls(self):
        return django_apps.get_model('esr21_subject.protocoldeviations')
    

    @property
    def create_protocol_deviations_options(self):
        """ Returns a dictionary of options to create a new
            unpersisted personal contact information model instance.
        """
        options = dict(
            deviation_id=self.id)
        return options
    
    
    @property
    def protocol_deviations_options(self):
        """ Returns a dictionary of options to get an existing
           protocol deviations instance.
        """
        # dev_opt = super().me
        options = dict(
            deviation_id=self.id)
        return options