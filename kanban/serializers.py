from rest_framework import serializers
from .libs.my_libs import Helper
from .models import *


class TipSerializer(serializers.Serializer):
    tip = serializers.CharField()
    board = serializers.IntegerField()
    filter = serializers.DictField()


class ColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = '__all__'


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['column'] = [item.name for item in instance.column.all()]
        rep['available_field'] = [f"{item.id}: {item.name}" for item in instance.available_field.all()]
        return rep


class ColumnOrderingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColumnOrdering
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['column'] = instance.column.name
        rep['board'] = instance.board.name
        return rep


class AvailableFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableField
        fields = '__all__'


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = ['field_type', 'value']


class CardSerializer(serializers.ModelSerializer, Helper):
    fields = FieldSerializer(many=True)

    class Meta:
        model = Card
        fields = ['id', 'title', 'text', 'board', 'column', 'fields']

    def create(self, validated_data):
        Helper.general_check(validated_data)
        card = Helper.create_card(validated_data)
        Helper.create_fields(validated_data['fields'], card)
        return card

    def update(self, instance, validated_data):
        Helper.general_check(validated_data)
        Helper.update_fields(validated_data['fields'], instance)
        return instance


