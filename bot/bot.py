import logging

from typing import Any, Dict, List

from bot.data import remove_ticker, get_tickers_from_selection, add_ticker, get_company_profile_from_selection
from bot import __version__, OperationalException
from bot.data.data_provider_manager import DataProviderManager

logger = logging.getLogger(__name__)


class Bot:

    def __init__(self, config: Dict[str, Any]) -> None:
        logger.info('Starting bot version %s', __version__)

        # Make variables private, only bot should change them
        self.__config = config
        self.__data_provider_manager = DataProviderManager(self.config)

        # Load tickers
        self.load_stock_selection_from_config()

    @property
    def config(self) -> Dict[str, Any]:
        return self.__config

    def set_config(self, config: Dict[str, Any]):
        self.__config = config

    def load_stock_selection_from_config(self):
        logger.info("Initializing provided stocks from config ...")
        tickers = self.__config.get('tickers', [])

        for ticker in tickers:

            try:
                self.add_stock_to_selection(ticker)
            except OperationalException as e:
                logger.error(str(e))
                continue

    def add_stock_to_selection(self, ticker: str) -> None:
        logger.info("Adding stock to selection ...")

        if not get_company_profile_from_selection(ticker, self.config):

            if self.__data_provider_manager.evaluate_ticker(ticker):

                profile = self.__data_provider_manager.get_profile(ticker)

                if not profile:
                    raise OperationalException("Could not evaluate {} with the data providers".format(ticker))

                company_name = profile.get('profile', {}).get('companyName', None)
                category = profile.get('profile', {}).get('industry', None)

                if not company_name:
                    raise OperationalException("Could not evaluate company name for stock {} with the data providers")

                if not company_name:
                    raise OperationalException("Could not evaluate category for stock {} with the data providers")

                try:
                    add_ticker(
                        ticker,
                        company_name=company_name,
                        category=category,
                        config=self.config
                    )
                except Exception:
                    raise OperationalException(
                        "Something went wrong with adding stock {} to the selection".format(ticker)
                    )
            else:
                raise OperationalException("Could not evaluate stock {} with the data providers".format(ticker))
        else:
            raise OperationalException(
                "Ticker {} is already present in registry".format(ticker)
            )

    def remove_stock_from_selection(self, ticker: str) -> None:
        logger.info("Removing stock from selection ...")

        if get_company_profile_from_selection(ticker, self.config):

            try:
                remove_ticker(ticker, self.config)
            except Exception:
                raise OperationalException("Something went wrong while deleting the stock from the selection")
        else:
            raise OperationalException("Provided stock {} does not exist in the selection".format(ticker))

    def get_stocks_selection(self) -> List[str]:
        logger.info("Get stocks from selection ...")
        tickers = get_tickers_from_selection(self.config)
        result = []

        for ticker in tickers:
            result.append(ticker[0])

        return result

    def remove_stocks_selection(self) -> None:
        logger.info("Removing stocks selection ...")
        tickers = self.get_stocks_selection()

        for ticker in tickers:
            try:
                self.remove_stock_from_selection(ticker)
            except OperationalException as e:
                logger.error(str(e))
                continue

        logger.info("Removed stock selection")





