from django.core.exceptions import ObjectDoesNotExist

from edc_base.view_mixins import EdcBaseViewMixin

from edc_dashboard.views import DashboardView as BaseDashboardView
from edc_navbar import NavbarViewMixin
from edc_subject_dashboard.view_mixins import SubjectDashboardViewMixin

from .dashboard_view_mixin import DashboardViewMixin
from ....model_wrappers import InformedConsentModelWrapper
from ....model_wrappers import AppointmentModelWrapper, ContactInformationModelWrapper, SubjectOffStudyModelWrapper
from edc_visit_schedule.site_visit_schedules import site_visit_schedules
from esr21_subject.models import OnSchedule, ScreeningEligibility
from django.shortcuts import redirect
from django.http import Http404
from django.apps import apps as django_apps


class DashboardView(DashboardViewMixin, EdcBaseViewMixin, SubjectDashboardViewMixin,
                    NavbarViewMixin, BaseDashboardView):
    dashboard_url = 'subject_dashboard_url'
    dashboard_template = 'subject_dashboard_template'
    appointment_model = 'edc_appointment.appointment'
    appointment_model_wrapper_cls = AppointmentModelWrapper
    consent_model = 'esr21_subject.informedconsent'
    consent_model_wrapper_cls = InformedConsentModelWrapper
    subject_locator_model = 'esr21_subject.personalcontactinfo'
    subject_locator_model_wrapper_cls = ContactInformationModelWrapper
    special_forms_include_value = "esr21_dashboard/subject/dashboard/special_forms.html"
    navbar_name = 'esr21_dashboard'
    navbar_selected_item = 'consented_subject'
    subject_locator_model = 'esr21_subject.personalcontactinfo'

    @property
    def subject_offstudy_wrapper(self):
        """
        - Used to create an instance of the subject offstudy if the offstudy form is filled,
        then pass the instance to the context so can be used in the special forms.
        - If not filled, a none object will returned so that the button cannot be rendered by the template
        """

        # getting the class for offstudy
        subject_offstudy_cls = django_apps.get_model('esr21_prn.subjectoffstudy')

        try:
            # get offstudy instance
            subject_offstudy_obj = subject_offstudy_cls.objects.get(subject_identifier=self.subject_identifier)
        except subject_offstudy_cls.DoesNotExist:
            # If the offstudy does not exist
            return None
        else:
            # create instance of the wrapper
            subject_offstudy_wrapper = SubjectOffStudyModelWrapper(model_obj=subject_offstudy_obj)

            # return instance so it can be used in the context
            return subject_offstudy_wrapper

    @property
    def appointments(self):
        """Returns a Queryset of all appointments for this subject.
        """
        if not self._appointments:
            self._appointments = self.appointment_model_cls.objects.filter(
                subject_identifier=self.subject_identifier).order_by(
                'visit_code')
        return self._appointments

    def get_onschedule_model_obj(self, schedule):
        try:
            return schedule.onschedule_model_cls.objects.get(
                subject_identifier=self.subject_identifier,
                schedule_name=schedule.name)
        except ObjectDoesNotExist:
            return None

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        locator_obj = self.get_locator_info()

        if 'main_schedule_enrollment' in self.request.path:
            self.main_schedule_enrollment()

        if 'sub_cohort_enrollment' in self.request.path:
            self.sub_cohort_enrollment()

        # import pdb; pdb.set_trace()

        context.update(
            locator_obj=locator_obj,
            subject_consent=self.consent_wrapped,
            schedule_names=[model.schedule_name for model in self.onschedule_models],
            is_subcohort_full=self.is_subcohort_full(),
            has_schedules=self.has_schedules(),
            subject_offstudy=self.subject_offstudy_wrapper
        )

        return context

    def get_locator_info(self):

        subject_identifier = self.kwargs.get('subject_identifier')
        try:
            obj = self.subject_locator_model_cls.objects.get(
                subject_identifier=subject_identifier)
        except ObjectDoesNotExist:
            return None
        return obj

    def set_current_schedule(self, onschedule_model_obj=None,
                             schedule=None, visit_schedule=None,
                             is_onschedule=True):
        if onschedule_model_obj:
            if is_onschedule:
                self.current_schedule = schedule
                self.current_visit_schedule = visit_schedule
                self.current_onschedule_model = onschedule_model_obj
                self.onschedule_models.append(onschedule_model_obj)
            self.visit_schedules.update(
                {visit_schedule.name: visit_schedule})

    def main_schedule_enrollment(self):
        cohort = 'esr21'
        onschedule_model = 'esr21_subject.onschedule'
        try:
            screening_eligibility = ScreeningEligibility.objects.get(subject_identifier=self.subject_identifier)
        except ObjectDoesNotExist:
            pass
        else:
            if screening_eligibility.is_eligible:
                self.put_on_schedule(f'{cohort}_enrol_schedule',
                                     onschedule_model=onschedule_model,
                                     onschedule_datetime=screening_eligibility.created.replace(microsecond=0))

                self.put_on_schedule(f'{cohort}_fu_schedule',
                                     onschedule_model=onschedule_model,
                                     onschedule_datetime=screening_eligibility.created.replace(microsecond=0))

    def sub_cohort_enrollment(self):
        cohort = 'esr21_sub'
        if not self.is_subcohort_full():
            onschedule_model = 'esr21_subject.onschedule'
            try:
                screening_eligibility = ScreeningEligibility.objects.get(subject_identifier=self.subject_identifier)
            except ObjectDoesNotExist:
                pass
            else:
                if screening_eligibility.is_eligible:
                    self.put_on_schedule(f'{cohort}_enrol_schedule',
                                         onschedule_model=onschedule_model,
                                         onschedule_datetime=screening_eligibility.created.replace(microsecond=0))

                    self.put_on_schedule(f'{cohort}_fu_schedule',
                                         onschedule_model=onschedule_model,
                                         onschedule_datetime=screening_eligibility.created.replace(microsecond=0))

    def put_on_schedule(self, schedule_name, onschedule_model, onschedule_datetime=None):
        _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
            onschedule_model=onschedule_model, name=schedule_name)
        schedule.put_on_schedule(
            subject_identifier=self.subject_identifier,
            onschedule_datetime=onschedule_datetime,
            schedule_name=schedule_name)

    def is_subcohort_full(self):
        onschedule_subcohort = OnSchedule.objects.filter(
            schedule_name='esr21_sub_enrol_schedule')
        return onschedule_subcohort.count() == 3000

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if 'main_schedule_enrollment' in self.request.path:
            url = self.request.path.split('main_schedule_enrollment')[0]
            return redirect(url)
        elif 'sub_cohort_enrollment' in self.request.path:
            url = self.request.path.split('sub_cohort_enrollment')[0]
            return redirect(url)
        else:
            return self.render_to_response(context)

    def has_schedules(self):
        onschedule = OnSchedule.objects.filter(
            subject_identifier=self.subject_identifier)
        return onschedule.count() > 0
