from abc import ABC, abstractmethod


class BaseModelManager(ABC):

    @abstractmethod
    def pre_process(self):
        pass

    @abstractmethod
    def post_process(self):
        pass

    @abstractmethod
    def text_to_voice(self, text: str):
        pass
