from edc_dashboard import UrlConfig

from .patterns import screening_identifier
from .views import ScreeningListBoardView


app_name = 'esr21_dashboard'

screening_listboard_url_config = UrlConfig(
    url_name='screening_listboard_url',
    view_class=ScreeningListBoardView,
    label='screening_listboard',
    identifier_label='screening_identifier',
    identifier_pattern=screening_identifier)

urlpatterns = []
urlpatterns += screening_listboard_url_config.listboard_urls
