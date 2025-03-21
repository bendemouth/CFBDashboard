from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
import requests as req

from CFBDash.models import Team


def index(request):
    pass

def team_details(request, team_slug):
    team = get_object_or_404(Team, slug=team_slug)
    stats = team.stats.all()
    all_teams = Team.objects.all()

    return render(request, 'team_details.html', {
        'team': team,
        'stats': stats,
        'all_teams': all_teams
    })
