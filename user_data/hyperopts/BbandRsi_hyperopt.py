# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement

import talib.abstract as ta
from pandas import DataFrame
from typing import Dict, Any, Callable, List

# import numpy as np
from skopt.space import Categorical, Dimension, Integer, Real

# import freqtrade.vendor.qtpylib.indicators as qtpylib
from freqtrade.optimize.hyperopt_interface import IHyperOpt
import freqtrade.vendor.qtpylib.indicators as qtpylib

class_name = 'BbandRsi_hyperopt'


# This class is a sample. Feel free to customize it.
class BbandRsi_hyperopt(IHyperOpt):
    """
    This is an Example hyperopt to inspire you. - corresponding to MACDStrategy in this repository.
    To run this, best use the following command (adjust to your environment if needed):
    ```
    freqtrade hyperopt --strategy MACDStrategy --hyperopt MACDStrategy_hyperopt --spaces buy sell
    ```
    The idea is to optimize only the CCI value.
    - Buy side: CCI between -700 and 0
    - Sell side: CCI between 0 and 700
    More information in https://github.com/freqtrade/freqtrade/blob/develop/docs/hyperopt.md
     """

    @staticmethod
    def populate_indicators(dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)

        # Bollinger bands
        bollinger = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=2)
        dataframe['bb_lowerband'] = bollinger['lower']
        dataframe['bb_middleband'] = bollinger['mid']
        dataframe['bb_upperband'] = bollinger['upper']

        return dataframe

    @staticmethod
    def buy_strategy_generator(params: Dict[str, Any]) -> Callable:
        """
        Define the buy strategy parameters to be used by hyperopt
        """

        def populate_buy_trend(dataframe: DataFrame, metadata: dict) -> DataFrame:
            """
            Buy strategy Hyperopt will build and use
            """
            dataframe.loc[
                (
                        (dataframe['rsi'] < 30) &
                        (dataframe['close'] < dataframe['bb_lowerband']) &
                        (dataframe['volume'] > 0)  # Make sure Volume is not 0
                ),
                'buy'] = 1
            return dataframe

        return populate_buy_trend

    @staticmethod
    def indicator_space() -> List[Dimension]:
        """
        Define your Hyperopt space for searching strategy parameters
        """
        return [
            Integer(-30, 100, name='rsi'),
        ]

    @staticmethod
    def sell_strategy_generator(params: Dict[str, Any]) -> Callable:
        """
        Define the sell strategy parameters to be used by hyperopt
        """

        def populate_sell_trend(dataframe: DataFrame, metadata: dict) -> DataFrame:
            """
            Sell strategy Hyperopt will build and use
            """
            dataframe.loc[
                (
                    (dataframe['rsi'] > 70)

                ),
                'sell'] = 1
            return dataframe

        return populate_sell_trend

    @staticmethod
    def sell_indicator_space() -> List[Dimension]:
        """
        Define your Hyperopt space for searching sell strategy parameters
        """
        return [
            Integer(0, 700, name='rsi'),
        ]

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                    (dataframe['rsi'] < 30) &
                    (dataframe['close'] < dataframe['bb_lowerband'])

            ),
            'buy'] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                    (dataframe['rsi'] > 70)

            ),
            'sell'] = 1
        return dataframe
