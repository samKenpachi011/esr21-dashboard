import re

from django.db.models import Q
from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import ListboardFilterViewMixin, SearchFormViewMixin
from edc_dashboard.views import ListboardView
from edc_navbar import NavbarViewMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


from ...model_wrappers import ProtocolDeviationsModelWrapper


class ListBoardView(EdcBaseViewMixin, NavbarViewMixin,
                    ListboardFilterViewMixin, SearchFormViewMixin,
                    ListboardView):
    
    listboard_template = 'protocol_deviations_listboard_template'
    listboard_url = 'protocol_deviations_listboard_url'
    listboard_panel_style = 'success' 
    listboard_fa_icon = "far fa-user-circle"
    
    model = 'esr21_subject.protocoldeviations'
    model_wrapper_cls = ProtocolDeviationsModelWrapper
    navbar_name = 'esr21_dashboard'
    navbar_selected_item = 'protocol_deviations'
    search_form_url = 'protocol_deviations_listboard_url'
    
    
    
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            protocol_deviation_add_url=self.model_cls().get_absolute_url())
        return context


    # def get_queryset_filter_options(self, request, *args, **kwargs):
    #     options = super().get_queryset_filter_options(request, *args, **kwargs)
    #     if kwargs.get('deviation_id'):
    #         options.update(
    #             {'deviation_id': kwargs.get('deviation_id')})
    #     return options

    # def extra_search_options(self, search_term):
    #     q = Q()
    #     if re.match('^[A-Z]+$', search_term):
    #         q = Q(deviation_name__exact=search_term)
    #     return q