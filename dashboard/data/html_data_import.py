import pydash
from bs4 import BeautifulSoup

from dashboard.data.data_import import DataImport
from dashboard.data.entities import DataImportRecord
from dashboard.data.utils import timeit
from dashboard.helpers import PAED_PATIENT_REPORT, ADULT_PATIENT_REPORT, CONSUMPTION_REPORT, HTML_PARSER

TR = "tr"
TD = "td"
TR_ROTATED = "tr_rotated"


@timeit
def extract_locations_and_import_records(report_outputs, partner_mapping):
    records = get_all_records(report_outputs, partner_mapping)
    locations = get_locations(records)
    return locations, records


def get_locations(records):
    unique_records_by_location = pydash.uniq(records, lambda item: item.location)
    locations = pydash.map_(unique_records_by_location, lambda item: item.location)
    return locations


@timeit
def get_all_records(report_outputs, partner_mapping):
    import_records = []
    for report_output in report_outputs:
        html_table_element = BeautifulSoup(report_output.output, HTML_PARSER)
        records_for_output = parse_records_from_html(html_table_element, report_output.report, partner_mapping)
        import_records.extend(records_for_output)
    return import_records


def by_type(report_type):
    def check_item(item):
        return item.report_type == report_type

    return check_item


def parse_pead_records(data_import_records):
    return pydash.chain(data_import_records).filter(by_type(PAED_PATIENT_REPORT)).map(
        lambda item: item.build_patient_record()).group_by(lambda item: item.location).value()


def parse_adult_records(data_import_records):
    return pydash.chain(data_import_records).filter(by_type(ADULT_PATIENT_REPORT)).map(
        lambda item: item.build_patient_record()).group_by(lambda item: item.location).value()


def parse_consumption_records(data_import_records):
    return pydash.chain(data_import_records).filter(by_type(CONSUMPTION_REPORT)).map(
        lambda item: item.build_consumption_record()).group_by(lambda item: item.location).value()


class HtmlDataImport(DataImport):
    def load(self, partner_mapping):
        locations, all_records = extract_locations_and_import_records(self.raw_data, partner_mapping)
        self.locs = locations
        self.pds = parse_pead_records(all_records)
        self.ads = parse_adult_records(all_records)
        self.cs = parse_consumption_records(all_records)
        return self


@timeit
def parse_records_from_html(html_table_element, report, partner_mapping):
    data_import_records = []
    table_column_names = []
    row_with_column_names = html_table_element.find(id=TR_ROTATED)
    for item in row_with_column_names:
        if item and item.text:
            table_column_names.append(item.text)

    for table_row_element in html_table_element.find_all(TR):
        if len(table_row_element) == len(row_with_column_names):
            items_in_row = table_row_element.find_all(TD)
            if len(items_in_row) > 0:
                data_import_record = DataImportRecord(warehouse=report.warehouse, report_type=report.report_type,
                                                      data=dict())
                for item_index, item in enumerate(items_in_row):
                    column_name = table_column_names[item_index]
                    data_import_record.data[column_name] = try_to_get_int(item)
                data_import_record.location = data_import_record.build_location(partner_mapping)
                data_import_records.append(data_import_record)

    return data_import_records


def try_to_get_int(item):
    try:
        return int(item.get_text())
    except ValueError as e:
        return item.get_text()
