
from attack_surface_service.api.v1.decorators import commit_statistics
from attack_surface_service.api.v1.serializers import (
    CloudEnvironmentSerializer, StatisticResponseSerializer)
from attack_surface_service.api.v1.services import get_machines_can_potentially_attack
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class AttackAPIView(APIView):

    @commit_statistics
    def post(self, request):
        query_serializer = CloudEnvironmentSerializer(data=request.data)
        query_serializer.is_valid(raise_exception=True)

        machines = get_machines_can_potentially_attack(request.data['fw_rules'], request.data['vms'], request.GET['vm_id'])
        if isinstance(machines, Response):
            return machines
        return Response(data=machines, status=status.HTTP_200_OK)


class StatsAPIView(APIView):

    @commit_statistics
    def post(self, request):
        query_serializer = CloudEnvironmentSerializer(data=request.data)
        query_serializer.is_valid(raise_exception=True)
        settings.STATISTIC['vm_count'] = len(request.data['vms'])
        resp_serializer = StatisticResponseSerializer(settings.STATISTIC)
        return Response(data=resp_serializer.data, status=status.HTTP_200_OK)
