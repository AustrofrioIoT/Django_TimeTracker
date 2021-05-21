from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse, response
from django.shortcuts import render
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.utils.timezone import localtime, now
from django.db.models import Q

from core.models import Event, EventTime
from core.forms import EventTimeForm, EventTimeFormUpdate
from business.models import Employee, Company, Department, Role
from business.forms import UserEditMultiForm, UserCreationMultiForm, CompanyForm, DepartmentForm, RoleForm
from django.db import transaction

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from datetime import timedelta, datetime, date
from .filters import EventTimeFilters

import csv

User = get_user_model()


class Dashboard(LoginRequiredMixin, generic.TemplateView):
    template_name = 'dash/admin-dash.html'
    login_url = 'webapp:login'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events_today'] = EventTime.objects.all()[:5]
        context['employees'] = Employee.objects.filter(user__is_staff=False).filter(user__is_active=True).filter(
            type_of_employee__type_employee="Employee")[:5]
        context['managers'] = Employee.objects.filter(user__is_staff=False).filter(user__is_active=True).filter(
            type_of_employee__type_employee="Manager")[:5]
        return context


class DashEmployees(LoginRequiredMixin, generic.ListView):
    model = Employee
    template_name = 'dash/admin-employees.html'
    login_url = 'webapp:login'

    def get_queryset(self):
        return Employee.objects.filter(user__is_staff=False, user__is_active=True,
                                       type_of_employee__type_employee="Employee").order_by('-id')


class DashManagers(LoginRequiredMixin, generic.ListView):
    model = Employee
    template_name = 'dash/admin-managers.html'
    login_url = 'webapp:login'

    def get_queryset(self):
        return Employee.objects.filter(user__is_staff=False, user__is_active=True,
                                       type_of_employee__type_employee="Manager").order_by('-id')


class DashEmployeeCreate(LoginRequiredMixin, generic.CreateView):
    form_class = UserCreationMultiForm
    template_name = "dash/admin-employees-create.html"
    success_url = reverse_lazy('webapp:admin-employees')
    login_url = 'webapp:login'

    def form_valid(self, form):
        user = form['user'].save()
        employee = form['employee'].save(commit=False)
        employee.user = user
        employee.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('webapp:admin-employees')

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            self.object = None
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(self.get_forbidden())

    def get_forbidden(self):
        return reverse_lazy('webapp:forbidden')


class DashEmployeeUpdate(LoginRequiredMixin, generic.UpdateView):
    model = User
    form_class = UserEditMultiForm
    template_name = "dash/admin-employees-update.html"
    success_url = reverse_lazy('webapp:admin-employees')
    login_url = 'webapp:login'

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            self.object = self.get_object()
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(self.get_forbidden())

    def get_forbidden(self):
        return reverse_lazy('webapp:forbidden')

    def get_form_kwargs(self):
        kwargs = super(DashEmployeeUpdate, self).get_form_kwargs()
        kwargs.update(instance={
            'user': self.object,
            'employee': self.object.employee,
        })
        # print('self.object ----------->  ', self.object)
        # print('self.object.employee ----------->  ', self.object.employee)
        return kwargs


class DashEmployeeDelete(LoginRequiredMixin, generic.DeleteView):
    model = Employee
    template_name = "dash/admin-employees-delete.html"
    success_url = reverse_lazy('webapp:admin-employees')


class DashEventTimes(LoginRequiredMixin, generic.ListView):
    model = EventTime
    template_name = 'dash/admin-whois.html'
    form_class = EventTimeForm
    login_url = 'webapp:login'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class
        context['filter'] = EventTimeFilters(self.request.GET, queryset=self.get_queryset())
        return context

    def get_queryset(self):
        return EventTime.objects.all().order_by('-id')


class AdminEventTimeList(LoginRequiredMixin, generic.ListView):
    model = EventTime
    template_name = 'dash/admin-whois.html'
    login_url = 'webapp:login'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return EventTime.objects.filter()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'List of AdminEvents'
        context['entity'] = 'Events'
        return context


class EventTimeUpdate(generic.UpdateView):
    model = EventTime
    form_class = EventTimeFormUpdate
    template_name = "dash/admin-eventtime-update.html"
    success_url = reverse_lazy("webapp:admin-whois")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_url'] = reverse_lazy("webapp:admin-whois")
        return context

def update_event(instance):
    instance.is_finished = True
    instance.end_datetime = datetime.now()       
    instance.save()

def final_event(request, id):
    event_open = EventTime.objects.filter(Q(is_finished=0), Q(owner=id))
    for i in event_open:
        update_event(i)
    context = {
        'icon': 'success',
        'title': 'Correcto',
        'text': 'End Shift'
        }
    return JsonResponse(context)   

class EventTimeCreate(LoginRequiredMixin, generic.CreateView):
    model = EventTime
    template_name = "dash/admin-eventtime-create.html"
    form_class = EventTimeForm
    success_url = reverse_lazy("webapp:admin-whois")

    def post(self, request, *args, **kwargs):
        owner_request = self.request.POST.get('owner')
        event_request = self.request.POST.get('event')                                
        form = self.form_class(request.POST)
        form = self.form_class(request.POST)        
        if form.is_valid():
            try:
                event_open = EventTime.objects.filter(Q(is_finished=0), Q(owner=owner_request))
                for i in event_open:
                    if i.event_id != 5 and i.event_id != 1:
                        t = update_event(i)
                        print(t)                 
            except ValueError as err:                
                print(str(err))
            form.save()
            return HttpResponseRedirect(self.success_url)
        self.object = None
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class
        context['title'] = 'Configure an EventTime'
        context['list_url'] = reverse_lazy("webapp:admin-whois")
        return context


class EventTimeDelete(generic.DeleteView):
    model = EventTime
    template_name = "dash/admin-eventtime-delete.html"
    success_url = reverse_lazy("webapp:admin-eventtime")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete an EventTime'
        context['entity'] = 'Event'
        return context

def evntime(request, id):
    event_applied = EventTime.objects.filter(Q(is_finished=0), Q(owner=id))                      
    if len(event_applied) == 0:
        event_send = 0
    else:
        for i in event_applied:
            if i.event_id != 5:
                event_send = i.event_id                
            else:
                if len(event_applied) == 1:
                   event_send = 5 

    context = {'evento_apl': event_send}
    return JsonResponse(context)

class Settings(LoginRequiredMixin, generic.TemplateView):
    template_name = 'dash/settings.html'
    login_url = 'webapp:login'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['companies'] = Company.objects.all()
        context['departments'] = Department.objects.all()
        context['roles'] = Role.objects.all()
        context['add-company'] = reverse_lazy('webapp:company-create')
        return context


class CompanyDelete(generic.DeleteView):
    model = Company
    template_name = "dash/company-delete.html"
    success_url = reverse_lazy("webapp:settings")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete an Company'
        context['entity'] = 'Company'
        return context


class DepartmentDelete(generic.DeleteView):
    model = Department
    template_name = "dash/department-delete.html"
    success_url = reverse_lazy("webapp:settings")


class RoleDelete(generic.DeleteView):
    model = Role
    template_name = "dash/role-delete.html"
    success_url = reverse_lazy("webapp:settings")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete an Role'
        context['entity'] = 'Role'
        return context


class CompanyCreate(LoginRequiredMixin, generic.CreateView):
    model = Company
    template_name = "dash/company-create.html"
    form_class = CompanyForm
    success_url = reverse_lazy("webapp:settings")

    def post(self, request, *args, **kwargs):
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.success_url)
        self.object = None
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create an Company'
        context['entity'] = 'Company'
        return context


class DepartmentCreate(LoginRequiredMixin, generic.CreateView):
    model = Department
    template_name = "dash/department-create.html"
    form_class = DepartmentForm
    success_url = reverse_lazy("webapp:settings")

    def post(self, request, *args, **kwargs):
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.success_url)
        self.object = None
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class RoleCreate(LoginRequiredMixin, generic.CreateView):
    model = Role
    template_name = "dash/role-create.html"
    form_class = RoleForm
    success_url = reverse_lazy("webapp:settings")

    def post(self, request, *args, **kwargs):
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.success_url)
        self.object = None
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=EventTime' + str(datetime.now()) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['owner', 'event', 'start_datetime', 'end_datetime', 'time_excess', 'time_afk', 'is_skipped'])

    # eventtimes = EventTime.objects.filter(owner= request.user)
    eventtimes = EventTime.objects.all()

    for eventime in eventtimes:
        writer.writerow(
            [eventime.owner, eventime.event, eventime.start_datetime, eventime.end_datetime, eventime.time_excess,
             eventime.time_afk, eventime.is_skipped])
    return response
