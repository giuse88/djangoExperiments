from django.shortcuts import render
from django.views.generic import View, TemplateView, FormView
from forms import NameForm
from models import UserName
from django.http  import HttpResponse

class IndexView(TemplateView):
    template_name = "tabs/index.html"

class Tab1View(TemplateView):
    template_name = "tabs/tab1.html"

class Tab2View(TemplateView):
    template_name = "tabs/tab2.html"

class ThanksView(View):
    def get(self, request, *args, **kwargs):
      return HttpResponse('Thanks')

class NameView(FormView):
    template_name = "tabs/names.html"
    form_class = NameForm
    success_url = "/names/"

    def get_context_data(self, **kwargs):
      context = super(NameView, self).get_context_data(**kwargs)
      context['names'] = UserName.objects.all()
      return context

    def form_valid(self, form): 
      obj = form.save()
      return super(NameView, self).form_valid(form)

