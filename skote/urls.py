
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

    #display
    path('', include("display.urls")),
    # path('clinic', include("clinic_mgt.urls")),
    path('portal/', include("portal.urls")),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

