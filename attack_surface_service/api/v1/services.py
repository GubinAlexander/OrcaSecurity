
from typing import Union

from attack_surface_service.models import Statistic


def get_attacked_vm(vms: list, vm_id: str) -> bool:
    for vm in vms:
        if vm_id == vm['vm_id']:
            return vm


def get_rules_allow_destination_traffic(rules: dict, vm: Union[dict, bool]) -> list:
    result = []
    for rule in rules:
        if rule['dest_tag'] in vm['tags']:
            result.append(rule)
    return result


def get_machines_can_potentially_attack(rules: list, vms: list, vm_id: str) -> list:
    result = []
    for rule in rules:
        for vm in vms:
            if rule['source_tag'] in vm['tags'] and vm['vm_id'] != vm_id:
                result.append(vm)
    return result


def statistic_calculation(executing_time: float) -> None:
    statistic = Statistic.objects.all().last()
    statistic.request_count += 1
    statistic.average_request_time = (statistic.average_request_time + executing_time) / statistic.request_count
    statistic.save()


def reset_statistic():
    from attack_surface_service.models import Statistic

    Statistic.objects.all().delete()
    statistic = Statistic.objects.create(request_count=0, average_request_time=0)
    statistic.save()
