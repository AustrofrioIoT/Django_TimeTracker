import django_filters

from core.models import EventTime


class EventTimeFilters(django_filters.FilterSet):
    class Meta:
        model = EventTime
        fields = ('event','owner')
        # fields = {
        #     'start_datetime': ['contains'],
        # }
