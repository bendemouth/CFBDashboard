import requests as req
from django.core.management.base import BaseCommand
from CFBDash.models import TeamStat, Team
from django.conf import  settings

class Command(BaseCommand):
    help = 'Fetches team stats'

    def handle(self, *args, **options):
        headers = {"Authorization": f"Bearer {settings.API_KEY}",
                   "accept": "application/json"}

        uri = "https://apinext.collegefootballdata.com/stats/season?year=2024"

        self.stdout.write("Fetching team stats")

        try:
            response = req.get(uri, headers=headers)
            response.raise_for_status()
        except req.RequestException as e:
            self.stdout.write(self.style.ERROR(f"Error fetching data: {e}"))
            return

        data = response.json()

        for stat in data:
            team_name = stat["team"].strip("\'")
            team = Team.objects.filter(school=team_name).first()

            if not team:
                self.stdout.write(self.style.ERROR(f"Team {team_name} not found"))
                continue

            obj, created = TeamStat.objects.get_or_create(
                team=team,
                stat=stat["statName"],
                defaults={
                    "conference": stat["conference"],
                    "stat_value": stat["statValue"]
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"Created stat for {team_name} - {stat['statName']}"))
            else:
                self.stdout.write(self.style.WARNING(f"Updated stat for {stat['team']} - {stat['statName']}"))

        self.stdout.write(self.style.SUCCESS("Successfully fetched team stats"))