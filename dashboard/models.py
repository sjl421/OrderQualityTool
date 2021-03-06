import json
import logging

from ckeditor.fields import RichTextField
from custom_user.models import AbstractEmailUser
from django.db import models
from django.db.models import CharField
from django_extensions.db.fields import AutoSlugField
from jsonfield import JSONField
from ordered_model.models import OrderedModel
from picklefield import PickledObjectField
from pymaybe import maybe

from dashboard.data.partner_mapping import FormattedKeyDict
from dashboard.helpers import NOT_REPORTING, YES, NO, REPORT_TYPES
from dashboard.widget import TestDefinitionField

MOH_CENTRAL = "MOH CENTRAL"

IIP = "IP"

DISTRICT = "District"

WAREHOUSE = "Warehouse"

logger = logging.getLogger(__name__)
CONSUMPTION = "CONSUMPTION"
LOCATION = "Facility Index"
MAUL = "MAUL"
JMS = "JMS"
NMS = "NMS"

WAREHOUSES = ((MAUL, MAUL), (JMS, JMS), (NMS, NMS))


class DashboardUser(AbstractEmailUser):
    access_level = CharField(
        choices=(
            (WAREHOUSE, WAREHOUSE),
            (DISTRICT, DISTRICT),
            (IIP, IIP),
            (MOH_CENTRAL, MOH_CENTRAL),
        ),
        max_length=50,
    )
    access_area = CharField(max_length=250, null=True, blank=True)

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    class Meta:
        app_label = "dashboard"
        verbose_name_plural = "Users"


class Cycle(models.Model):
    title = models.CharField(max_length=256, db_index=True, unique=True)
    state = PickledObjectField()

    def __unicode__(self):
        return "%s" % (self.title)


choices = ((YES, YES), (NO, NO), (NOT_REPORTING, NOT_REPORTING))


class Score(models.Model):
    name = models.CharField(max_length=256, db_index=True)
    cycle = models.CharField(max_length=256, db_index=True)
    district = models.CharField(max_length=256, db_index=True)
    ip = models.CharField(max_length=256, db_index=True)
    warehouse = models.CharField(max_length=256, db_index=True)
    data = JSONField()
    default_fail_count = models.IntegerField(default=0)
    default_pass_count = models.IntegerField(default=0)
    f1_fail_count = models.IntegerField(default=0)
    f1_pass_count = models.IntegerField(default=0)
    f2_fail_count = models.IntegerField(default=0)
    f2_pass_count = models.IntegerField(default=0)
    f3_fail_count = models.IntegerField(default=0)
    f3_pass_count = models.IntegerField(default=0)

    class Meta:
        unique_together = ("name", "cycle", "district", "ip", "warehouse")


class Consumption(models.Model):
    name = models.CharField(max_length=256, db_index=True)
    cycle = models.CharField(max_length=256, db_index=True)
    district = models.CharField(max_length=256, db_index=True)
    ip = models.CharField(max_length=256, db_index=True)
    warehouse = models.CharField(max_length=256, db_index=True)
    opening_balance = models.FloatField(null=True, blank=True)
    quantity_received = models.FloatField(null=True, blank=True)
    consumption = models.FloatField(null=True, blank=True)
    loses_adjustments = models.FloatField(null=True, blank=True)
    closing_balance = models.FloatField(null=True, blank=True)
    months_of_stock_on_hand = models.FloatField(null=True, blank=True)
    days_out_of_stock = models.FloatField(null=True, blank=True)
    quantity_required_for_current_patients = models.FloatField(null=True, blank=True)
    estimated_number_of_new_patients = models.FloatField(null=True, blank=True)
    estimated_number_of_new_pregnant_women = models.FloatField(null=True, blank=True)
    packs_ordered = models.FloatField(null=True, blank=True)
    notes = models.CharField(max_length=256, null=True, blank=True)
    formulation = models.CharField(max_length=256, null=True, blank=True, db_index=True)

    def __unicode__(self):
        return "%s %s" % (self.cycle, self.formulation)

    class Meta:
        verbose_name_plural = "Consumption Records"


class AdultPatientsRecord(models.Model):
    name = models.CharField(max_length=256, db_index=True)
    cycle = models.CharField(max_length=256, db_index=True)
    district = models.CharField(max_length=256, db_index=True)
    ip = models.CharField(max_length=256, db_index=True)
    warehouse = models.CharField(max_length=256, db_index=True)
    existing = models.FloatField(null=True, blank=True)
    new = models.FloatField(null=True, blank=True)
    formulation = models.CharField(max_length=256, null=True, blank=True)

    def __unicode__(self):
        return "%s %s" % (self.cycle, self.formulation)

    class Meta:
        verbose_name_plural = "Adult Patient Records"


class PAEDPatientsRecord(models.Model):
    name = models.CharField(max_length=256, db_index=True)
    cycle = models.CharField(max_length=256, db_index=True)
    district = models.CharField(max_length=256, db_index=True)
    ip = models.CharField(max_length=256, db_index=True)
    warehouse = models.CharField(max_length=256, db_index=True)
    existing = models.FloatField(null=True, blank=True)
    new = models.FloatField(null=True, blank=True)
    formulation = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Paed Patient Records"

    def __unicode__(self):
        return "%s %s" % (self.cycle, self.formulation)


class MultipleOrderFacility(models.Model):
    name = models.CharField(max_length=256, db_index=True)
    cycle = models.CharField(max_length=256, db_index=True)
    district = models.CharField(max_length=256, db_index=True)
    ip = models.CharField(max_length=256, db_index=True)
    warehouse = models.CharField(max_length=256, db_index=True)

    def __unicode__(self):
        return "%s %s" % (self.cycle, self.name)

    class Meta:
        verbose_name_plural = "Facilities with Multiple Orders"


class Dhis2StandardReport(models.Model):
    name = models.CharField(max_length=256, db_index=True, blank=False)
    report_id = models.CharField(max_length=256, db_index=True, blank=False)
    warehouse = models.CharField(choices=WAREHOUSES, max_length=50, blank=False)
    report_type = models.CharField(choices=REPORT_TYPES, max_length=50, blank=False)
    org_unit_id = models.CharField(max_length=20, db_index=True, blank=False)

    def __unicode__(self):
        return "%s" % self.name

    class Meta:
        verbose_name_plural = "DHIS2 Standard Reports"


class LocationToPartnerMapping(models.Model):
    mapping = PickledObjectField()

    def update(self, mapping):
        self.objects.all().delete()
        self.objects.create(mapping=mapping)

    @classmethod
    def get_mapping(cls):
        return FormattedKeyDict(cls.objects.first().mapping)


class FacilityTest(OrderedModel):
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    definition = TestDefinitionField()
    description = RichTextField()
    short_description = models.TextField()
    featured = models.BooleanField(default=False)
    slug = AutoSlugField(populate_from=["name".encode("utf-8")])

    class Meta(OrderedModel.Meta):
        verbose_name_plural = "Facility Tests"

    def __unicode__(self):
        return u"%s" % self.name

    def get_type(self):
        return maybe(json.loads(self.definition))["type"]["id"].or_else(None)


class TracingFormulations(models.Model):
    name = models.CharField(max_length=255)
    consumption_formulations = JSONField()
    patient_formulations = JSONField()
    slug = AutoSlugField(populate_from=["name".encode("utf-8")])

    def as_dict_obj(self):
        return {
            "name": self.name,
            "slug": self.slug,
            "patient_formulations": self.patient_formulations,
            "consumption_formulations": self.consumption_formulations,
        }

    class Meta:
        verbose_name_plural = "Tracing Formulations"

    def __unicode__(self):
        return u"%s" % (self.name)

    @staticmethod
    def get_abc_paed():
        return TracingFormulations.objects.get(slug="abc3tc-paed")

    @staticmethod
    def get_tdf_adult():
        return TracingFormulations.objects.get(slug="tdf3tcefv-adult")

    @staticmethod
    def get_efv_paed():
        return TracingFormulations.objects.get(slug="efv200-paed")
