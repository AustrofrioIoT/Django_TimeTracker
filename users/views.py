from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from .models import User


# Create your views here.
class UsuarioList(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = 'user/list.html'
    permission_required = 'user.view_user'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return User.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'User List'
        context['crear_url'] = reverse_lazy('users:create_user')
        context['list_url'] = reverse_lazy('users:list_user')
        context['entity'] = 'Usuarios'
        return context
