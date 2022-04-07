
from django.contrib import admin
from django.urls import path,include
from skote import views
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from django.conf.urls.static import static
from django.conf import settings

app_name='skote'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include("authentication.urls")),
    # Allauth
    path('account/', include('allauth.urls')),
    path('auth-logout/',TemplateView.as_view(template_name="account/logout-success.html"),name ='pages-logout'),
    path('auth-lockscreen/',TemplateView.as_view(template_name="account/lock-screen.html"),name ='pages-lockscreen'),
    #     #Custum change password done page redirect
    # path('accounts/password/change/', login_required(MyPasswordChangeView.as_view()), name="account_change_password"),
    # #Custum set password done page redirect
    # path('accounts/password/set/', login_required(MyPasswordSetView.as_view()), name="account_set_password"),
    #display
    path('', include("display.urls")),
    path('business/', include('corporate_portal.urls')),
    path('portal/', include("portal.urls")),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

