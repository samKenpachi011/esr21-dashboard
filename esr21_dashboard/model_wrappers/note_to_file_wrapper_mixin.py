from asyncio import protocols
from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .note_to_file_wrapper import NoteToFileModelWrapper

class NoteToFileWrapperMixin:
    
    note_to_file_model_wrapper_cls = NoteToFileModelWrapper
    
    
    @property
    def note_to_file_model_obj(self):
        try:
            return self.note_to_file_cls.objects.get(
                **self.note_to_file_options)
        except ObjectDoesNotExist:
            return None    
        
        
    @property
    def protocol_deviations(self):
        model_obj = self.note_to_file_model_obj or self.note_to_file_cls(
            **self.create_note_to_file_options
        )
        return self.note_to_file_model_wrapper_cls(model_obj=model_obj)
            
        
    @property
    def note_to_file_cls(self):
        return django_apps.get_model('esr21_subject.notetofile')
    

    @property
    def create_note_to_file_options(self):
        options = dict(
            note_to_file_id=self.id)
        return options
    
    
    @property
    def note_to_file_options(self):
        options = dict(
            note_to_file_id=self.id)
        return options