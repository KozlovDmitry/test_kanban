from rest_framework.exceptions import ValidationError
from ..models import *
import datetime


class Helper:
    def __init__(self, my_context=None):
        self.my_context = my_context

    @staticmethod
    def general_check(validated_data):
        if len(validated_data['fields']) == 0:
            raise ValidationError('fields - This field is required.', code=400)

        helper = Helper({
            'board': validated_data['board'],
            'column': validated_data['column'],
            'fields': validated_data['fields'],

        })

        list(map(
            helper.check_field,
            validated_data['fields']
        ))
        field_types = [item['field_type'] for item in helper.my_context['fields']]
        helper.check_mandatory_fields(field_types)

    @staticmethod
    def create_card(validated_data):
        card = Card(
            title=validated_data['title'],
            text=validated_data['text'],
            board=validated_data['board'],
            column=validated_data['column']
        )
        card.save()
        return card

    @staticmethod
    def create_fields(fields, card):
        fields_list = list(map(
            lambda field: Field(
                value=field['value'],
                field_type=field['field_type'],
                card=card
            ),
            fields
        ))
        return Field.objects.bulk_create(fields_list)

    @staticmethod
    def create_fields(fields, card):
        fields_list = list(map(
            lambda field: Field(
                value=field['value'],
                field_type=field['field_type'],
                card=card
            ),
            fields
        ))

        return Field.objects.bulk_create(fields_list)

    @staticmethod
    def update_fields(fields, card):
        old_fields = card.fields.all()
        old_fields_types = [item.field_type for item in card.fields.all()]
        update_field_list = []
        create_field_list = []
        def updater(field):
            if field['field_type'] in old_fields_types:
                new_field = old_fields.get(field_type=field['field_type'])
                new_field.value = field['value']
                update_field_list.append(new_field)
            else:
                new_field = Field(
                    value=field['value'],
                    field_type=field['field_type'],
                    card=card
                )
                create_field_list.append(new_field)
            return new_field

        list(map(
            updater,
            fields
        ))

        Field.objects.bulk_create(create_field_list)
        Field.objects.bulk_update(update_field_list, ['value'])

        return None

    @staticmethod
    def get_tips():
        template = {
            'tip': 'For card filter use POST-request like that',
            'board': 1,
            'filter': {
                'time_from': "2021-01-01 00:00",
                'time_to': "2021-01-05 00:00",
                'exact': 'exact statement',
                'contains': 'fuzzy statement',
                'lt': '<',
                'lte': '<=',
                'gt': '>',
                'gte': '>='
            }
        }
        return template

    @staticmethod
    def card_filter(request):
        try:
            data = request.data
        except Exception:
            raise ValidationError(Helper.get_tips(), code=400)
        if 'board' not in data:
            raise ValidationError('board is mandatory field', code=400)

        cards = Helper.apply_filter(data)
        return cards

    @staticmethod
    def apply_filter(data):
        try:
            board = Board.objects.get(id=data['board'])
        except Exception:
            raise ValidationError(f"There is no board with id {data['board']}", code=404)

        cards = Card.objects.filter(board=board)

        time_fields = Field.objects.filter(card__in=cards,
                                           field_type__in=AvailableField.objects.filter(board=board, type='datetime').all())
        int_fields = Field.objects.filter(card__in=cards,
                                          field_type__in=AvailableField.objects.filter(board=board, type='integer').all())
        text_fields = Field.objects.filter(card__in=cards,
                                           field_type__in=AvailableField.objects.filter(board=board, type__in=['text area', 'text']).all())

        if 'filter' in data:
            suit_fields = []

            if 'time_from' in data['filter']:
                Helper.time_format_check(data['filter']['time_from'], 'time_from')
                suit_fields.append(time_fields.filter(value__gte=data['filter']['time_from']))
            if 'time_to' in data['filter']:
                Helper.time_format_check(data['filter']['time_to'], 'time_to')
                suit_fields.append(time_fields.filter(value__lte=data['filter']['time_to']))
            if 'exact' in data['filter']:
                suit_fields.append(text_fields.filter(value__exact=data['filter']['exact']))
            if 'contains' in data['filter']:
                suit_fields.append(text_fields.filter(value__icontains=data['filter']['contains']))
            if 'lt' in data['filter']:
                Helper.int_format_check(data['filter']['lt'], 'lt')
                suit_fields.append(int_fields.filter(value__lt=data['filter']['lt']))
            if 'lte' in data['filter']:
                Helper.int_format_check(data['filter']['lte'], 'lte')
                suit_fields.append(int_fields.filter(value__lte=data['filter']['lte']))
            if 'gt' in data['filter']:
                Helper.int_format_check(data['filter']['gt'], 'gt')
                suit_fields.append(int_fields.filter(value__gt=data['filter']['gt']))
            if 'gte' in data['filter']:
                Helper.int_format_check(data['filter']['gte'], 'gte')
                suit_fields.append(int_fields.filter(value__gte=data['filter']['gte']))

            result = {
                'result_set': None
            }

            def result_set_builder(queryset):
                queryset = set(queryset)
                if result['result_set'] is None:
                    result['result_set'] = queryset
                result['result_set'] &= queryset

            def get_suit_cards(fields):
                return Card.objects.filter(fields__in=fields)

            suit_cards = list(map(
                get_suit_cards,
                suit_fields
            ))

            list(map(
                result_set_builder,
                suit_cards
            ))
            cards = set(result['result_set'])

        return cards

    @staticmethod
    def time_format_check(time, filter_field):
        try:
            datetime.datetime.fromisoformat(time)
        except Exception:
            raise ValidationError(f"Possible format for {filter_field} -"
                                  f" YYYY-MM-DD[*HH[:MM[:SS[.fff[fff]]]][+HH:MM[:SS[.ffffff]]]]", code=400)
        return None

    @staticmethod
    def int_format_check(num, filter_field):
        try:
            int(num)
        except Exception:
            raise ValidationError(f"Possible format for {filter_field} - integer", code=400)
        return None

    def check_field(self, field):
        self.check_exist_filed(field)
        self.check_data_field(field)
        return True

    def check_exist_filed(self, field):
        available_fields = self.my_context['board'].available_field.all()

        if field['field_type'] not in available_fields:
            raise ValidationError(f'Available fields: {", ".join([item.id for item in available_fields])}', code=400)

    def check_mandatory_fields(self, field_types):
        mandatory_fields = self.my_context['board'].available_field.filter(required=True)

        def checker(mandatory_field):
            if mandatory_field not in field_types:
                raise ValidationError(f'Mandatory fields: {", ".join([f"{item.id}({item.name})" for item in mandatory_fields])}. '
                                      f'You passed only: {", ".join([f"{item.id}({item.name})" for item in field_types])}', code=400)

        list(map(
            checker,
            mandatory_fields
        ))

    def check_data_field(self, field):
        if field['field_type'].type == 'integer':
            try:
                int(field['value'])
            except ValueError or TypeError:
                raise ValidationError(f'Field {field["field_type"].id}({field["field_type"].name}) should be integer', code=400)

        if field['field_type'].type == 'datetime':
            try:
                datetime.datetime.fromisoformat(field['value'])
            except ValueError or TypeError:
                raise ValidationError(f'Possible format for {field["field_type"].id}({field["field_type"].name}): '
                                 f'YYYY-MM-DD[*HH[:MM[:SS[.fff[fff]]]][+HH:MM[:SS[.ffffff]]]]', code=400)
        return True



