from django.shortcuts import render, get_object_or_404

# Create your views here.
from CFBDash.models import Team, TeamStat


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

def stat_plots(request):
    all_stats = TeamStat.objects.values_list('stat', flat=True).distinct()

    x_stat = request.GET.get('x_stat')
    y_stat = request.GET.get('y_stat')

    labels = []
    data = []
    map = {}

    if x_stat and y_stat:
        x_data = TeamStat.objects.filter(stat=x_stat)
        y_data = TeamStat.objects.filter(stat=y_stat)

        for entry in x_data:
            map[entry.team_id] = {
                'team': entry.team.school,
                'x': entry.stat_value,
                'y': None, # Leave none and append y data in next block
            }

        for entry in y_data:
            if entry.team_id in map:
                map[entry.team_id]['y'] = entry.stat_value

        for team_data in map.values():
            if team_data['y'] is not None:
                data.append({
                    'x': team_data['x'],
                    'y': team_data['y'],
                    'name': team_data['team']
                })

    return render(request, 'stat_plots.html', {
        'x_stat': x_stat,
        'y_stat': y_stat,
        'labels': labels,
        'data': data,
        'map': map,
        'all_stats': all_stats
    })
