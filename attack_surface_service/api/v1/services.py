
from typing import Union

from django.conf import settings
from rest_framework import status
from rest_framework.response import Response


def get_attacked_vm(vms: list, vm_id: str) -> bool:
    for vm in vms:
        if vm_id == vm['vm_id']:
            return vm


def get_rules_allow_destination_traffic(rules: list, vm: Union[dict, bool]) -> list:
    result = []
    for rule in rules:
        if rule['dest_tag'] in vm['tags']:
            result.append(rule)
    return result


def get_machines_can_potentially_attack(rules: list, vms: list, vm_id: str) -> Union[list, Response]:
    attacked_vm = get_attacked_vm(vms, vm_id)
    if not attacked_vm:
        return Response(data='There is no virtual machine with this id', status=status.HTTP_404_NOT_FOUND)

    result = []
    allow_destination_rules = get_rules_allow_destination_traffic(rules, attacked_vm)
    for rule in allow_destination_rules:
        for vm in vms:
            if rule['source_tag'] in vm['tags'] and vm['vm_id'] != vm_id and vm['vm_id'] not in result:
                result.append(vm['vm_id'])
    return result


def statistic_calculation(executing_time: float) -> None:
    settings.STATISTIC['request_count'] += 1
    average_request_time = settings.STATISTIC['average_request_time']
    settings.STATISTIC['average_request_time'] = (average_request_time + executing_time) / settings.STATISTIC['request_count']
