
from attack_surface_service.api.v1.decorators import commit_statistics
from attack_surface_service.api.v1.serializers import (
    CloudEnvironmentSerializer, StatisticResponseSerializer, VirtualMachineResponseSerializer)
from attack_surface_service.api.v1.services import (
    get_attacked_vm, get_machines_can_potentially_attack, get_rules_allow_destination_traffic)
from attack_surface_service.models import Statistic
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class AttackAPIView(APIView):

    @commit_statistics
    def post(self, request):
        query_serializer = CloudEnvironmentSerializer(data=request.data)
        query_serializer.is_valid(raise_exception=True)
        attacked_vm = get_attacked_vm(request.data['vms'], request.GET['vm_id'])
        if not attacked_vm:
            return Response(data='There is no virtual machine with this id', status=status.HTTP_404_NOT_FOUND)

        allow_destination_rules = get_rules_allow_destination_traffic(request.data['fw_rules'], attacked_vm)
        machines = get_machines_can_potentially_attack(allow_destination_rules, request.data['vms'], request.GET['vm_id'])
        resp_serializer = VirtualMachineResponseSerializer(machines, many=True)
        return Response(data=resp_serializer.data, status=status.HTTP_200_OK)


class StatsAPIView(APIView):

    @commit_statistics
    def post(self, request):
        query_serializer = CloudEnvironmentSerializer(data=request.data)
        query_serializer.is_valid(raise_exception=True)
        data = Statistic.objects.values('request_count', 'average_request_time').last()
        data['vm_count'] =  len(request.data['vms'])
        resp_serializer = StatisticResponseSerializer(data)
        return Response(data=resp_serializer.data, status=status.HTTP_200_OK)
