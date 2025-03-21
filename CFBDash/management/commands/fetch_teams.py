import requests as req
from django.core.management.base import BaseCommand
from CFBDash.models import Team
from django.conf import  settings


class Command(BaseCommand):
    help = "Fetch teams from API and store them in the database"

    def handle(self, *args, **options):
        headers = {"Authorization": f"Bearer {settings.API_KEY}",
                   "accept": "application/json"}

        teams_api = "https://apinext.collegefootballdata.com/teams/fbs?year=2024"

        self.stdout.write("Fetching teams from API...")

        try:
            response = req.get(teams_api, headers=headers)
            response.raise_for_status()
        except req.RequestException as e:
            self.stderr.write(self.style.ERROR(f"Error fetching data: {e}"))
            return

        data = response.json()

        for team in data:
            obj, created = Team.objects.update_or_create(
                api_id=team["id"],
                defaults={
                    "school": team["school"],
                    "abbr": team["abbreviation"],
                    "conference": team.get("conference", ""),  # Prevents KeyError
                    "division": team.get("division", ""),
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"Added: {team['school']}"))
            else:
                self.stdout.write(self.style.WARNING(f"Updated: {team['school']}"))

        self.stdout.write(self.style.SUCCESS("Teams successfully inserted/updated!"))