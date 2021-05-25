from urllib.parse import urlencode, unquote

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()


@register.inclusion_tag('esr21_dashboard/buttons/eligibility_confirmation_button.html')
def eligibility_confirmation_button(model_wrapper):
    title = ['Edit eligibility confirmation form.']
    return dict(
        screening_identifier=model_wrapper.object.screening_identifier,
        href=model_wrapper.href,
        title=' '.join(title))


@register.inclusion_tag('esr21_dashboard/buttons/eligibility_button.html')
def eligibility_button(model_wrapper):
    comment = []
    obj = model_wrapper.object
    tooltip = None
    if not obj.is_eligible:
        comment = obj.ineligibility.split(',')
    comment = list(set(comment))
    comment.sort()
    return dict(eligible=obj.is_eligible, comment=comment,
                tooltip=tooltip, obj=obj)


@register.inclusion_tag('esr21_dashboard/buttons/dashboard_button.html')
def dashboard_button(model_wrapper):
    subject_dashboard_url = settings.DASHBOARD_URL_NAMES.get(
        'subject_dashboard_url')
    return dict(
        subject_dashboard_url=subject_dashboard_url,
        subject_identifier=model_wrapper.subject_identifier)
