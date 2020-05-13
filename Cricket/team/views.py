from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import *
from .forms import *
from collections import Counter

# Create your views here.


def teams(request):
    teams = Team.objects.all()
    context = {'teams': teams}
    return render(request, 'team/team.html', context)


def players(request, id=None):
    context = {}
    context['team'] = get_object_or_404(Team, id=id)
    return render(request, 'team/players.html', context)


def playerHistory_details(request, id=None):
    try:
        player = get_object_or_404(Player, id=id)
        playerHistory = PlayerHistory.objects.get(player__pk=player.id)
    except:
        return HttpResponse('<h1>Player Stats not updated. Please Update the stats.</h1>')

    context = {}
    context['player'] = player
    context['playerHistory'] = playerHistory
    return render(request, 'team/playerhistory_details.html', context)


def playerHistory_edit(request, id=None):
    player = get_object_or_404(Player, id=id)
    playerHistory = PlayerHistory.objects.get(player__pk=player.id)
    if request.method == 'POST':
        playerhistory_form = PlayerHistoryForm(
            request.POST, instance=playerHistory)
        if playerhistory_form.is_valid():
            playerhistory_form.save()
            return HttpResponseRedirect(reverse('teams'))
        else:
            return render(request, 'team/playerhistory_edit.html', {"playerhistory_form": playerhistory_form})
    else:
        playerhistory_form = PlayerHistoryForm(instance=playerHistory)
        return render(request, 'team/playerhistory_edit.html', {"playerhistory_form": playerhistory_form})


def matchesList(request):
    matches = Matches.objects.all()
    context = {'matches': matches}
    return render(request, 'team/matches.html', context)


def matchesAdd(request):
    context = {}
    if request.method == 'POST':
        match_form = MatchForm(request.POST)
        context['match_form'] = match_form
        if match_form.is_valid():
            u = match_form.save()
            return HttpResponseRedirect(reverse('matches_list'))
        else:
            return render(request, 'team/matches_add.html', context)
    else:
        match_form = MatchForm()
        context['match_form'] = match_form
        return render(request, 'employee/matches_add.html', context)

# ------------------------------------------


def pointsView(request):
    points = PointsTable.objects.values_list()
    l = [i[1] for i in points]
    points = Counter(l)
    context = {'points': sorted(
        points.items(), key=lambda x: x[1], reverse=True)}

    return render(request, 'team/points.html', context)
