from abc import ABC, abstractmethod


class BaseProgressUpdater(ABC):
    @abstractmethod
    def get_new_progress(self):
        pass


class BaseIsAchievedUpdater(ABC):
    @abstractmethod
    def get_is_achieved(self):
        pass
