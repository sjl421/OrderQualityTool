import os
from collections import defaultdict

from django.test import TestCase

from dashboard.data.adherence import GuidelineAdherenceCheckAdult1L, calculate_score
from dashboard.data.blanks import BlanksQualityCheck, IsReportingCheck, MultipleCheck, WebBasedCheck
from dashboard.data.consumption_patients import ConsumptionAndPatientsQualityCheck
from dashboard.data.cycles import DIFFERENTORDERSOVERTIMECheck
from dashboard.data.free_form_report import FreeFormReport
from dashboard.data.negatives import NegativeNumbersQualityCheck
from dashboard.data.utils import clean_name, get_patient_total, get_consumption_totals, \
    values_for_records
from dashboard.helpers import *


class FakeReport():
    pass


class Cell():
    def __init__(self, value):
        self.value = value


class DataTestCase(TestCase):
    def test_clean_name(self):
        row = [Cell("Byakabanda HC III_Rakai"), Cell(""), Cell(""), Cell(""), Cell(""), Cell("Rakai ")]
        assert clean_name(row) == "Byakabanda HC III"

    def test_consumption_records(self):
        report = FakeReport()
        report.cs = {"PLACE1": [{FORMULATION: "A", "openingBalance": 3},
                                {FORMULATION: "B", "openingBalance": 3},
                                {FORMULATION: "A", "openingBalance": 12}]}
        check = ConsumptionAndPatientsQualityCheck(report)
        records = check.get_consumption_records("PLACE1", "A")
        assert records == [{FORMULATION: "A", "openingBalance": 3}, {FORMULATION: "A", "openingBalance": 12}]

    def test_patient_records(self):
        report = FakeReport()
        report.cycle = "Jul - Aug 2015"
        report.pds = {"PLACE1": [{FORMULATION: "A1", NEW: 3},
                                 {FORMULATION: "B", NEW: 3},
                                 {FORMULATION: "A2", NEW: 12}]}
        check = ConsumptionAndPatientsQualityCheck(report)
        records = check.get_patient_records("PLACE1", "A", False)
        assert records == [{FORMULATION: "A1", NEW: 3}, {FORMULATION: "A2", NEW: 12}]

    def test_adult_records(self):
        report = FakeReport()
        report.cycle = "Jul - Aug 2015"
        report.ads = {"PLACE1": [{FORMULATION: "A", NEW: 3},
                                 {FORMULATION: "B", NEW: 3},
                                 {FORMULATION: "A", NEW: 12}]}
        check = ConsumptionAndPatientsQualityCheck(report)
        records = check.get_patient_records("PLACE1", "A", True)
        assert records == [{FORMULATION: "A", NEW: 3}, {FORMULATION: "A", NEW: 12}]

    def test_patient_totals(self):
        assert get_patient_total([{NEW: 10, EXISTING: 12}, {NEW: None, EXISTING: 12}]) == 34

    def test_consumption_totals(self):
        assert get_consumption_totals([NEW], [{NEW: 10, EXISTING: 12}, {NEW: None, EXISTING: 12}]) == 10
        assert get_consumption_totals([NEW], [{NEW: None, EXISTING: 12}, {NEW: 10, EXISTING: 12}]) == 10
        assert get_consumption_totals([EXISTING], [{NEW: 10, EXISTING: 12}, {NEW: None, EXISTING: 12}]) == 24
        assert get_consumption_totals([EXISTING, NEW],
                                      [{NEW: 10, EXISTING: 12}, {NEW: None, EXISTING: 12}]) == 34

    def test_values_for_records(self):
        assert values_for_records([NEW], [{NEW: 10, EXISTING: 12}, {NEW: None, EXISTING: 12}]) == [10, None]

    def test_blanks(self):
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tests', 'fixtures',
                                 "new_format.xlsx")
        report = FreeFormReport(file_path, "May Jun").load()
        report.cycle = "Jul - Aug 2015"
        cases = [{'test': BlanksQualityCheck, 'expected': 8.0},
                 {'test': MultipleCheck, 'expected': 20.0},
                 {'test': IsReportingCheck, 'expected': 96.0},
                 {'test': WebBasedCheck, 'expected': 96.0}
                 ]
        for case in cases:
            result = case['test'](report).run()['DEFAULT']
            self.assertEquals(result[YES], case['expected'])

    def test_publishing_scores(self):
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tests', 'fixtures',
                                 "new_format.xlsx")
        report = FreeFormReport(file_path, "May Jun").load()
        cases = [{'test': BlanksQualityCheck, 'expected': 8.0},
                 {'test': MultipleCheck, 'expected': 20.0},
                 {'test': IsReportingCheck, 'expected': 96.0},
                 {'test': WebBasedCheck, 'expected': 96.0}
                 ]
        for case in cases:
            result = case['test'](report).run()['DEFAULT']
            self.assertEquals(result[YES], case['expected'])

    def xtest_calculate_score(self):
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tests', 'fixtures',
                                 "new_format.xlsx")
        report = FreeFormReport(file_path, "May Jun").load()
        no, not_reporting, yes = NegativeNumbersQualityCheck(report).run()['DEFAULT']
        assert yes == 57.3


class GuidelineAdherenceAdult1LTestCase(TestCase):
    def test_score_is_yes_if_sum_of_new_hiv_positive_women_and_new_art_for_tdf_is_80_percent_that_for_AZT(self):
        df1_count = df2_count = 1
        sum_df1 = 9
        sum_df2 = 2
        ratio = 0.8
        result, no, not_reporting, yes = calculate_score(df1_count, df2_count, sum_df1, sum_df2, ratio, 0, 0, 0)
        self.assertEqual(result, YES)
        self.assertEqual(yes, 1)
        self.assertEqual(no, 0)
        self.assertEqual(not_reporting, 0)

    def test_score_is_yes_if_sum_of_new_hiv_positive_women_and_new_art_for_tdf_is_zero_and_that_for_AZT_is_also_zero(
            self):
        df1_count = df2_count = 1
        sum_df1 = 0
        sum_df2 = 0
        ratio = 0.8
        result, no, not_reporting, yes = calculate_score(df1_count, df2_count, sum_df1, sum_df2, ratio, 0, 0, 0)
        self.assertEqual(result, YES)
        self.assertEqual(yes, 1)
        self.assertEqual(no, 0)
        self.assertEqual(not_reporting, 0)

    def test_score_is_no_if_tdf_cells_are_blank(self):
        df1_count = df2_count = 1
        sum_df1 = 0
        sum_df2 = 12
        ratio = 0.8
        result, no, not_reporting, yes = calculate_score(df1_count, df2_count, sum_df1, sum_df2, ratio, 0, 0, 0, True,
                                                         False)
        self.assertEqual(result, NO)
        self.assertEqual(yes, 0)
        self.assertEqual(no, 1)
        self.assertEqual(not_reporting, 0)

    def test_score_is_no_if_azt_cells_are_blank(self):
        df1_count = df2_count = 1
        sum_df1 = 0
        sum_df2 = 0
        ratio = 0.8
        result, no, not_reporting, yes = calculate_score(df1_count, df2_count, sum_df1, sum_df2, ratio, 0, 0, 0, False,
                                                         True)
        self.assertEqual(result, NO)
        self.assertEqual(yes, 0)
        self.assertEqual(no, 1)
        self.assertEqual(not_reporting, 0)

    def test_score_is_not_reporting_if_azt_or_tdf_cells_are_not_found(self):
        df1_count = df2_count = 0
        sum_df1 = 0
        sum_df2 = 0
        ratio = 0.8
        result, no, not_reporting, yes = calculate_score(df1_count, df2_count, sum_df1, sum_df2, ratio, 0, 0, 0, False,
                                                         True)
        self.assertEqual(result, NOT_REPORTING)
        self.assertEqual(yes, 0)
        self.assertEqual(no, 0)
        self.assertEqual(not_reporting, 1)

    def test_run(self):
        report = FakeReport()
        report.cs = {"PLACE1": [{FORMULATION: "A", "openingBalance": 1},
                                {FORMULATION: "B", "openingBalance": 2},
                                {FORMULATION: "C", "openingBalance": 3},
                                {FORMULATION: "E", "openingBalance": 4},
                                {FORMULATION: "A", "openingBalance": 12}]}
        check = GuidelineAdherenceCheckAdult1L(report)

    def test_adherence_filter(self):
        report = FakeReport()
        report.locs = [{"name": "PLACE1", "scores": defaultdict(dict)}]
        report.cs = {"PLACE1": [
            {
                FORMULATION: "Tenofovir/Lamivudine (TDF/3TC) 300mg/300mg [Pack 30]",
                "estimated_number_of_new_pregnant_women": 4,
                "estimated_number_of_new_patients": 4
            },
            {
                FORMULATION: "Tenofovir/Lamivudine/Efavirenz (TDF/3TC/EFV) 300mg/300mg/600mg[Pack 30]",
                "estimated_number_of_new_pregnant_women": 4,
                "estimated_number_of_new_patients": 4},
            {
                FORMULATION: "Zidovudine/Lamivudine (AZT/3TC) 300mg/150mg [Pack 60]",
                "estimated_number_of_new_pregnant_women": 1,
                "estimated_number_of_new_patients": 1},
            {
                FORMULATION: "Zidovudine/Lamivudine/Nevirapine (AZT/3TC/NVP) 300mg/150mg/200mg [Pack 60]",
                "estimated_number_of_new_pregnant_women": 1,
                "estimated_number_of_new_patients": 1},
            {FORMULATION: "A", "openingBalance": 12}]}
        check = GuidelineAdherenceCheckAdult1L(report)
        assert check.run()['DEFAULT']['YES'] == 100


class TestDIFFERENTORDERSOVERTIMECheck(TestCase):
    def test_same_values_scores_no(self):
        report = FakeReport()
        report.cycle = 'Jul - Aug 2015'
        report.locs = [{"name": "PLACE1", "scores": defaultdict(dict)}]
        report.cs = {
            'PLACE1': [
                {
                    FORMULATION: F1_QUERY,
                    OPENING_BALANCE: 12,
                    ESTIMATED_NUMBER_OF_NEW_PATIENTS: 3,
                    ART_CONSUMPTION: 4
                }
            ]
        }

        other_report = FakeReport()
        other_report.cycle = 'May - Jun 2015'
        other_report.locs = [{"name": "PLACE1", "scores": defaultdict(dict)}]
        other_report.cs = {
            'PLACE1': [
                {
                    FORMULATION: F1_QUERY,
                    OPENING_BALANCE: 12,
                    ESTIMATED_NUMBER_OF_NEW_PATIENTS: 3,
                    ART_CONSUMPTION: 4
                }
            ]
        }
        scores = DIFFERENTORDERSOVERTIMECheck(report, other_report).run()
        self.assertTrue(F1 in scores)
        self.assertEqual(scores[F1], {NO: 100.0, YES: 0, NOT_REPORTING: 0})

    def test_all_zeros_scores_yes(self):
        report = FakeReport()
        report.cycle = 'Jul - Aug 2015'
        report.locs = [{"name": "PLACE1", "scores": defaultdict(dict)}]
        report.cs = {
            'PLACE1': [
                {
                    FORMULATION: F1_QUERY,
                    OPENING_BALANCE: 0,
                    ESTIMATED_NUMBER_OF_NEW_PATIENTS: 0,
                    ART_CONSUMPTION: 0
                }
            ]
        }

        other_report = FakeReport()
        other_report.cycle = 'May - Jun 2015'
        other_report.locs = [{"name": "PLACE1", "scores": defaultdict(dict)}]
        other_report.cs = {
            'PLACE1': [
                {
                    FORMULATION: F1_QUERY,
                    OPENING_BALANCE: 0,
                    ESTIMATED_NUMBER_OF_NEW_PATIENTS: 0,
                    ART_CONSUMPTION: 0
                }
            ]
        }
        scores = DIFFERENTORDERSOVERTIMECheck(report, other_report).run()
        self.assertTrue(F1 in scores)
        self.assertEqual(scores[F1], {NO: 0.0, YES: 100.0, NOT_REPORTING: 0})

    def test_diff_scores_yes(self):
        report = FakeReport()
        report.cycle = 'Jul - Aug 2015'
        report.locs = [{"name": "PLACE1", "scores": defaultdict(dict)}]
        report.cs = {
            'PLACE1': [
                {
                    FORMULATION: F1_QUERY,
                    OPENING_BALANCE: 12,
                    ESTIMATED_NUMBER_OF_NEW_PATIENTS: 2,
                    ART_CONSUMPTION: 4
                }
            ]
        }

        other_report = FakeReport()
        other_report.cycle = 'May - Jun 2015'
        other_report.locs = [{"name": "PLACE1", "scores": defaultdict(dict)}]
        other_report.cs = {
            'PLACE1': [
                {
                    FORMULATION: F1_QUERY,
                    OPENING_BALANCE: 12,
                    ESTIMATED_NUMBER_OF_NEW_PATIENTS: 0,
                    ART_CONSUMPTION: 4
                }
            ]
        }
        scores = DIFFERENTORDERSOVERTIMECheck(report, other_report).run()
        self.assertTrue(F1 in scores)
        self.assertEqual(scores[F1], {NO: 0.0, YES: 100.0, NOT_REPORTING: 0})

    def test_missing_scores_na(self):
        report = FakeReport()
        report.cycle = 'Jul - Aug 2015'
        report.locs = [{"name": "PLACE1", "scores": defaultdict(dict)}]
        report.cs = {
            'PLACE1': [
                {
                    FORMULATION: "the",
                    OPENING_BALANCE: 12,
                    ESTIMATED_NUMBER_OF_NEW_PATIENTS: 3,
                    ART_CONSUMPTION: 4
                }
            ]
        }

        other_report = FakeReport()
        other_report.cycle = 'May - Jun 2015'
        other_report.locs = [{"name": "PLACE1", "scores": defaultdict(dict)}]
        other_report.cs = {
            'PLACE1': [
                {
                    FORMULATION: F1_QUERY,
                    OPENING_BALANCE: 12,
                    ESTIMATED_NUMBER_OF_NEW_PATIENTS: 3,
                    ART_CONSUMPTION: 4
                }
            ]
        }
        scores = DIFFERENTORDERSOVERTIMECheck(report, other_report).run()
        self.assertTrue(F1 in scores)
        self.assertEqual(scores[F1], {NO: 0.0, YES: 0, NOT_REPORTING: 100.0})