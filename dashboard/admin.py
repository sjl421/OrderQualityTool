from admirarchy.utils import HierarchicalModelAdmin
from custom_user.forms import EmailUserChangeForm, EmailUserCreationForm
from django.contrib.admin import AdminSite, ModelAdmin
from django.contrib.admin.models import LogEntry
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy
from django.utils.translation import ugettext_lazy as _
from dynamic_preferences.admin import GlobalPreferenceAdmin
from dynamic_preferences.models import GlobalPreferenceModel
from logentry_admin.admin import LogEntryAdmin
from ordered_model.admin import OrderedModelAdmin

from dashboard.forms import TestDefinitionForm
from dashboard.models import (
    DashboardUser,
    Consumption,
    Cycle,
    AdultPatientsRecord,
    PAEDPatientsRecord,
    Score,
    MultipleOrderFacility,
    Dhis2StandardReport,
    FacilityTest,
    TracingFormulations,
)
from dashboard.tasks import update_checks


class EmailUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
    )

    form = EmailUserChangeForm
    add_form = EmailUserCreationForm

    list_display = ("email", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = ("groups", "user_permissions")


class QdbSite(AdminSite):
    site_title = ugettext_lazy("Order Quality admin")

    site_header = ugettext_lazy("Order Quality administration")

    index_title = ugettext_lazy("Order Quality administration")


class MyModelAdmin(HierarchicalModelAdmin):
    hierarchy = True


class ConsumptionAdmin(ModelAdmin):
    list_display = (
        "name",
        "cycle",
        "district",
        "ip",
        "warehouse",
        "formulation",
        "opening_balance",
        "quantity_received",
        "consumption",
        "loses_adjustments",
        "closing_balance",
        "months_of_stock_on_hand",
        "quantity_required_for_current_patients",
        "estimated_number_of_new_patients",
        "estimated_number_of_new_pregnant_women",
    )
    search_fields = ("name", "cycle", "district", "ip")
    list_filter = ("cycle", "formulation")


class PatientAdmin(ModelAdmin):
    search_fields = ("name", "district")
    list_filter = ("cycle", "formulation", "ip", "warehouse")
    list_display = (
        "name", "cycle", "district", "ip", "warehouse", "formulation", "existing", "new"
    )


def run_tests(model_admin, request, queryset):
    update_checks.apply_async(args=[[c.id for c in queryset.all()]], priority=1)


run_tests.short_description = "Run quality tests for these cycles"


class ScoreAdmin(ModelAdmin):
    search_fields = ("name", "district")
    list_display = (
        "name",
        "cycle",
        "district",
        "ip",
        "warehouse",
        "default_pass_count",
        "default_fail_count",
        "f1_pass_count",
        "f1_fail_count",
    )
    list_filter = ("cycle",)

    def cycle(self, obj):
        return obj.facility_cycle.cycle

    def facility(self, obj):
        return obj.facility_cycle.facility


class CycleAdmin(ModelAdmin):
    actions = [run_tests]

    def get_queryset(self, request):
        return super(CycleAdmin, self).get_queryset(request).defer("state")


class FacilityTestAdmin(OrderedModelAdmin):
    list_display = ("name", "move_up_down_links", "order")


class TracingFormulationAdmin(ModelAdmin):
    search_fields = ("name", "model")
    list_display = ("name", "slug")


admin_site = QdbSite()
admin_site.register(Group, GroupAdmin)
admin_site.register(DashboardUser, EmailUserAdmin)
admin_site.register(Score, ScoreAdmin)
admin_site.register(AdultPatientsRecord, PatientAdmin)
admin_site.register(PAEDPatientsRecord, PatientAdmin)
admin_site.register(Consumption, ConsumptionAdmin)
admin_site.register(Cycle, CycleAdmin)
admin_site.register(MultipleOrderFacility)
admin_site.register(GlobalPreferenceModel, GlobalPreferenceAdmin)
admin_site.register(Dhis2StandardReport)
admin_site.register(FacilityTest, FacilityTestAdmin)
admin_site.register(TracingFormulations, TracingFormulationAdmin)
admin_site.register(LogEntry, LogEntryAdmin)
