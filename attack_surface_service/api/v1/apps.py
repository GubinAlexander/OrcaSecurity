
from django.apps import AppConfig


class AttackServiceConfig(AppConfig):
    name = 'attack_surface_service'

    def ready(self):
        from attack_surface_service.api.v1.services import reset_statistic

        reset_statistic()
