
from django.contrib import admin
from django.urls import path,include
from skote import views
from .views import MyPasswordSetView ,MyPasswordChangeView
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    #display
    path('', include("display.urls")),

    # Dashboards View
    path('dashboard_default',views.DashboardView.as_view(),name='dashboard'),
    path('dashboard_saas',views.SaasView.as_view(),name='dashboard_saas'),
    path('dashboard_crypto',views.CryptoView.as_view(),name='dashboard_crypto'),
    path('dashboard_blog',views.BlogView.as_view(),name='dashboard_blog'),
    # Calender View
    path('calendar',views.CalendarView.as_view(),name='calendar'),
    path('full-calendar',views.CalendarFullView.as_view(),name='full-calendar'),
    # Chat View
    path('chat',views.ChatView.as_view(),name='chat'),
    # Layouts
    path('layout/',include('layout.urls')),
    # File manager View
    path('filemanager',views.FileManagerView.as_view(),name='filemanager'),
    #Ecommerce
    path('ecommerce/',include("ecommerce.urls")),
    #Crypto
    path('crypto/',include('crypto.urls')),
    #Email
    path("email/",include("e_mail.urls")),
    #Invoices
    path('invoices/',include('invoices.urls')),
    #Projects
    path('projects/',include('projects.urls')),
    #Tasks
    path('tasks/',include('tasks.urls')),
    #Blog
    path('blog/',include('blog.urls')),
    #Blog
    path('contacts/',include('contacts.urls')),
    #Authencation
    # path('authentication/',include('authentication.urls')),
    #Pages
    path('pages/',include('pages.urls')),
    #Components
    path('components/',include('components.urls')),
    # Allauth
    path('account/', include('allauth.urls')),
    path('auth-logout/',TemplateView.as_view(template_name="account/logout-success.html"),name ='pages-logout'),
    path('auth-lockscreen/',TemplateView.as_view(template_name="account/lock-screen.html"),name ='pages-lockscreen'),
        #Custum change password done page redirect
    path('accounts/password/change/', login_required(MyPasswordChangeView.as_view()), name="account_change_password"),
    #Custum set password done page redirect
    path('accounts/password/set/', login_required(MyPasswordSetView.as_view()), name="account_set_password"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

