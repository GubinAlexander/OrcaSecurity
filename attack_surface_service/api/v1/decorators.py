import time

from attack_surface_service.api.v1.services import statistic_calculation


def commit_statistics(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        executing_time = time.time() - start
        statistic_calculation(executing_time)
        return result
    return wrapper
