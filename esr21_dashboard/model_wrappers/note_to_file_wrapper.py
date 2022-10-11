from django.conf import settings
from edc_model_wrapper import ModelWrapper


class NoteToFileModelWrapper(ModelWrapper):

    model = 'esr21_subject.notetofile'
    next_url_attrs = ['id']
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'note_to_file_listboard_url')
    querystring_attrs = ['id']
