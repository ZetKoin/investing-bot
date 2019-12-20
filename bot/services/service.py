from abc import ABC, abstractmethod
from typing import Any, Dict, List

from bot.bot import Bot


class ServiceException(Exception):
    """
    Should be raised with a service-formatted message in an _service_* method
    if the required state is wrong, i.e.:
    raise ServiceException('*Status:* `no active trade`')
    """
    def __init__(self, message: str) -> None:
        super().__init__(self)
        self.message = message

    def __str__(self):
        return self.message

    def __json__(self):
        return {
            'msg': self.message
        }


class Service(ABC):
    """
    Service class can be used to have extra features, like bot actions and data, and access to DB data
    """

    def __init__(self, bot: Bot):
        self._bot = bot

    def __trade_status(self) -> List[Dict[str, Any]]:
        pass

    @property
    def name(self) -> str:
        """ Returns the lowercase name of the implementation """
        return self.__class__.__name__.lower()

    @property
    def bot(self) -> Bot:
        return self._bot

    @abstractmethod
    def startup(self) -> None:
        pass

    @abstractmethod
    def cleanup(self) -> None:
        """ Cleanup pending module resources """
        pass

    def _service_add_stock_to_selection(self, ticker: str) -> None:
        self._bot.add_stock_to_selection(ticker)

    def _service_remove_stock_from_selection(self, ticker: str) -> None:
        self._bot.remove_stock_from_selection(ticker)

    def _service_remove_stock_selection(self) -> None:
        self._bot.remove_stocks_selection()

    def _service_get_stocks_selection(self) -> List[str]:
        return self._bot.get_stocks_selection()

    def _service_reload_stocks_selection_config(self) -> None:
        self._bot.load_stock_selection_from_config()

