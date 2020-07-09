
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

# from .models import Choice, Question, Chart

from django.utils import timezone

from django.conf import settings
import os

class IndexView(generic.ListView):
    template_name = 'home/home.html'
    context_object_name = 'latest_question_list'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
       
        
    #     context['title']= 'Real Estate Analysis'

    #     return context
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return 'Real Estate Analysis'
        # return Question.objects.filter(
        #     pub_date__lte=timezone.now()
        # ).order_by('-pub_date')[:5]