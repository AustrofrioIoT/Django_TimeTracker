from django.db.models import fields
from django.forms import *
import datetime
from .models import Event, EventTime
from business.models import Employee
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker
from django.utils import timezone
from django.db.models import Q

class EventForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
            form.field.widget.attrs['autofocus'] = True

        self.fields['start_datetime'] = DateTimeField(
            widget=DateTimePicker(
                options={
                    "format": "YYYY-MM-DD HH:mm:ss",
                    'useCurrent': True,
                    'collapse': False,
                }
            ),
        )

    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Insert Name Event',
                }
            ),
            'time_to_finish': TextInput(
                attrs={
                    'placeholder': 'Insert Event Time (hours)',
                }
            ),
        }

class EventTimeForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['owner'].queryset = Employee.objects.filter(user__is_active=True).filter(user__is_superuser=False)        
        self.fields['event'].widget.attrs['disabled'] = 'disabled'
        self.fields['start_datetime'] = DateTimeField(
            widget=DateTimePicker(
                options={
                    "format": "YYYY-MM-DD HH:mm:ss",
                    'sideBySide': True,
                }
            )
        )

        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
            form.field.widget.attrs['autofocus'] = True

    class Meta:
        model = EventTime
        fields = '__all__'
        exclude = ('end_datetime', 'is_overtime', 'time_excess', 'time_afk', 'is_skipped')

    def clean(self):
        cleaned_data = super(EventTimeForm, self).clean()
        event = cleaned_data.get('event')
        owner = cleaned_data.get('owner')        
        evento_request = Event.objects.get(name="Start Shift")
        # is_finished = cleaned_data.get('is_finished')
        start_datetime = cleaned_data.get('start_datetime')
        if EventTime.objects.filter(start_datetime__date=start_datetime).filter(event=event).filter(owner=owner).exists():
            raise forms.ValidationError("There is already an event created that day")
        if not EventTime.objects.filter(Q(is_finished=0), Q(event=evento_request.id)).exists() and evento_request != event:
           raise forms.ValidationError("Invalid option, You need to start the day") 




class EventTimeFormUpdate(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['owner'].queryset = Employee.objects.filter(user__is_active=True).filter(user__is_superuser=False)
        self.fields['owner'].widget.attrs['readonly'] = True

        instance = getattr(self, 'instance', None)
        # print(instance.id)
        if instance and instance.id:
            self.fields['owner'].required = False
            self.fields['owner'].widget.attrs['disabled'] = 'disabled'

        # DateTimePicjer Configurartion after install pip install django-tempus-dominus
        self.fields['start_datetime'] = DateTimeField(
            widget=DateTimePicker(
                options={
                    "format": "YYYY-MM-DD HH:mm:ss",
                    # 'minDate': datetime.date.today().strftime('%Y-%m-%d'),  # Tomorrow
                    'useCurrent': True,
                    'collapse': False,
                }
            ),
        )
        # DateTimePicjer Configurartion after install pip install django-tempus-dominus

        self.fields['end_datetime'] = DateTimeField(
            widget=DateTimePicker(
                options={
                    "format": "YYYY-MM-DD HH:mm:ss",
                    'sideBySide': True,
                }
            ),
            required=False
        )

        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
            form.field.widget.attrs['autofocus'] = True

    class Meta:
        model = EventTime
        fields = '__all__'
        exclude = ('is_overtime', 'time_excess', 'time_afk', 'is_skipped')

    def clean(self):
        cleaned_data = super(EventTimeFormUpdate, self).clean()
        event = cleaned_data.get('event')
        owner = cleaned_data.get('owner')
        # is_finished = cleaned_data.get('is_finished')
        start_datetime = cleaned_data.get('start_datetime')
        end_datetime = cleaned_data.get('end_datetime')
        eventtime_id = cleaned_data.get('id_eventtime')
        instance = getattr(self, 'instance', None)

        variable = EventTime.objects.filter(start_datetime__date=start_datetime).filter(event=event).filter(owner=owner).first()

        if variable:
            if instance.id != variable.id:
                raise ValidationError("Duplicates Events Same Day ")
            else:
                print("entra al else:",variable.id)
        else:

            if end_datetime != None and not (start_datetime <= end_datetime):
                raise ValidationError('Invalid start and end datetime')

    # This Function Is Used To keep the PK Name in Select Option
    def clean_owner(self):
        instance = getattr(self, 'instance', None)
        if instance:
            return instance.owner
        else:
            return self.cleaned_data.get('instance', None)
