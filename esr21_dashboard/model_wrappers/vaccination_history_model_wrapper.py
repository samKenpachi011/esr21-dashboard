from django.conf import settings
from edc_model_wrapper import ModelWrapper


class VaccinationHistoryModelWrapper(ModelWrapper):

    model = 'esr21_subject.vaccinationhistory'
    next_url_attrs = ['subject_identifier']
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'screening_listboard_url')

    @property
    def querystring_attrs(self):
        options = ['subject_identifier', ]
        prefil_fields = ['received_vaccine', 'dose_quantity',
                         'dose1_product_name', 'dose1_date',
                         'dose2_product_name', 'dose2_date',
                         'dose3_product_name', 'dose3_date', ]
        options.extend(prefil_fields)
        return options
