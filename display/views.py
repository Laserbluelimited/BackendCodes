from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView

# Create your views here.
class HomePageView(View):
    def get(self, request):
        return render(request, 'display/index.html')
