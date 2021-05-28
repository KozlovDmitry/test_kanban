from django.db import models


class Board(models.Model):
    name = models.CharField(max_length=100)
    column = models.ManyToManyField('Column', related_name='board', through='ColumnOrdering', blank=True, null=True)
    available_field = models.ManyToManyField('AvailableField', related_name='board', blank=True, null=True)

    def __str__(self):
        return self.name


class ColumnOrdering(models.Model):
    board = models.ForeignKey('Board', on_delete=models.CASCADE)
    column = models.ForeignKey('Column', related_name='order_rule', on_delete=models.CASCADE)
    order = models.IntegerField()

    class Meta:
        unique_together = ['board', 'column']
        ordering = ['order']

    def __str__(self):
        return f"{self.board.name} - {self.column.name}"


class Column(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['order_rule']

    def __str__(self):
        return self.name


class AvailableField(models.Model):
    types = [
        ('datetime', 'datetime'),
        ('integer', 'integer'),
        ('text area', 'text area'),
        ('text', 'text')
    ]

    name = models.CharField(max_length=100)
    required = models.BooleanField()
    type = models.CharField(choices=types, max_length=32)

    def __str__(self):
        return self.name


class Field(models.Model):
    value = models.TextField()
    field_type = models.ForeignKey('AvailableField', related_name='field', on_delete=models.CASCADE)
    card = models.ForeignKey('Card', related_name='fields', on_delete=models.CASCADE)

    def __str__(self):
        return self.value


class Card(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    board = models.ForeignKey('Board', related_name='card', on_delete=models.CASCADE)
    column = models.ForeignKey('Column', related_name='card', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
