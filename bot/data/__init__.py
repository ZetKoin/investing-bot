import logging
import sqlite3
from typing import Dict, Any, List, Tuple

from bot import setup

logger = logging.getLogger(__name__)

SELECTION_STOCKS_TABLE_NAME = 'SELECTION'
TRADES_TABLE_NAME = 'TRADES'


def create_connection(config: Dict[str, Any]):
    return sqlite3.connect(setup.get_database_file(config))


def create_tables(config: Dict[str, Any]) -> None:
    table_names = get_all_table_names(config)

    if SELECTION_STOCKS_TABLE_NAME not in table_names:
        logger.info("Creating database table {} ...".format(SELECTION_STOCKS_TABLE_NAME))
        con = create_connection(config)

        # Create ticker tables
        con.execute('''
            CREATE TABLE SELECTION
            ([ticker_id] INTEGER PRIMARY KEY, [ticker] text, [company_name] text, [category] text)
        ''')

        con.commit()
        con.close()

    if TRADES_TABLE_NAME not in table_names:
        logger.info("Creating database table {} ...".format(TRADES_TABLE_NAME))
        con = create_connection(config)

        # Create open trades table
        con.execute('''
            CREATE TABLE TRADES
            ([trade_id] INTEGER PRIMARY KEY, [ticker_id] integer, [buy_date] timestamp)
        ''')

        con.commit()
        con.close()


def add_ticker(ticker: str, company_name: str, category: str, config: Dict[str, Any]) -> None:

    logger.info("Adding ticker {} to registry...".format(ticker))

    con = create_connection(config)
    cursor = con.cursor()

    # Add ticker if not exists
    insert_statement = """
           INSERT INTO TICKERS (ticker, company_name, category)
           VALUES (?, ?, ?);
       """

    data_tuple = (ticker, company_name, category)
    cursor.execute(insert_statement, data_tuple)

    con.commit()
    con.close()


def remove_ticker(ticker: str, config: Dict[str, Any]) -> None:

    logger.info("Removing ticker {} from registry ...".format(ticker))
    con = create_connection(config)
    cursor = con.cursor()

    delete_statement = '''
        DELETE from TICKERS where ticker = ? 
    '''

    cursor.execute(delete_statement, (ticker,))
    con.commit()
    con.close()


def get_company_profile_from_selection(ticker: str, config: Dict[str, any]) -> Tuple[str]:
    con = create_connection(config)
    cursor = con.cursor()

    logger.info("Getting {} company info from registry ...".format(ticker))

    cursor.execute(" SELECT * FROM TICKERS WHERE ticker=?", (ticker, ))
    result = cursor.fetchall()

    con.close()
    return result


def get_tickers_from_selection(config: Dict[str, any]) -> List[str]:
    con = create_connection(config)
    cursor = con.cursor()

    logger.info("Getting all tickers from registry ...")

    # Get ticker if exists
    select_statement = '''
       SELECT (ticker) from TICKERS
    '''

    cursor.execute(select_statement)
    result = cursor.fetchall()
    con.close()
    return result


def get_all_table_names(config: Dict[str, Any]) -> List[str]:
    table_names = []
    con = create_connection(config)
    cursor = con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    for table_name in tables:
        table_names += table_name

    return table_names


