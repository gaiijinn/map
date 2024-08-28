from abc import ABC, abstractmethod


class BaseAchievementGetter(ABC):
    @abstractmethod
    def get_achievement(self, *args, **kwargs):
        pass


class BaseUserGetter(ABC):
    @abstractmethod
    def get_user(self, *args, **kwargs):
        pass
