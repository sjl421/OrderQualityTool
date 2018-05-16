# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-11-27 00:07
from __future__ import unicode_literals

from django.db import migrations

default_tests = [
    {
        "name": "Facility Reporting",
        "short_description": "Did the facility submit an order?",
        "description": "Reports if the facility has submitted an order or not during a given cycle",
        "test_type": "FACILITY_ONLY",
    },
    {
        "short_description": "GUIDELINE ADHERENCE (Adult 1L): Estimated new patients on TDF-based formulations are 80%+ of total?",
        "name": "GUIDELINE ADHERENCE (Adult 1L)",
        "description": """Tests is the facility is adhering to national guidelines for Adult 1st Line therapy.

This is done by testing if the volume of estimated new ART patients on Adult TDF-based formulations (i.e. TDF/3TC/EFV 300/300/600mg and TDF/3TC 300/300mg) represent at least 80% of the total of those on TDF-based and AZT-based formulations (Adult AZT-based formulations are AZT/3TC/NVP 300/150/200mg and AZT/3TC 300/150mg)""",
        "test_type": "FACILITY_ONLY",
    },
    {
        "name": "GUIDELINE ADHERENCE (Adult 2L)",
        "short_description": "GUIDELINE ADHERENCE (Adult 2L): Estimated new patients on ATV/r-based formulations are 73%+ of total?",
        "description": """Tests is the facility is adhering to national guidelines for Adult 2nd Line therapy

This is done by testing if the volume of estimated new ART patients on Adult ATV/r-based formulations (i.e. ATV/r 300/100mg) represent at least 73% of the total of those on ATV/r-based and LPV/r-based formulations (Adult LPV/r-based formulations are LPV/r 200/50mg)""",
        "test_type": "FACILITY_ONLY",
    },
    {
        "name": "GUIDELINE ADHERENCE (Paediatric 1L)",
        "short_description": "GUIDELINE ADHERENCE (Paediatric 1L): Estimated new patients on ABC-based formulations are 80%+ of total?",
        "description": """Tests is the facility is adhering to national guidelines for Paediatric 1st Line therapy

This is done by testing if the volume of estimated new ART patients on Paediatric ABC-based formulations (i.e. ABC/3TC 60/30mg) represent at least 80% of the total of those on ABC-based and AZT-based formulations (Paediatric AZT-based formulations are AZT/3TC/NVP 60/30/50mg and AZT/3TC 60/30mg)""",
        "test_type": "FACILITY_ONLY",
    },
    {
        "name": "MULTIPLE ORDERS",
        "short_description": "MULTIPLE ORDERS: Submitted more than one order?",
        "description": """Reports facilities that have submitted more than one order during a given cycle""",
        "test_type": "FACILITY_ONLY",
    },
    {
        "name": "NO BLANKS",
        "short_description": "NO BLANKS: Order form free of blanks?",
        "description": """Tests if the facility has submitted a complete order form or has left blanks in any data fields where a number (either zero or otherwise) should have been input""",
        "test_type": "FACILITY_ONLY",
    },
    {
        "name": "NO NEGATIVES",
        "short_description": "NO NEGATIVES: Order free of negative inputs?",
        "description": """This test is carried out for the system's three Sample Formulations: 1) Adult TDF/3TC/EFV (300/300/600mg), 2) Paediatric ABC/3TC (60/30mg), and 3) Paediatric EFV(200mg)

Tests if the facility has input a negative number into any of four key data fields (Opening Balance, ART Consumption, Closing Balance and Estimated New ART Patients) where a positive number or zero should be""",
        "test_type": "FACILITY_AND_SAMPLE_FORMULATION",
    },
    {
        "name": "VOLUME TALLY",
        "short_description": "VOLUME TALLY: Consumption and patient volumes within 30%?",
        "description": """This test is carried out for the system's three Sample Formulations: 1) Adult TDF/3TC/EFV (300/300/600mg), 2) Paediatric ABC/3TC (60/30mg), and 3) Paediatric EFV(200mg)

Tests if the facility has reported corresponding Consumption volumes and Patient numbers that "make sense", i.e. are within 30% of each other. The specific datapoints compared are:

1) For Sample Formulation 1, Adult TDF/3TC/EFV: Compares bimonthly Consumption volumes of formulation Tenofovir/Lamivudine/Efavirenz (TDF/3TC/EFV) 300mg/300mg/600mg[Pack 30] (converted into an estimated Patients figure by dividing by 2.0) with Patient Numbers for regimens TDF/3TC/EFV (ADULT) and TDF/3TC/EFV (PMTCT)

2) For Sample Formulation 2, Paediatric ABC/3TC: Compares bimonthly Consumption volumes of formulation Abacavir/Lamivudine (ABC/3TC) 60mg/30mg [Pack 60] (converted into an estimated Patients figure by dividing by 4.6) with Patient Numbers for regimens ABC/3TC/EFV (PAED), ABC/3TC/NVP (PAED) and ABC/3TC/LPV/r (PAED)

3) For Sample Formulation 3, Paediatric EFV: Compares bimonthly Consumption volumes of formulation Efavirenz (EFV) 200mg [Pack 90] (converted into an estimated Patients figure by dividing by 1.0) with Patient Numbers for regimens ABC/3TC/EFV (PAED) and AZT/3TC/EFV (PAED)""",
        "test_type": "FACILITY_AND_SAMPLE_FORMULATION",
    },
    {
        "name": "NON-REPEATING",
        "short_description": "NON-REPEATING: Order changes in consecutive cycles?",
        "description": """This test is carried out for the system's three Sample Formulations: 1) Adult TDF/3TC/EFV (300/300/600mg), 2) Paediatric ABC/3TC (60/30mg), and 3) Paediatric EFV(200mg)

Tests if the facility has submitted the same order in consecutive cycles. This is done by comparing certain key datapoints (Opening Balance, ART Consumption, Closing Balance and Estimated New ART Patients) from a given cycle with the same datapoints reported in the previous cycle""",
        "test_type": "FACILITY_AND_SAMPLE_FORMULATION",
    },
    {
        "name": "OPENING = CLOSING",
        "short_description": "OPENING = CLOSING: Opening  balance = Closing balance from previous cycle?",
        "description": """This test is carried out for the system's three Sample Formulations: 1) Adult TDF/3TC/EFV (300/300/600mg), 2) Paediatric ABC/3TC (60/30mg), and 3) Paediatric EFV(200mg)

Tests if the "Opening Balance" reported by the facility in one cycle is the same as the "Closing Balance" result of the previous cycle""",
        "test_type": "FACILITY_AND_SAMPLE_FORMULATION",
    },
    {
        "name": "STABLE CONSUMPTION",
        "short_description": "STABLE CONSUMPTION: Consumption changes by less than 50% vs. previous cycle?",
        "description": """This test is carried out for the system's three Sample Formulations: 1) Adult TDF/3TC/EFV (300/300/600mg), 2) Paediatric ABC/3TC (60/30mg), and 3) Paediatric EFV(200mg)

Tests if the facility's total Consumption volume (i.e. ART Consumption + PMTCT Consumption) in a given cycle is stable relative to that of the previous cycle, with stability defined as a change of less than 50%. This test is run for the system's three Sample Formulations but excludes facilities that are considered "low volume", according to the following rules:

1) For Sample Formulation 1, Adult TDF/3TC/EFV: Total consumption in either cycle must be at least 20 packs

2) For Sample Formulation 2, Paediatric ABC/3TC: Total consumption in either cycle must be at least 10 packs

3) For Sample Formulation 3, Paediatric EFV: Total consumption in either cycle must be at least 10 packs""",
        "test_type": "FACILITY_AND_SAMPLE_FORMULATION",
    },
    {
        "name": "WAREHOUSE FULFILMENT",
        "short_description": "WAREHOUSE FULFILMENT: Volume delivered = volume ordered in previous cycle?",
        "description": """This test is carried out for the system's three Sample Formulations: 1) Adult TDF/3TC/EFV (300/300/600mg), 2) Paediatric ABC/3TC (60/30mg), and 3) Paediatric EFV(200mg)

Tests if the "Quantity Received" reported by the facility in one cycle is the same as the "Packs Ordered" result of the previous cycle.
This test can therefore reflect more than just the facility's ability to input correct figures as per what has been delivered. It also tests warehouse ability to correctly deliver what has been requested""",
        "test_type": "FACILITY_AND_SAMPLE_FORMULATION",
    },
    {
        "name": "NRTI vs. INSTI/NNRTI/PI patient volumes (ADULT)",
        "short_description": "NRTI vs. INSTI/NNRTI/PI patient volumes (ADULT): Differ by <30%?",
        "description": """Tests if the current patient numbers implied by facility's reported Adult NRTI consumption volumes are similar to those implied by the reported Adult NNRTI/PI consumption volumes

This is done by taking total consumption volumes (ART and PMTCT) for each of the formulations below, converting to patient numbers (by dividing through by 2.0 for all formulations), summing the totals for both sets of formulations (NRTI and NNRTI/PI) separately, and finally testing if the two resulting figures are within 30% of each other.

NRTI formulations: TDF/3TC 300/300mg, AZT/3TC 300/150mg, ABC/3TC 600/300mg
NNRTI/PI formulations: NVP 200mg, EFV 600mg, ATV/r 300/100mg, LPV/r 200/50mg""",
        "test_type": "FACILITY_ONLY",
    },
    {
        "name": "NRTI vs. INSTI/NNRTI/PI patient volumes (PAED)",
        "short_description": "NRTI vs. INSTI/NNRTI/PI patient volumes (PAED): Differ by <30%?",
        "description": """Tests if the current patient numbers implied by facility's reported Paediatric NRTI consumption volumes are similar to those implied by the reported Paediatric NNRTI/PI consumption volumes

This is done by taking total consumption volumes (ART and PMTCT) for each of the formulations below, converting to patient numbers (by dividing through by 4.6 for all formulations apart from EFV 200mg which you divide through by 1.0), summing the totals for both sets of formulations (NRTI and NNRTI/PI) separately, and finally testing if the two resulting figures are within 30% of each other

NRTI formulations: AZT/3TC 60/30mg, ABC/3TC 60/30mg
NNRTI/PI formulations: NVP 50mg, EFV 200mg, LPV/r 100/25mg, LPV/r 80/20mg""",
        "test_type": "FACILITY_ONLY",
    },
]


def create_default_tests(apps, schema_editor):
    model = apps.get_registered_model("dashboard", "FacilityTest")
    for test in default_tests:
        model.objects.create(**test)


class Migration(migrations.Migration):
    dependencies = [("dashboard", "0028_facilitytest_test_type")]

    operations = [migrations.RunPython(create_default_tests)]
