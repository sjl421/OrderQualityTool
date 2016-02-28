from django.test import TestCase
from model_mommy import mommy

from dashboard.data.nn import NNRTICURRENTADULTSCheck
from dashboard.helpers import DEFAULT, DF1, NNRTI_CURRENT_ADULTS, DF2, FIELDS, RATIO, YES, FORMULATION, VALUE, COLUMN, ROWS, FINAL_SCORE, TOTAL
from dashboard.models import Score, Consumption
from dashboard.views.data_sources import NNRTIDataSource, HEADERS


class NNRTIDataSourceTestCaseForCurrentAdults(TestCase):
    test_name = NNRTI_CURRENT_ADULTS
    check_class = NNRTICURRENTADULTSCheck

    def test_correct_template_is_selected(self):
        data_source = NNRTIDataSource()
        self.assertEqual(data_source.get_template(""), "check/nnrti.html")

    def test_that_table_for_df1_has_proper_header(self):
        combination = DEFAULT
        score = Score.objects.create(name="F1", warehouse="W1", ip="I1", district="D1", REPORTING={DEFAULT: YES},
                                     WEB_BASED={DEFAULT: YES}, pass_count=2, fail_count=0)
        data_source = NNRTIDataSource()
        data = data_source.load(score, self.test_name, combination)
        self.assertEqual(data[DF1][HEADERS], ["ART", "eMTCT", TOTAL])
        self.assertEqual(data[DF1]["table_header"], "NNRTI")

    def test_that_table_for_df2_has_proper_header(self):
        combination = DEFAULT
        score = Score.objects.create(name="F1", warehouse="W1", ip="I1", district="D1", REPORTING={DEFAULT: YES},
                                     WEB_BASED={DEFAULT: YES}, pass_count=2, fail_count=0)
        data_source = NNRTIDataSource()
        data = data_source.load(score, self.test_name, combination)
        self.assertEqual(data[DF2][HEADERS], ["ART", "eMTCT", TOTAL])
        self.assertEqual(data[DF2]["table_header"], "NNRTI/PI")

    def test_that_table_for_df1_has_2_rows(self):
        formulations = self.check_class.combinations[0][DF1]
        fields = self.check_class.combinations[0][FIELDS]
        cycle = "Jan - Feb 2014"
        facility_name = "F1"
        warehouse_name = "W1"
        ip_name = "I1"
        district_name = "D1"
        for formulation in formulations:
            data = {FORMULATION: formulation}
            for field in fields:
                data[field] = 20
            mommy.make(Consumption, name=facility_name, warehouse=warehouse_name, ip=ip_name, district=district_name, cycle=cycle, **data)
        combination = DEFAULT
        score = Score.objects.create(name=facility_name, warehouse=warehouse_name, ip=ip_name, district=district_name, REPORTING={DEFAULT: YES},
                                     WEB_BASED={DEFAULT: YES}, pass_count=2, fail_count=0, cycle=cycle)
        data_source = NNRTIDataSource()
        data = data_source.load(score, self.test_name, combination)
        self.assertEqual(len(data[DF1][ROWS]), 3)
        self.assertEqual(data[DF1][ROWS][1][COLUMN], "Tenofovir/Lamivudine (TDF/3TC) 300mg/300mg [Pack 30]")
        self.assertEqual(data[DF1][ROWS][0][TOTAL], 40)

    def test_that_each_df1_shows_ratios(self):
        formulations = self.check_class.combinations[0][DF1]
        fields = self.check_class.combinations[0][FIELDS]
        cycle = "Jan - Feb 2014"
        facility_name = "F1"
        warehouse_name = "W1"
        ip_name = "I1"
        district_name = "D1"
        for formulation in formulations:
            data = {FORMULATION: formulation}
            for field in fields:
                data[field] = 20
            mommy.make(Consumption, name=facility_name, warehouse=warehouse_name, ip=ip_name, district=district_name, cycle=cycle, **data)
        combination = DEFAULT
        score = Score.objects.create(name=facility_name, warehouse=warehouse_name, ip=ip_name, district=district_name, REPORTING={DEFAULT: YES},
                                     WEB_BASED={DEFAULT: YES}, pass_count=2, fail_count=0, cycle=cycle)
        data_source = NNRTIDataSource()
        data = data_source.load(score, self.test_name, combination)
        ratios_key = DF1 + "_ratios"
        self.assertEqual(len(data[ratios_key][ROWS]), 3)
        self.assertEqual(data[ratios_key][ROWS][0][VALUE], 2.0)
        self.assertEqual(data[ratios_key][ROWS][0][COLUMN], "Zidovudine/Lamivudine (AZT/3TC) 300mg/150mg [Pack 60]")
        self.assertEqual(data[ratios_key][ROWS][1][VALUE], 2.0)
        self.assertEqual(data[ratios_key][ROWS][1][COLUMN], "Tenofovir/Lamivudine (TDF/3TC) 300mg/300mg [Pack 30]")
        self.assertEqual(data[ratios_key][ROWS][2][VALUE], 2.0)
        self.assertEqual(data[ratios_key][ROWS][2][COLUMN], "Abacavir/Lamivudine (ABC/3TC) 600mg/300mg [Pack 30]")

    def test_that_each_df1_shows_calculated_tables(self):
        formulations = self.check_class.combinations[0][DF1]
        fields = self.check_class.combinations[0][FIELDS]
        cycle = "Jan - Feb 2014"
        facility_name = "F1"
        warehouse_name = "W1"
        ip_name = "I1"
        district_name = "D1"
        for formulation in formulations:
            data = {FORMULATION: formulation}
            for field in fields:
                data[field] = 20
            mommy.make(Consumption, name=facility_name, warehouse=warehouse_name, ip=ip_name, district=district_name, cycle=cycle, **data)
        combination = DEFAULT
        score = Score.objects.create(name=facility_name, warehouse=warehouse_name, ip=ip_name, district=district_name, REPORTING={DEFAULT: YES},
                                     WEB_BASED={DEFAULT: YES}, pass_count=2, fail_count=0, cycle=cycle)
        data_source = NNRTIDataSource()
        data = data_source.load(score, self.test_name, combination)
        ratios_key = "%s_calculated" % DF1
        self.assertEqual(len(data[ratios_key][ROWS]), 5)
        self.assertEqual(data[ratios_key][ROWS][0][COLUMN], "NNRTI")
        self.assertEqual(data[ratios_key][ROWS][1][VALUE], 20.0)
        self.assertEqual(data[ratios_key][ROWS][1][COLUMN], "Zidovudine/Lamivudine (AZT/3TC) 300mg/150mg [Pack 60]")
        self.assertEqual(data[ratios_key][ROWS][2][VALUE], 20.0)
        self.assertEqual(data[ratios_key][ROWS][2][COLUMN], "Tenofovir/Lamivudine (TDF/3TC) 300mg/300mg [Pack 30]")
        self.assertEqual(data[ratios_key][ROWS][3][VALUE], 20.0)
        self.assertEqual(data[ratios_key][ROWS][3][COLUMN], "Abacavir/Lamivudine (ABC/3TC) 600mg/300mg [Pack 30]")
        self.assertEqual(data[ratios_key][ROWS][4][VALUE], 60.0)
        self.assertEqual(data[ratios_key][ROWS][4][COLUMN], TOTAL)
        self.assertEqual(data[ratios_key][ROWS][4]["isHeader"], True)

    def test_that_table_for_df2_has_2_rows(self):
        formulations = self.check_class.combinations[0][DF2]
        fields = self.check_class.combinations[0][FIELDS]
        cycle = "Jan - Feb 2014"
        facility_name = "F1"
        warehouse_name = "W1"
        ip_name = "I1"
        district_name = "D1"
        for formulation in formulations:
            data = {FORMULATION: formulation}
            for field in fields:
                data[field] = 20
            mommy.make(Consumption, name=facility_name, warehouse=warehouse_name, ip=ip_name, district=district_name, cycle=cycle, **data)
        combination = DEFAULT
        score = Score.objects.create(name=facility_name, warehouse=warehouse_name, ip=ip_name, district=district_name, REPORTING={DEFAULT: YES},
                                     WEB_BASED={DEFAULT: YES}, pass_count=2, fail_count=0, cycle=cycle)
        data_source = NNRTIDataSource()
        data = data_source.load(score, self.test_name, combination)
        self.assertEqual(len(data[DF2][ROWS]), 4)
        self.assertEqual(data[DF2][ROWS][1][COLUMN], "Nevirapine (NVP) 200mg [Pack 60]")
        self.assertEqual(data[DF2][ROWS][0][TOTAL], 40)

    def test_that_each_df2_shows_ratios(self):
        formulations = self.check_class.combinations[0][DF2]
        fields = self.check_class.combinations[0][FIELDS]
        cycle = "Jan - Feb 2014"
        facility_name = "F1"
        warehouse_name = "W1"
        ip_name = "I1"
        district_name = "D1"
        for formulation in formulations:
            data = {FORMULATION: formulation}
            for field in fields:
                data[field] = 20
            mommy.make(Consumption, name=facility_name, warehouse=warehouse_name, ip=ip_name, district=district_name, cycle=cycle, **data)
        combination = DEFAULT
        score = Score.objects.create(name=facility_name, warehouse=warehouse_name, ip=ip_name, district=district_name, REPORTING={DEFAULT: YES},
                                     WEB_BASED={DEFAULT: YES}, pass_count=2, fail_count=0, cycle=cycle)
        data_source = NNRTIDataSource()
        data = data_source.load(score, self.test_name, combination)
        ratios_key = DF2 + "_ratios"
        self.assertEqual(len(data[ratios_key][ROWS]), 4)
        self.assertEqual(data[ratios_key][ROWS][0][VALUE], 2.0)
        self.assertEqual(data[ratios_key][ROWS][0][COLUMN], "Efavirenz (EFV) 600mg [Pack 30]")
        self.assertEqual(data[ratios_key][ROWS][1][VALUE], 2.0)
        self.assertEqual(data[ratios_key][ROWS][1][COLUMN], "Nevirapine (NVP) 200mg [Pack 60]")
        self.assertEqual(data[ratios_key][ROWS][2][VALUE], 2.0)
        self.assertEqual(data[ratios_key][ROWS][2][COLUMN], "Atazanavir/Ritonavir (ATV/r) 300mg/100mg [Pack 30]")
        self.assertEqual(data[ratios_key][ROWS][3][VALUE], 2.0)
        self.assertEqual(data[ratios_key][ROWS][3][COLUMN], "Lopinavir/Ritonavir (LPV/r) 200mg/50mg [Pack 120]")

    def test_that_each_df2_shows_calculated_tables(self):
        formulations = self.check_class.combinations[0][DF2]
        fields = self.check_class.combinations[0][FIELDS]
        cycle = "Jan - Feb 2014"
        facility_name = "F1"
        warehouse_name = "W1"
        ip_name = "I1"
        district_name = "D1"
        for formulation in formulations:
            data = {FORMULATION: formulation}
            for field in fields:
                data[field] = 20
            mommy.make(Consumption, name=facility_name, warehouse=warehouse_name, ip=ip_name, district=district_name, cycle=cycle, **data)
        combination = DEFAULT
        score = Score.objects.create(name=facility_name, warehouse=warehouse_name, ip=ip_name, district=district_name, REPORTING={DEFAULT: YES},
                                     WEB_BASED={DEFAULT: YES}, pass_count=2, fail_count=0, cycle=cycle)
        data_source = NNRTIDataSource()
        data = data_source.load(score, self.test_name, combination)
        ratios_key = "%s_calculated" % DF2
        self.assertEqual(len(data[ratios_key][ROWS]), 6)
        self.assertEqual(data[ratios_key][ROWS][0][COLUMN], "NNRTI/PI")
        self.assertEqual(data[ratios_key][ROWS][1][VALUE], 20.0)
        self.assertEqual(data[ratios_key][ROWS][1][COLUMN], "Efavirenz (EFV) 600mg [Pack 30]")
        self.assertEqual(data[ratios_key][ROWS][2][VALUE], 20.0)
        self.assertEqual(data[ratios_key][ROWS][2][COLUMN], "Nevirapine (NVP) 200mg [Pack 60]")
        self.assertEqual(data[ratios_key][ROWS][3][VALUE], 20.0)
        self.assertEqual(data[ratios_key][ROWS][3][COLUMN], "Atazanavir/Ritonavir (ATV/r) 300mg/100mg [Pack 30]")
        self.assertEqual(data[ratios_key][ROWS][4][VALUE], 20.0)
        self.assertEqual(data[ratios_key][ROWS][4][COLUMN], "Lopinavir/Ritonavir (LPV/r) 200mg/50mg [Pack 120]")
        self.assertEqual(data[ratios_key][ROWS][5][VALUE], 80.0)
        self.assertEqual(data[ratios_key][ROWS][5][COLUMN], TOTAL)

    def test_calculates_nnrti_count(self):

        fields = self.check_class.combinations[0][FIELDS]
        cycle = "Jan - Feb 2014"
        facility_name = "F1"
        warehouse_name = "W1"
        ip_name = "I1"
        district_name = "D1"
        for part in [DF1, DF2]:
            formulations = self.check_class.combinations[0][part]
            for formulation in formulations:
                data = {FORMULATION: formulation}
                for field in fields:
                    data[field] = 20
                mommy.make(Consumption, name=facility_name, warehouse=warehouse_name, ip=ip_name, district=district_name, cycle=cycle, **data)
        combination = DEFAULT
        score = Score.objects.create(name=facility_name, warehouse=warehouse_name, ip=ip_name, district=district_name, REPORTING={DEFAULT: YES},
                                     WEB_BASED={DEFAULT: YES}, pass_count=2, fail_count=0, cycle=cycle)
        data_source = NNRTIDataSource()
        data = data_source.load(score, self.test_name, combination)
        self.assertEqual(data["%s_COUNT" % DF1], 60.0)
        self.assertEqual(data["%s_COUNT" % DF2], 80.0)
        self.assertEqual(data[FINAL_SCORE], 25.0)