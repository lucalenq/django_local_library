from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice, Question, Chart

from django.utils import timezone

from django.conf import settings
import os

class HomeView(generic.TemplateView):
    template_name = 'polls/index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['message'] = Chart.objects.all() 
        # context['chart'] = Chart.plot()
        # context['describe_df']= Chart.describeData('C:\\Users\\Alenquer\\it\\django\\apps\\data_science_idealista\\polls\\datasets\\df_idealista_bcn_pg_1_to_50.csv')
        #context['facets']= Chart.displayFacets('C:\\Users\\Alenquer\\it\\django\\apps\\data_science_idealista\\polls\\datasets\\df_idealista_bcn_pg_1_to_50.csv')
        #context['facets']= Chart.displayFacets(os.path.join(settings.DATASET_DIRS, 'df_idealista_bcn_pg_1_to_50.csv'))
        # context['facets']= Chart.displayFacets(os.path.join(settings.DATASET_DIRS[0] + 
        #                                                     '\df_idealista_bcn_pg_1_to_50.csv'
        #                                                     )
        #                                         )
        # context['facets']= Chart.displayFacets(os.path.join(settings.DATASET_DIRS[0] + 
        #                                                     'df_idealista_bcn_pg_1_to_50.csv'
        #                                                     ) 
        #                                         )
        # context['facets']= Chart.displayFacets(os.path.join(settings.DATASET_DIRS[0] + 
        #                                                     '\df_idealista_bcn_pg_1_to_50.csv'
        #                                                     ) 
        #                                         )
        context['facets']= Chart.displayFacets(os.path.join(settings.STATICFILES_DIRS[0] + 
                                                            '/df_idealista_bcn_pg_1_to_50.csv'
                                                            ) 
                                                )
        

        context['my_dataset_dir'] = os.path.join(settings.STATICFILES_DIRS[0], 
                                                            'df_idealista_bcn_pg_1_to_50.csv'
                                                            ) 
        
        # os.path.join(SITE_ROOT, '..', 'static')

        return context

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())
        

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))