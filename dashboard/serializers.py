from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from dashboard.models import Score


class FacilityScoreSerializer(ModelSerializer):
    class Meta:
        model = Score


class JSONSerializerField(serializers.Field):
    """ Serializer for JSONField -- required to make field writable"""

    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        return value


class ScoreSerializer(ModelSerializer):
    REPORTING = JSONSerializerField()
    WEB_BASED = JSONSerializerField()
    MULTIPLE_ORDERS = JSONSerializerField()
    OrderFormFreeOfGaps = JSONSerializerField()
    guidelineAdherenceAdult1L = JSONSerializerField()
    guidelineAdherenceAdult2L = JSONSerializerField()
    guidelineAdherencePaed1L = JSONSerializerField()
    nnrtiPaed = JSONSerializerField()
    nnrtiAdults = JSONSerializerField()
    stablePatientVolumes = JSONSerializerField()
    consumptionAndPatients = JSONSerializerField()
    warehouseFulfilment = JSONSerializerField()
    differentOrdersOverTime = JSONSerializerField()
    closingBalanceMatchesOpeningBalance = JSONSerializerField()
    orderFormFreeOfNegativeNumbers = JSONSerializerField()
    stableConsumption = JSONSerializerField()

    class Meta:
        model = Score


class NewImportSerializer(serializers.Serializer):
    period = serializers.CharField()
