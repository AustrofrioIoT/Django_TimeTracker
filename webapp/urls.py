from django.urls import path
from django.contrib.auth import views as auth_views

from .views import *
from .views_admin import *
from . import views_admin
from webapp import views

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('sheets/', EventTimeList.as_view(), name='sheets'),
    path('punch/', punch_task, name='punch_task'),
    path('afk/', afk_task, name='afk_task'),
    path('skip/', skip_task, name='skip_task'),
    path('403/', Forbidden.as_view(), name='forbidden'),
    path('login/', auth_views.LoginView.as_view(template_name='webapp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='webapp/login.html'), name='logout'),
]

# Urls for Admins
urlpatterns += [
    path('dashboard/', Dashboard.as_view(), name='admin-dash'),
    path('dashboard/managers', DashManagers.as_view(), name='admin-managers'),
    path('dashboard/employees', DashEmployees.as_view(), name='admin-employees'),
    path('dashboard/employees/add', DashEmployeeCreate.as_view(), name='admin-employee-create'),
    path('dashboard/employees/update/<int:pk>', DashEmployeeUpdate.as_view(), name='admin-employee-update'),
    path('dashboard/employees/delete/<int:pk>', DashEmployeeDelete.as_view(), name='admin-employee-delete'),
    path('dashboard/whois', DashEventTimes.as_view(), name='admin-whois'),
    path('export-csv/', export_csv, name='export-csv'),
    path('dashboard/settings', Settings.as_view(), name='settings'),
    path('dashboard/settings/company/add', CompanyCreate.as_view(), name='company-create'),
    path('dashboard/settings/company/delete/<int:pk>', CompanyDelete.as_view(), name='company-delete'),
    path('dashboard/settings/department/add', DepartmentCreate.as_view(), name='department-create'),
    path('dashboard/settings/department/delete/<int:pk>', DepartmentDelete.as_view(), name='department-delete'),
    path('dashboard/settings/role/add', RoleCreate.as_view(), name='role-create'),
    path('dashboard/settings/role/delete/<int:pk>', RoleDelete.as_view(), name='role-delete'),
    path('dashboard/eventtime', AdminEventTimeList.as_view(), name='admin-eventtime'),
    path('dashboard/eventtime/add', EventTimeCreate.as_view(), name='admin-eventtime-create'),
    path('dashboard/eventtime/update/<int:pk>', EventTimeUpdate.as_view(), name='admin-eventtime-update'),
    path('dashboard/eventtime/delete/<int:pk>', EventTimeDelete.as_view(), name='admin-eventtime-delete'),
    path('dashboard/eventtime/prob_evnt/owner=<int:id>', views_admin.evntime, name='admin-eventtime-test'),
    path('dashboard/eventtime/end_shift/<int:id>', views_admin.final_event, name='admin-eventtime-end_shift')
]
