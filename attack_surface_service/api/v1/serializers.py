
from rest_framework import serializers


class VirtualMachineSerializer(serializers.Serializer):
    vm_id = serializers.CharField()
    name = serializers.CharField()
    tags = serializers.ListField()


class FirewallRuleSerializer(serializers.Serializer):
    fw_id = serializers.CharField()
    source_tag = serializers.CharField()
    dest_tag = serializers.CharField()


class CloudEnvironmentSerializer(serializers.Serializer):
    vms = VirtualMachineSerializer(many=True)
    fw_rules = FirewallRuleSerializer(many=True)


class StatisticResponseSerializer(serializers.Serializer):
    request_count = serializers.IntegerField()
    average_request_time = serializers.FloatField()
    vm_count = serializers.IntegerField()
