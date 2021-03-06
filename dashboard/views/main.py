import base64
from functools import cmp_to_key

import pygogo
from braces.views import LoginRequiredMixin, StaffuserRequiredMixin
from django.contrib import messages
from django.contrib.admin.models import LogEntry, CHANGE
from django.http import HttpResponse
from django.views.generic import TemplateView, FormView
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook

from dashboard.data.partner_mapping import load_file
from dashboard.forms import FileUploadForm, MappingUploadForm, Dhis2ImportForm
from dashboard.helpers import F3, F2, F1, sort_cycle
from dashboard.models import (
    Score,
    LocationToPartnerMapping,
    FacilityTest,
    TracingFormulations,
)
from dashboard.tasks import import_data_from_dhis2, run_manual_import
from dashboard.utils import log_formatter, should_log_time


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        return context


class AboutPageView(TemplateView):
    template_name = "about.html"


class AboutTestPageView(TemplateView):
    template_name = "about_tests.html"

    def get_context_data(self, **kwargs):
        context = super(AboutTestPageView, self).get_context_data(**kwargs)
        context["tests"] = FacilityTest.objects.all()
        return context


class AboutBackground(TemplateView):
    template_name = "about_background.html"


class AboutHowWorks(TemplateView):
    template_name = "about_works.html"


class AboutHowUsed(TemplateView):
    template_name = "about_used.html"


logger = pygogo.Gogo(__name__, low_formatter=log_formatter).get_logger()
logger.setLevel("INFO" if should_log_time() else "ERROR")


class Dhis2ImportView(LoginRequiredMixin, StaffuserRequiredMixin, FormView):
    template_name = "import_dhis2.html"
    form_class = Dhis2ImportForm
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super(Dhis2ImportView, self).get_context_data(**kwargs)
        context["title"] = "Import Data For Cycle from DHIS2"
        return context

    def form_valid(self, form):
        cycles = form.cleaned_data["cycle"]
        logger.info(
            "launching task",
            extra={"task_name": "import_data_from_dhis2", "periods": cycles},
        )
        for cycle in cycles:
            import_data_from_dhis2.apply_async(args=[cycle], priority=2)
        LogEntry.objects.create(
            user_id=self.request.user.id,
            action_flag=CHANGE,
            change_message="Started Import for cycle %s from dhis2" % (cycles),
        )
        messages.add_message(
            self.request,
            messages.INFO,
            "Successfully started import for cycles %s" % (cycles),
        )
        return super(Dhis2ImportView, self).form_valid(form)


def serialize_upload_file(import_file):
    return base64.b64encode(import_file.read())


class DataImportView(LoginRequiredMixin, StaffuserRequiredMixin, FormView):
    template_name = "import.html"
    form_class = FileUploadForm
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super(DataImportView, self).get_context_data(**kwargs)
        context["title"] = "Import Data For Cycle"
        return context

    def form_valid(self, form):
        import_file = form.cleaned_data["import_file"]
        cycle = form.cleaned_data["cycle"]
        run_manual_import.apply_async(
            args=[cycle, serialize_upload_file(import_file)], priority=1
        )
        messages.add_message(
            self.request,
            messages.INFO,
            "Successfully started import for cycle %s" % cycle,
        )
        return super(DataImportView, self).form_valid(form)


class PartnerMappingImportPage(LoginRequiredMixin, StaffuserRequiredMixin, FormView):
    template_name = "partner-mapping.html"
    form_class = MappingUploadForm
    success_url = "/import/mapping"

    def get_context_data(self, **kwargs):
        context = super(PartnerMappingImportPage, self).get_context_data(**kwargs)
        context["title"] = "Update the Partner to Facility Mapping"
        return context

    def form_valid(self, form):
        import_file = form.cleaned_data["import_file"]
        mapping = load_file(import_file)
        LocationToPartnerMapping.objects.all().delete()
        LocationToPartnerMapping.objects.create(mapping=mapping)
        messages.add_message(
            self.request, messages.INFO, "Successfully updated the partner mapping"
        )
        return super(PartnerMappingImportPage, self).form_valid(form)


def download_mapping(request):
    excel_data = [["Name", "IP"]]

    for location, partner in LocationToPartnerMapping.get_mapping().items():
        excel_data.append([location, partner])

    wb = Workbook()
    ws = wb.active
    for line in excel_data:
        ws.append(line)

    response = HttpResponse(
        save_virtual_workbook(wb),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = "attachment; filename=partner_mapping.xlsx"

    return response


DEFAULT = "DEFAULT"


class ReportsView(LoginRequiredMixin, TemplateView):
    template_name = "scores_table.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ReportsView, self).get_context_data(*args, **kwargs)
        access_level = self.request.user.access_level
        access_area = self.request.user.access_area
        qs_filter = {}
        if access_level and access_area:
            qs_filter[access_level.lower()] = access_area
        qs = Score.objects.filter(**qs_filter)
        ips = qs.values("ip").order_by("ip").distinct()
        warehouses = qs.values("warehouse").order_by("warehouse").distinct()
        checks = FacilityTest.objects.all()
        districts = qs.values("district").order_by("district").distinct()
        raw_cycles = [c[0] for c in qs.values_list("cycle").distinct()]
        cycles = sorted(raw_cycles, key=cmp_to_key(sort_cycle), reverse=True)
        context["districts"] = districts
        context["ips"] = ips
        context["warehouses"] = warehouses
        context["cycles"] = cycles
        context["checks"] = checks
        context["formulations"] = TracingFormulations.objects.all()
        return context
