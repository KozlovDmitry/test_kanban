from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'board/$', BoardList.as_view()),
    url(r'board/(?P<pk>[0-9]+)/$', BoardDetail.as_view()),
    url(r'column/$', ColumnList.as_view()),
    url(r'column/(?P<pk>[0-9]+)/$', ColumnDetail.as_view()),
    url(r'columnordering/$', ColumnOrderingList.as_view()),
    url(r'columnordering/(?P<pk>[0-9]+)/$', ColumnOrderingDetail.as_view()),
    url(r'availablefield/$', AvailableFieldList.as_view()),
    url(r'availablefield/(?P<pk>[0-9]+)/$', AvailableFieldDetail.as_view()),
    url(r'card/$', CardList.as_view()),
    url(r'card/(?P<pk>[0-9]+)/$', CardDetail.as_view()),
    url(r'cardfilter/$', CardFilter.as_view()),

]