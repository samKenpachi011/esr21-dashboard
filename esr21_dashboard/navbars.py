from django.conf import settings
from edc_navbar import NavbarItem, site_navbars, Navbar


no_url_namespace = True if settings.APP_NAME == 'esr21_dashboard' else False

esr21_dashboard = Navbar(name='esr21_dashboard')

esr21_dashboard.append_item(
    NavbarItem(
        name='eligible_subject',
        title='Subject Screening',
        label='Subject Screening',
        fa_icon='fa fa-user-plus',
        url_name=settings.DASHBOARD_URL_NAMES.get('screening_listboard_url'),
        no_url_namespace=no_url_namespace))

esr21_dashboard.append_item(
    NavbarItem(
        name='consented_subject',
        title='Subjects',
        label='Subjects',
        fa_icon='fa fa-user-plus',
        url_name=settings.DASHBOARD_URL_NAMES.get('subject_listboard_url'),
        no_url_namespace=no_url_namespace))

site_navbars.register(esr21_dashboard)
