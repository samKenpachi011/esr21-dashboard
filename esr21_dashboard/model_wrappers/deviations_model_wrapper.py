from django.conf import settings
from edc_model_wrapper import ModelWrapper


class ProtocolDeviationsModelWrapper(ModelWrapper):

    model = 'esr21_subject.protocoldeviations'
    next_url_attrs = ['id']
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'protocol_deviations_listboard_url')
    querystring_attrs = ['id']
