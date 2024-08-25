from abc import ABC, abstractmethod


class BaseLevelFinder(ABC):
    @abstractmethod
    def get_level(self, total_exp: int):
        pass

    @abstractmethod
    def get_last_level(self):
        pass


class BaseExperienceCalculator(ABC):
    @abstractmethod
    def get_total_exp(self, user: object):
        pass
