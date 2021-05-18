from django.db import models
from django.utils import timezone
from datetime import timedelta, datetime, date
from business.models import Employee
from django.utils.timezone import localtime, now
from django.core.exceptions import ValidationError
import time

class Event(models.Model):
    """
    Event Model
    """
    name = models.CharField(max_length=120, unique=True, verbose_name="Nombre del Evento")
    time_to_finish = models.IntegerField(default=0, verbose_name="Tiempo de Duracion")
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank=True, null=True,
                               verbose_name="Clase Padre")

    def add_user_to_list_of_attendees(self, owner):
        registration = EventTime.objects.create(owner=owner, event=1, end_datetime=timezone.now(), is_finished=False,
                                                is_overtime=False, time_excess=0, )
        registration.save()

    def remove_user_from_list_of_attendees(self, owner):
        registration = EventTime.objects.get(owner=owner, event=self)
        registration.delete()

    def __str__(self):
        return '{}'.format(self.name)


class EventTime(models.Model):
    """
    Time Track of each event
    """
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    owner = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_datetime = models.DateTimeField(default=datetime.now)
    end_datetime = models.DateTimeField(blank=True, null=True)
    is_finished = models.BooleanField(default=False)
    is_overtime = models.BooleanField(default=False)
    time_excess = models.IntegerField(default=0)
    time_afk = models.IntegerField(default=0)
    is_skipped = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id', ]

    @property
    def get_day(self):
        print(start_datetime.date())
        return start_datetime.date()

    @property
    def time(self):
        if self.end_datetime is None:
            dif = timezone.now() - self.start_datetime
        else:
            dif = self.end_datetime-self.start_datetime
        return str(dif).split(".")[0]

    def end_task(self):
        """
        Sets the end time of an event and marks it as finished
        """
        self.end_datetime = timezone.now()
        self.is_finished = True
        dif = (int)((self.end_datetime - self.start_datetime) / timedelta(seconds=60))
        if self.event.time_to_finish > 0 and dif > self.event.time_to_finish:
            self.is_overtime = True
            self.time_excess = dif - self.event.time_to_finish
        if self.event.id == 5:
            self.time_afk = dif
        self.save()

    def save(self, *args, **kwargs):
        # super(EventTime, self).save(*args, **kwargs)
        if not self.is_finished:
            self.end_datetime = None
            self.is_finished = False
            self.is_overtime = False
            self.time_excess = 0
            self.time_afk = 0
            self.is_skipped = False
        # else:
        #     self.start_datetime = datetime.now()
        #     self.end_datetime = datetime.date.today().strftime('%Y-%m-%d')
        super(EventTime, self).save(*args, **kwargs)

    def __str__(self):
        return 'id={},owner={},event={},start_datetime={},end_datetime={}, is_finished={}>' \
            .format(self.id, self.owner, self.event.pk, self.start_datetime, self.end_datetime, self.is_finished)
