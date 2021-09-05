from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = 'esr21_dashboard'
    admin_site_name = 'esr21_subject_admin'
