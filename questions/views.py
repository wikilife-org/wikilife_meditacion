# encoding: utf-8
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.db.models import Avg, Max, Min, Count
from django.db import connection, transaction
from collections import defaultdict

from questions.models import *

def deepDefaultDict():
    return defaultdict(deepDefaultDict)
    
def index(request):
    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    return render_to_response('questions/index.html', {'latest_poll_list': latest_poll_list}, )

def start(request):
    person = Person()
    person.save()
    return HttpResponseRedirect(reverse('questions.views.detail', args=(person.id, 0,)))

def detail(request, person_id, seq):
    p = get_object_or_404(Poll, sequence=seq)
    choices = p.choice_set.all().order_by('sequence')
    return render_to_response('questions/detail.html', {'person_id':person_id, 'poll': p, 'choices':choices}, context_instance=RequestContext(request))

def thanks(request, person_id):
    answers = Response.objects.all().filter(person=person_id)
    person = get_object_or_404(Person, pk=person_id)
    for a in answers:
        a.stat = answer_stats(a)

    return render_to_response('questions/thanks.html', {'answers':answers, "person":person}, context_instance=RequestContext(request))

def legal(request):
     return render_to_response('questions/legal.html')
 
def answer_stats(answer):
    stat = Response.objects.filter(poll=answer.poll).values('choice').annotate(total=Count('id'))
    total = 0 
    for s in stat:
        total += s['total']
    stat_percent = {}
    for s in stat:
        t = float(s['total']) / total * 100
        c = Choice.objects.get(pk=s['choice'])
        if answer.choice == c:
            return t
    return 0

def sortByChoice(choices):
    print "hola"
    decoradas = [( x[0] == None and "1" or x[0].choice.lower()[0], x) for x in choices]
    decoradas.sort()
    return decoradas

def sortByPercent(choices):
    print "hola3"
    decoradas = [( x[1], x) for x in choices]
    decoradas.sort()
    return decoradas

def result(request, response_id):
    answer = get_object_or_404(Response, pk=response_id)

    stat = Response.objects.filter(poll=answer.poll).values('choice').annotate(total=Count('id')).order_by('choice')
    total = 0 
    for s in stat:
        total += s['total']
        
    stat_percent = []
    for s in stat:
        t = float(s['total']) / total * 100
        c = Choice.objects.get(pk=s['choice'])
        stat_percent.append((c,t)) 
    
    user_choice = None
    for r in stat_percent:
        if r[0].pk ==  answer.choice.pk:
            user_choice = r
            
    result = []
    if len(stat_percent) > 4:
        stat_percent1 = sortByPercent(stat_percent)
        stat_percent1 = stat_percent1[:4]
        stat_percent1.reverse()
        
        is_there = False
        for s in stat_percent1:
            if s[1][0].pk ==  answer.choice.pk:
                is_there = True
                break
            
        if  not is_there:
            stat_percent1[3] = (0,user_choice)
            
        for s in stat_percent1:
             result.append(s[1])
    else:
        result = stat_percent

    stat_percent1 = sortByChoice(result)
    
    
    polls_count = Poll.objects.count()
    if answer.poll.sequence == (polls_count - 1):
        is_last = True
    else:
        is_last = False
    return render_to_response('questions/result.html', {'stat':stat_percent1, 'answer':answer, 'is_last':is_last}, context_instance=RequestContext(request))

def vote(request):
    p = get_object_or_404(Poll, pk=request.POST['poll_id'])
    person = get_object_or_404(Person, pk=request.POST['person_id'])
    try:
        selected_choice = p.choice_set.get(pk=request.POST['selected_choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
        return render_to_response('polls/detail.html', {
            'poll': p,
            'person_id':person.id,
            'error_message': "You didn't select a choice.",
        }, context_instance=RequestContext(request))
    else:
        answer = Response(person=person, poll=p, choice=selected_choice)
        answer.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
            #return HttpResponseRedirect(reverse('questions.views.detail', args=(person.id, p.sequence+1,)))
        return HttpResponseRedirect(reverse('questions.views.result', args=(answer.id,)))

def email(request):
    email = request.POST['email']
    person = get_object_or_404(Person, pk=request.POST['person_id'])
    
    contact = Contact(email=email, person=person)
    contact.save()
    return HttpResponseRedirect(reverse('questions.views.index'))
    
def charts(request):
    chart_list = Chart.objects.all().order_by('title')
    return render_to_response('questions/charts.html', {'charts': chart_list}, )

def chart(request, chart_id):
    chart = get_object_or_404(Chart, pk=chart_id)
    
    poll1 = chart.poll1
    poll2 = chart.poll2
    
    #res = deepDefaultDict()
    res = {}
    """"
    for x in poll1.choice_set.all():
        res[x] = {}
        for y in poll2.choice_set.all():
            res[x][y] = 0
    """    
    for x in poll2.choice_set.all():
        res[x] = {}
        for y in poll1.choice_set.all():
            res[x][y] = 0

    cursor = connection.cursor()
    cursor.execute("select rp2.choice_id, rp1.choice_id, count(rp1.person_id) from questions_response as rp1 left join questions_response as rp2 on rp1.person_id=rp2.person_id where rp1.poll_id=%s and rp2.poll_id=%s  group  by 1,2 order by 1,2", [poll1.id, poll2.id,])
    query_result = cursor.fetchall()
    respondents = 0
    for row in query_result:
        c2 = Choice.objects.get(pk=row[0])
        c1 = Choice.objects.get(pk=row[1])
        res[c2][c1] = row[2]
        respondents += row[2]

    for i in res.keys():
        for j in res[i]:
            res[i][j] = float(res[i][j]) / respondents * 100
        
    if not chart.pie_chart:
        return render_to_response('questions/chart.html', {'chart':chart, 'stat':res, 'respondents':respondents}, context_instance=RequestContext(request))
    else:
        return render_to_response('questions/pie_chart.html', {'chart':chart, 'stat':res, 'respondents':respondents}, context_instance=RequestContext(request))

        
    
