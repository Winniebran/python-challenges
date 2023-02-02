from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from teams.models import Team
from django.forms.models import model_to_dict
from .utils import (
    data_processing,
    InvalidYearCupError,
    NegativeTitlesError,
    ImpossibleTitlesError,
)


class TeamView(APIView):
    def post(self, request):
        try:
            data_processing(request.data)
            team = Team.objects.create(**request.data)

            return Response(model_to_dict(team), 201)

        except NegativeTitlesError as error:
            return Response(error.message, 400)
        except InvalidYearCupError as error:
            return Response(error.message, 400)
        except ImpossibleTitlesError as error:
            return Response(error.message, 400)

    def get(self, request):
        teams = Team.objects.all()
        teams_dict = [model_to_dict(team) for team in teams]

        return Response(teams_dict)


class TeamView2(APIView):
    def get(self, request, team_id: int):
        try:
            team = Team.objects.get(pk=team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, 404)

        return Response(model_to_dict(team))

    def patch(self, request, team_id: int):
        try:
            team = Team.objects.get(pk=team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, 404)

        team.__dict__.update(request.data)
        team.save()
        return Response(model_to_dict(team), 200)

    def delete(self, request, team_id: int):
        try:
            Team.objects.get(pk=team_id).delete()
            return Response(status=204)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, 404)
