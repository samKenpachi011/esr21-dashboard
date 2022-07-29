import re

from django.db.models import Q
from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import ListboardFilterViewMixin, SearchFormViewMixin
from edc_dashboard.views import ListboardView
from edc_navbar import NavbarViewMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.urls.base import reverse

from django.http.response import HttpResponseRedirect


class ReportViewError(Exception):
    pass

from ...model_wrappers import NoteToFileModelWrapper


class ListBoardView(NavbarViewMixin,EdcBaseViewMixin,
                    ListboardFilterViewMixin, SearchFormViewMixin,
                    ListboardView):
    
    listboard_template = 'note_to_file_listboard_template'
    listboard_url = 'note_to_file_listboard_url'
    listboard_panel_style = 'info' 
    listboard_fa_icon = "fa-user-plus"
    
    model = 'esr21_subject.notetofile'
    model_wrapper_cls = NoteToFileModelWrapper
    navbar_name = 'esr21_dashboard'
    navbar_selected_item = 'note_to_files'
    ordering = '-modified'
    paginate_by = 10
    search_form_url = 'note_to_file_listboard_url'
    
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            note_to_files_add_url=self.model_cls().get_absolute_url())
        return context

    def get_queryset_filter_options(self, request, *args, **kwargs):
        options = super().get_queryset_filter_options(request, *args, **kwargs)
        if kwargs.get('id'):
            options.update(
                {'note_to_file_id': kwargs.get('id')})
        return options

    def extra_search_options(self, search_term):
        q = Q()
        if re.match('^[A-Z]+$', search_term):
            q = Q(note_to_file_name__exact=search_term)
        return q
    
    def post(self, request, *args, **kwargs):

        if request.method == 'POST':
            try:
                url_name = request.url_name_data['note_to_file_listboard_url']
            except KeyError as e:
                raise ReportViewError(
                    f'Invalid action.')
            url = reverse(url_name, kwargs=kwargs)
            return HttpResponseRedirect(url)