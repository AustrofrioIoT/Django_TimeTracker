from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.response import TemplateResponse
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.utils.timezone import localtime, now

from core.models import Event, EventTime
from core.forms import EventForm, EventTimeForm
from business.models import Employee
from users.models import User
from datetime import timedelta


class Home(LoginRequiredMixin, generic.TemplateView):
    template_name = 'webapp/home.html'
    login_url = 'webapp:login'

    def get_template_names(self):
        if self.request.user.is_superuser:
            template_name = 'dash/admin-dash.html'
        else:
            template_name = self.template_name
        return [template_name]

    def get_context_data(self, **kwargs):
        today = localtime(now()).date()
        context = super().get_context_data(**kwargs)

        if not self.request.user.is_superuser:
            employee_instance = Employee.objects.get(user=self.request.user)
            context['event_today'] = EventTime.objects.filter(owner=employee_instance, start_datetime__date=today,
                                                              event=1).first()
            context['firstbreak_today'] = EventTime.objects.filter(owner=employee_instance, start_datetime__date=today,
                                                                   event=2).first()
            context['lunch_today'] = EventTime.objects.filter(owner=employee_instance, start_datetime__date=today,
                                                              event=3).first()
            context['secondbreak_today'] = EventTime.objects.filter(owner=employee_instance, start_datetime__date=today,
                                                                    event=4).first()
            context['afk_today'] = EventTime.objects.filter(owner=employee_instance, start_datetime__date=today,
                                                            event=5).first()

        else:
            context['events_today'] = EventTime.objects.all()
            context['employees'] = Employee.objects.filter(user__is_active=True,
                                                           type_of_employee__type_employee="Employee")
            context['managers'] = Employee.objects.filter(user__is_active=True,
                                                          type_of_employee__type_employee="Manager")
        # print(context)
        return context


@csrf_exempt
@login_required
def punch_task(request):
    if request.POST.get('action') == 'post_event':
        flag = None
        today = localtime(now()).date()
        events = ['start', 'firstbreak', 'lunch', 'secondbreak']
        eventtimeid = request.POST.get('post_event_time_id')
        eventid = int(request.POST.get('post_event_id'))
        event_instance = Event.objects.get(id=eventid)
        employee_instance = Employee.objects.get(user=request.user)

        if eventtimeid in events or EventTime.objects.get(id=eventtimeid).is_finished:
            eventtimeid_obj = EventTime(event=event_instance, owner=employee_instance)
            print('before save ----> ', eventtimeid_obj)
            eventtimeid_obj.save()
            print('after save ----> ', eventtimeid_obj)
        else:
            if eventid == 1:
                events_obj = EventTime.objects.filter(owner=employee_instance, start_datetime__date=today)
                for e in events_obj:
                    eventtimeid_obj = EventTime.objects.get(id=e.id)
                    if not eventtimeid_obj.end_datetime:
                        eventtimeid_obj.end_task()
                    else:
                        print('EventTime {0} ya esta cerrado...'.format(eventtimeid_obj.id))
            else:
                eventtimeid_obj = EventTime.objects.get(id=eventtimeid)
                eventtimeid_obj.end_task()
        flag = eventtimeid_obj.is_finished
        url = reverse('webapp:home')
        return JsonResponse({'event_today': eventtimeid_obj.id, 'flag': flag, 'url': url})
    return HttpResponse("Error access denied")


@csrf_exempt
@login_required
def afk_task(request):
    if request.POST.get('action') == 'post_event':
        flag = None
        eventtimeid = request.POST.get('post_event_time_id')
        eventid = int(request.POST.get('post_event_id'))
        event_instance = Event.objects.get(id=eventid)
        employee_instance = Employee.objects.get(user=request.user)

        if eventtimeid == 'afk' or EventTime.objects.get(id=eventtimeid).is_finished:
            eventtimeid_obj = EventTime(event=event_instance, owner=employee_instance)
            eventtimeid_obj.save()
        else:
            eventtimeid_obj = EventTime.objects.get(id=eventtimeid)
            eventtimeid_obj.end_task()
        flag = eventtimeid_obj.is_finished
        url = reverse('webapp:home')
        return JsonResponse({'event_today': eventtimeid_obj.id, 'flag': flag, 'url': url})
    return HttpResponse("Error access denied")


@csrf_exempt
@login_required
def skip_task(request):
    if request.POST.get('action') == 'post_event':
        flag = None
        events = ['start', 'firstbreak', 'lunch', 'secondbreak']
        eventtimeid = request.POST.get('post_event_time_id')
        eventid = int(request.POST.get('post_event_id'))
        event_instance = Event.objects.get(id=eventid)
        employee_instance = Employee.objects.get(user=request.user)

        if eventtimeid in events:
            eventtimeid_obj = EventTime(event=event_instance, owner=employee_instance)
        else:
            eventtimeid_obj = EventTime.objects.get(id=eventtimeid)
        eventtimeid_obj.end_datetime = None
        eventtimeid_obj.is_finished = True
        eventtimeid_obj.is_skipped = True
        eventtimeid_obj.save()
        flag = eventtimeid_obj.is_finished
        url = reverse('webapp:home')
        return JsonResponse({'event_today': eventtimeid_obj.id, 'flag': flag, 'url': url})
    return HttpResponse("Error access denied")


class EventTimeList(LoginRequiredMixin, generic.ListView):
    model = EventTime
    template_name = 'webapp/eventtime_list.html'
    login_url = 'webapp:login'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Event List'
        context['entity'] = 'Events'
        return context

    def get_queryset(self):
        today = localtime(now()).date()
        employee_instance = Employee.objects.get(user=self.request.user)
        return EventTime.objects.filter(owner=employee_instance).filter(start_datetime__date=today).order_by('-id')


class EventTimeDetail(LoginRequiredMixin, generic.DetailView):
    model = EventTime


class EventTimeUpdate(LoginRequiredMixin, generic.UpdateView):
    model = EventTime
    form_class = EventTimeForm
    template_name = "webapp/event_detail.html"
    success_url = reverse_lazy("webapp:home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit an Event'
        context['entity'] = 'Events'
        context['list_url'] = reverse_lazy('webapp:home')
        return context


class EventTimeCreate(LoginRequiredMixin, generic.CreateView):
    model = EventTime
    template_name = "webapp/crear_evento.html"
    form_class = EventForm
    success_url = reverse_lazy("webapp:sheets")

    def post(self, request, *args, **kwargs):
        form = EventTimeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.success_url)
        self.object = None
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create an EventTime'
        context['entity'] = 'EventTime'
        context['list_url'] = reverse_lazy('webapp:sheets')
        return context


class EventTimeDelete(LoginRequiredMixin, generic.DeleteView):
    model = EventTime
    template_name = "webapp/eliminar_eventtime.html"
    success_url = reverse_lazy("webapp:sheets")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Event'
        context['entity'] = 'Event'
        return context


class EventCreate(LoginRequiredMixin, generic.CreateView):
    model = Event
    template_name = "webapp/crear_evento.html"
    form_class = EventForm
    success_url = reverse_lazy("webapp:event_create")

    def post(self, request, *args, **kwargs):
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.success_url)
        self.object = None
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create an Event'
        context['entity'] = 'Events'
        return context


class Forbidden(LoginRequiredMixin, generic.TemplateView):
    login_url = 'webapp:login'
    template_name = 'webapp/403.html'
