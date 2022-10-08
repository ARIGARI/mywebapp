from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from .models import Question, Choice
from .forms import QuestionForm


# Create your views here.

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:7]
    template = loader.get_template('polls/index.html')
    context = {
        'mensaje': 'Lista de preguntas',
        'ultimas_preguntas': latest_question_list,
    }
    return render(request, 'polls/index.html', context)

'''def hola_dos(request):
    return HttpResponse("hola2")'''

'''def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    #return render(request, 'polls/detail.html', {'question': question})
    #question = Question.objects.get(pk=question_id)
    #return HttpResponse("You're looking at question %s." % question_id)
    context = {
        'mensaje': "Detalle de la encuesta",
        'question': question
    }
    return render(request, 'polls/detail.html', context)
'''
'''def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)'''
'''def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
'''

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'mensaje': 'Detalle de la pregunta','question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

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

def add_or_change_question(request, question_id=None):
    question = None
    if question_id:
        question = get_object_or_404(Question, pk=question_id)
        if request.method == "POST":
            form = QuestionForm(
            data=request.POST,
            files=request.FILES,
            instance=question
            )
            if form.is_valid():
                question = form.save()
                #return redirect("polls:detail", pk=question.pk)
                return HttpResponseRedirect(reverse('polls:detail', args=(question.id,))) 
        else:
            form = QuestionForm(instance=question)
    context = {"question": question, "form": form}
    return render(request, "polls/polls_form.html", context)      