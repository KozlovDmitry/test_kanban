from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *


class BoardList(generics.ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer


class BoardDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer


class ColumnList(generics.ListCreateAPIView):
    queryset = Column.objects.all()
    serializer_class = ColumnSerializer


class ColumnDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Column.objects.all()
    serializer_class = ColumnSerializer


class ColumnOrderingList(generics.ListCreateAPIView):
    queryset = ColumnOrdering.objects.all()
    serializer_class = ColumnOrderingSerializer


class ColumnOrderingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ColumnOrdering.objects.all()
    serializer_class = ColumnOrderingSerializer


class AvailableFieldList(generics.ListCreateAPIView):
    queryset = AvailableField.objects.all()
    serializer_class = AvailableFieldSerializer


class AvailableFieldDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = AvailableField.objects.all()
    serializer_class = AvailableFieldSerializer


class CardList(generics.ListCreateAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer


class CardDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer


class CardFilter(Helper, APIView):
    def get(self, request):
        ser = TipSerializer(data=Helper.get_tips())
        if ser.is_valid():
            return Response(ser.validated_data)

    def post(self, request, *args, **kwargs):
        cards = Helper.card_filter(request)
        ser = CardSerializer(cards, many=True)
        return Response(ser.data)
