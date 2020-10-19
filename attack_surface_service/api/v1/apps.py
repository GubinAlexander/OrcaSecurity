
from django.apps import AppConfig
from django.db import connection


class AttackServiceConfig(AppConfig):
    name = 'attack_surface_service'

    def ready(self):
        from attack_surface_service.api.v1.services import reset_statistic

        all_tables = connection.introspection.table_names()
        if 'attack_surface_service_statistic' in all_tables:
            reset_statistic()
