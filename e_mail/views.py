from email.message import EmailMessage
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import EmailForm
from .models import E_mail



# Create your views here.
class EmailHomeView(LoginRequiredMixin, View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    def get(self, request):
        emails = E_mail.objects.all()
        return render(request, 'email/email-home.html', context={'emails':emails})

class CreateEmailView(LoginRequiredMixin, View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    form_class= EmailForm
    def get(self, request):
        form = self.form_class()
        return render(request, 'email/edit-custom.html', context={'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save(commit=True)

            return redirect ('portal:email-home')
        return render(request, 'email/edit-custom.html', context={'form':form})


class EditEmailView(LoginRequiredMixin, View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    form_class= EmailForm
    def get(self, request, slug):
        form = self.form_class()
        email_obj = get_object_or_404(E_mail, slug=slug)
        return render(request, 'email/edit.html', context={'form':form, 'email':email_obj})

    def post(self, request, slug):
        email_obj = get_object_or_404(E_mail, slug=slug)
        form = self.form_class(request.POST, instance=email_obj)
        if form.is_valid():
            form.save(commit=True)

            return redirect ('portal:email-home')
        return render(request, 'email/edit.html', context={'form':form, 'email':email_obj})


