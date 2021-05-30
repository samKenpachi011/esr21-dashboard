from edc_dashboard import UrlConfig

from .patterns import screening_identifier, subject_identifier
from .views import ScreeningListBoardView, SubjectListBoardView, DashboardView


app_name = 'esr21_dashboard'

screening_listboard_url_config = UrlConfig(
    url_name='screening_listboard_url',
    view_class=ScreeningListBoardView,
    label='screening_listboard',
    identifier_label='screening_identifier',
    identifier_pattern=screening_identifier)

subject_listboard_url_config = UrlConfig(
    url_name='subject_listboard_url',
    view_class=SubjectListBoardView,
    label='subject_listboard',
    identifier_label='subject_identifier',
    identifier_pattern=subject_identifier)

subject_dashboard_url_config = UrlConfig(
    url_name='subject_dashboard_url',
    view_class=DashboardView,
    label='subject_dashboard',
    identifier_label='subject_identifier',
    identifier_pattern=subject_identifier)

urlpatterns = []
urlpatterns += screening_listboard_url_config.listboard_urls
urlpatterns += subject_listboard_url_config.listboard_urls
urlpatterns += subject_dashboard_url_config.dashboard_urls
