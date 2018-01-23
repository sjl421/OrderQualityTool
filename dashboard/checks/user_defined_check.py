import importlib

from pydash import py_

from dashboard.checks.check import as_float_or_1, get_factored_values, as_values, available_comparisons
from dashboard.checks.check_preview import DBBasedCheckPreview
from dashboard.checks.entities import Definition
from dashboard.helpers import DEFAULT, NO, YES, N_A

CLASS_BASED = "ClassBased"


class UserDefinedFacilityCheck(DBBasedCheckPreview):

    def get_combinations(self):
        return [DEFAULT]

    def for_each_facility(self, facility_data, combination, other_facility_data=None):
        groups = []
        for group in self.definition.groups:
            values_for_group = self._group_values_from_location_data(group, facility_data, other_facility_data)
            groups.append(values_for_group)
        comparison_result, comparison_text = self.compare_results(groups)
        return comparison_result

    def _group_values_from_location_data(self, group, facility_data, other_facility_data):
        data_source = other_facility_data if group.cycle.id is "Previous" else facility_data
        records = group.model.get_records(data_source)

        if records:
            values = self.get_values_from_records(records, group)
            factored_values = get_factored_values(self.get_formulations(group), group.factors, values)
            return {
                "name": group.name,
                "aggregation": group.aggregation.name,
                "values": values,
                "headers": group.selected_fields,
                "has_factors": group.has_factors,
                "factored_values": factored_values,
                "result": self.aggregate_values(group, factored_values)
            }

    def get_values_from_records(self, records, group):
        formulations = [f.lower() for f in self.get_formulations(group)]
        return py_(records).reject(lambda x: x.formulation.lower() not in formulations).map(
            as_values(group.selected_fields)).value()


class UserDefinedFacilityTracedCheck(UserDefinedFacilityCheck):
    def get_combinations(self):
        return [tracer.get("name") for tracer in self.definition.groups[0].model.tracing_formulations]

    def get_formulations(self, group, sample_tracer=None):
        if sample_tracer and "name" in sample_tracer:
            return py_(group.model.tracing_formulations).filter(
                {"name": sample_tracer.get("name")}).first().value().get('formulations')
        return group.model.tracing_formulations[0].get('formulations')


class UserDefinedSingleGroupFacilityTracedCheck(UserDefinedFacilityCheck):

    def compare_results(self, groups):
        if self.definition.operator:
            comparison_class = available_comparisons.get(self.definition.operator.id)
            comparator = comparison_class()
            operator_constant = self.definition.operator_constant

            operator_constant = as_float_or_1(operator_constant)

            if comparator:
                group1_result = groups[0].get('result')
                group2_result = None
                comparison_result = comparator.compare(group1_result, group2_result, constant=operator_constant)
                result_text = comparator.text(group1_result, group2_result, operator_constant, comparison_result)
                result = YES if comparison_result else NO
                return result, result_text
        return N_A, None


testTypes = {
    "FacilityTwoGroups": UserDefinedFacilityCheck,
    "FacilityOneGroup": UserDefinedSingleGroupFacilityTracedCheck,
    "FacilityTwoGroupsAndTracingFormulation": UserDefinedFacilityTracedCheck,
}


def get_check_from_dict(data):
    definition = Definition.from_dict(data)
    return get_check(definition)


def get_check(definition):
    check_type = definition.type.get('id')
    full_class_name = definition.python_class
    if check_type == CLASS_BASED and full_class_name:
        return get_check_by_class(full_class_name)
    dynamic_check = testTypes.get(check_type)(definition)
    return dynamic_check


def get_check_by_class(full_class_name):
    module_name = ".".join(full_class_name.split(".")[:-1])
    class_name = full_class_name.split(".")[-1]
    selected_module = importlib.import_module(module_name)
    check_class = getattr(selected_module, class_name)
    return check_class()