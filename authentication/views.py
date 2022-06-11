from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import LoginForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_http_methods
from .helpers import account_activation_token, generate_password
from .models import User
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from client_mgt.models import CorporateClient
from django.contrib import messages
from e_mail import send
from django.contrib.auth.mixins import LoginRequiredMixin
from corporate_portal.mixins import GroupRequiredMixin
# Create your views here.

# Authentication
class AuthLoginView(View):
    template_name = 'authentication-actual/auth-login.html'
    form_class = LoginForm

    def get(self , request):
        form = self.form_class()
        return render (request,self.template_name, context={'form':form})
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password, is_activated=True)
            if user is not None:
                login(request, user)
                return redirect('portal:dashboard')
            else:
                messages.add_message(request, messages.WARNING, 'Email or password is invalid')
        return render(request, self.template_name, context={'form':form})

@require_http_methods(["GET"])
def activate_cor_user(request, uidb64, token):
    """Check the activation token sent via mail."""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        messages.add_message(request, messages.WARNING, str(e))
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        if user.is_activated!=True:
            user.is_activated = True  # now we're activating the user
            user.save()
            company = CorporateClient.objects.get(user=user)
            return redirect('authentication:send-cor-pass-mail', slug=company.slug)
        else:
            messages.add_message(request, messages.SUCCESS, "Your account has been activated")
            return redirect('corporate_portal:login')
    else:
        messages.add_message(request, messages.WARNING, "Having issues setting up your account? Contact support")
        return redirect('corporate_portal:login')

@require_http_methods(["GET"])
def send_cor_password_mail(request, slug):
    company = get_object_or_404(CorporateClient, slug=slug)
    password = generate_password()
    company.user.set_password(password)
    company.user.save()
    send_mail = send.SendgridClient(recipients=[company.user.email])
    send_mail.set_template_id('d-16d58c90f9e742d6bb0f912342e960c8')
    send_mail.set_template_data({'company_name':company.company_name, 'password':password})
    send_mail.send()
    messages.add_message(request, messages.SUCCESS, 'Your password has been sent to {}'.format(company.main_contact_email))
    return redirect('corporate_portal:login')

class AuthLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('display:home-page')

class ChangeCorPassword(LoginRequiredMixin,GroupRequiredMixin, View):
    login_url = '/business/login'
    redirect_field_name = 'redirect_to'
    group_required = [u'Corporate group']
    form_class = PasswordChangeForm

    def get(self, request, slug):
        company = get_object_or_404(CorporateClient, slug=slug)
        form = self.form_class()
        return render(request, 'cor_temp/change-password.html', context={'form':form, 'company':company})

    def post(self, request, slug):
        company = get_object_or_404(CorporateClient, slug=slug)
        form = self.form_class(request.POST)
        print(form.errors)
        if form.is_valid():
            password = form.cleaned_data['password']

            user = company.user
            user.set_password(password)
            user.save()
            print('success')
            messages.add_message(request, messages.SUCCESS, 'Your password has been changed')
        else:
            messages.add_message(request, messages.WARNING, 'Inputted passwords are not the same')
            return render(request, 'cor_temp/change-password.html', context={'form':form, 'company':company})
        return render(request, 'cor_temp/change-password.html', context={'form':form, 'company':company})
