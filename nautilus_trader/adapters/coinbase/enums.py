# -------------------------------------------------------------------------------------------------
#  Copyright (C) 2015-2023 Nautech Systems Pty Ltd. All rights reserved.
#  https://nautechsystems.io
#
#  Licensed under the GNU Lesser General Public License Version 3.0 (the "License");
#  You may not use this file except in compliance with the License.
#  You may obtain a copy of the License at https://www.gnu.org/licenses/lgpl-3.0.en.html
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# -------------------------------------------------------------------------------------------------

from enum import Enum
from enum import unique

from nautilus_trader.model.data.bar import BarSpecification
from nautilus_trader.model.enums import BarAggregation
from nautilus_trader.model.enums import OrderSide
from nautilus_trader.model.enums import OrderStatus
from nautilus_trader.model.enums import OrderType
from nautilus_trader.model.enums import PriceType
from nautilus_trader.model.enums import TimeInForce
from nautilus_trader.model.enums import TriggerType
from nautilus_trader.model.enums import bar_aggregation_to_str
from nautilus_trader.model.orders import Order


"""
Defines `Coinbase` common enums.


References
----------
https://docs.cloud.coinbase.com/advanced-trade-api/reference
"""


@unique
class CoinbaseRateLimitType(Enum):
    """Represents a `Coinbase` rate limit type."""

    REQUEST_WEIGHT = "REQUEST_WEIGHT"
    ORDERS = "ORDERS"
    RAW_REQUESTS = "RAW_REQUESTS"


@unique
class CoinbaseRateLimitInterval(Enum):
    """Represents a `Coinbase` rate limit interval."""

    SECOND = "SECOND"
    MINUTE = "MINUTE"
    DAY = "DAY"


@unique
class CoinbaseKlineInterval(Enum):
    """Represents a `Coinbase` kline chart interval."""

    
    MINUTE_1 = "1m"
    MINUTE_5 = "5m"
    MINUTE_15 = "15m"
    MINUTE_30 = "30m"
    HOUR_1 = "1h"
    HOUR_2 = "2h"
    HOUR_6 = "6h"
    DAY_1 = "1d"


@unique
class CoinbaseExchangeFilterType(Enum):
    """Represents a `Coinbase` exchange filter type."""

    EXCHANGE_MAX_NUM_ORDERS = "EXCHANGE_MAX_NUM_ORDERS"
    EXCHANGE_MAX_NUM_ALGO_ORDERS = "EXCHANGE_MAX_NUM_ALGO_ORDERS"


@unique
class CoinbaseSymbolFilterType(Enum):
    """Represents a `Coinbase` symbol filter type."""

    PRICE_FILTER = "PRICE_FILTER"
    PERCENT_PRICE = "PERCENT_PRICE"
    PERCENT_PRICE_BY_SIDE = "PERCENT_PRICE_BY_SIDE"
    LOT_SIZE = "LOT_SIZE"
    MIN_NOTIONAL = "MIN_NOTIONAL"
    NOTIONAL = "NOTIONAL"
    ICEBERG_PARTS = "ICEBERG_PARTS"
    MARKET_LOT_SIZE = "MARKET_LOT_SIZE"
    MAX_NUM_ORDERS = "MAX_NUM_ORDERS"
    MAX_NUM_ALGO_ORDERS = "MAX_NUM_ALGO_ORDERS"
    MAX_NUM_ICEBERG_ORDERS = "MAX_NUM_ICEBERG_ORDERS"
    MAX_POSITION = "MAX_POSITION"
    TRAILING_DELTA = "TRAILING_DELTA"


#@unique
#class CoinbaseAccountType(Enum):
#    """Represents a `Coinbase` account type."""
#
#    SPOT = "SPOT"
#    MARGIN_CROSS = "MARGIN_CROSS"
#    MARGIN_ISOLATED = "MARGIN_ISOLATED"
#    FUTURES_USDT = "FUTURES_USDT"
#    FUTURES_COIN = "FUTURES_COIN"
#
#    @property
#    def is_spot(self):
#        return self == CoinbaseAccountType.SPOT
#
#    @property
#    def is_margin(self):
#        return self in (
#            CoinbaseAccountType.MARGIN_CROSS,
#            CoinbaseAccountType.MARGIN_ISOLATED,
#        )
#
#    @property
#    def is_spot_or_margin(self):
#        return self in (
#            CoinbaseAccountType.SPOT,
#            CoinbaseAccountType.MARGIN_CROSS,
#            CoinbaseAccountType.MARGIN_ISOLATED,
#        )
#
#    @property
#    def is_futures(self) -> bool:
#        return self in (
#            CoinbaseAccountType.FUTURES_USDT,
#            CoinbaseAccountType.FUTURES_COIN,
#        )


@unique
class CoinbaseOrderSide(Enum):
    """Represents a `Coinbase` order side."""

    BUY = "BUY"
    SELL = "SELL"


@unique
class CoinbaseExecutionType(Enum):
    """Represents a `Coinbase` execution type."""

    NEW = "NEW"
    CANCELED = "CANCELED"
    CALCULATED = "CALCULATED"  # Liquidation Execution
    REJECTED = "REJECTED"
    TRADE = "TRADE"
    EXPIRED = "EXPIRED"


@unique
class CoinbaseOrderStatus(Enum):
    """Represents a `Coinbase` order status."""

    NEW = "NEW"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    CANCELED = "CANCELED"
    PENDING_CANCEL = "PENDING_CANCEL"
    REJECTED = "REJECTED"
    # EXPIRED = "EXPIRED"


@unique
class CoinbaseTimeInForce(Enum):
    """Represents a `Coinbase` order time in force."""

    GTC = "GTC"
    IOC = "IOC"
    FOK = "FOK"
    GTX = "GTX"  # FUTURES only, Good Till Crossing (Post Only)
    GTE_GTC = "GTE_GTC"  # Undocumented


@unique
class CoinbaseOrderType(Enum):
    """Represents a `Coinbase` order type."""

    LIMIT = "LIMIT"
    MARKET = "MARKET"
    STOP = "STOP"
    STOP_LIMIT = "STOP_LIMIT"
    UNKNOWN_ORDER_TYPE = "UNKNOWN_ORDER_TYPE" 
    # STOP_LOSS = "STOP_LOSS"  # SPOT/MARGIN only
    # STOP_LOSS_LIMIT = "STOP_LOSS_LIMIT"  # SPOT/MARGIN only
    # TAKE_PROFIT = "TAKE_PROFIT"
    # TAKE_PROFIT_LIMIT = "TAKE_PROFIT_LIMIT"  # SPOT/MARGIN only
    # LIMIT_MAKER = "LIMIT_MAKER"  # SPOT/MARGIN only
    # STOP_MARKET = "STOP_MARKET"  # FUTURES only
    # TAKE_PROFIT_MARKET = "TAKE_PROFIT_MARKET"  # FUTURES only
    # TRAILING_STOP_MARKET = "TRAILING_STOP_MARKET"  # FUTURES only


@unique
class CoinbaseSecurityType(Enum):
    """Represents a `Coinbase` endpoint security type."""

    NONE = "NONE"
    TRADE = "TRADE"
    MARGIN = "MARGIN"  # SPOT/MARGIN only
    USER_DATA = "USER_DATA"
    USER_STREAM = "USER_STREAM"
    MARKET_DATA = "MARKET_DATA"


@unique
class CoinbaseMethodType(Enum):
    """Represents a `Coinbase` endpoint method type."""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


@unique
class CoinbaseNewOrderRespType(Enum):
    """
    Represents a `Coinbase` newOrderRespType.
    """

    ACK = "ACK"
    RESULT = "RESULT"
    FULL = "FULL"


class CoinbaseEnumParser:
    """
    Provides common parsing methods for enums used by the 'Coinbase' exchange.

    Warnings
    --------
    This class should not be used directly, but through a concrete subclass.
    """

    def __init__(self) -> None:
        # Construct dictionary hashmaps
        self.ext_to_int_status = {
            CoinbaseOrderStatus.NEW: OrderStatus.ACCEPTED,
            CoinbaseOrderStatus.CANCELED: OrderStatus.CANCELED,
            CoinbaseOrderStatus.PARTIALLY_FILLED: OrderStatus.PARTIALLY_FILLED,
            CoinbaseOrderStatus.FILLED: OrderStatus.FILLED,
            CoinbaseOrderStatus.NEW_ADL: OrderStatus.FILLED,
            CoinbaseOrderStatus.NEW_INSURANCE: OrderStatus.FILLED,
            CoinbaseOrderStatus.EXPIRED: OrderStatus.EXPIRED,
        }

        self.ext_to_int_order_side = {
            CoinbaseOrderSide.BUY: OrderSide.BUY,
            CoinbaseOrderSide.SELL: OrderSide.SELL,
        }
        self.int_to_ext_order_side = {b: a for a, b in self.ext_to_int_order_side.items()}

        self.ext_to_int_bar_agg = {
            "s": BarAggregation.SECOND,
            "m": BarAggregation.MINUTE,
            "h": BarAggregation.HOUR,
            "d": BarAggregation.DAY,
            "w": BarAggregation.WEEK,
            "M": BarAggregation.MONTH,
        }
        self.int_to_ext_bar_agg = {b: a for a, b in self.ext_to_int_bar_agg.items()}

        self.ext_to_int_time_in_force = {
            CoinbaseTimeInForce.FOK: TimeInForce.FOK,
            CoinbaseTimeInForce.GTC: TimeInForce.GTC,
            CoinbaseTimeInForce.GTX: TimeInForce.GTC,  # Convert GTX to GTC
            CoinbaseTimeInForce.GTE_GTC: TimeInForce.GTC,  # Undocumented
            CoinbaseTimeInForce.IOC: TimeInForce.IOC,
        }
        self.int_to_ext_time_in_force = {
            TimeInForce.GTC: CoinbaseTimeInForce.GTC,
            TimeInForce.GTD: CoinbaseTimeInForce.GTC,  # Convert GTD to GTC
            TimeInForce.FOK: CoinbaseTimeInForce.FOK,
            TimeInForce.IOC: CoinbaseTimeInForce.IOC,
        }

    def parse_coinbase_order_side(self, order_side: CoinbaseOrderSide) -> OrderSide:
        try:
            return self.ext_to_int_order_side[order_side]
        except KeyError:
            raise RuntimeError(  # pragma: no cover (design-time error)
                f"unrecognized Coinbase order side, was {order_side}",  # pragma: no cover
            )

    def parse_internal_order_side(self, order_side: OrderSide) -> CoinbaseOrderSide:
        try:
            return self.int_to_ext_order_side[order_side]
        except KeyError:
            raise RuntimeError(  # pragma: no cover (design-time error)
                f"unrecognized Nautilus order side, was {order_side}",  # pragma: no cover
            )

    def parse_coinbase_time_in_force(self, time_in_force: CoinbaseTimeInForce) -> TimeInForce:
        try:
            return self.ext_to_int_time_in_force[time_in_force]
        except KeyError:
            raise RuntimeError(  # pragma: no cover (design-time error)
                f"unrecognized Coinbase time in force, was {time_in_force}",  # pragma: no cover
            )

    def parse_internal_time_in_force(self, time_in_force: TimeInForce) -> CoinbaseTimeInForce:
        try:
            return self.int_to_ext_time_in_force[time_in_force]
        except KeyError:
            raise RuntimeError(  # pragma: no cover (design-time error)
                f"unrecognized Nautilus time in force, was {time_in_force}",  # pragma: no cover
            )

    def parse_coinbase_order_status(self, order_status: CoinbaseOrderStatus) -> OrderStatus:
        try:
            return self.ext_to_int_status[order_status]
        except KeyError:
            raise RuntimeError(  # pragma: no cover (design-time error)
                f"unrecognized Coinbase order status, was {order_status}",  # pragma: no cover
            )

    def parse_coinbase_order_type(self, order_type: CoinbaseOrderType) -> OrderType:
        # Implement in child class
        raise NotImplementedError

    def parse_internal_order_type(self, order: Order) -> CoinbaseOrderType:
        # Implement in child class
        raise NotImplementedError

    def parse_coinbase_bar_agg(self, bar_agg: str) -> BarAggregation:
        try:
            return self.ext_to_int_bar_agg[bar_agg]
        except KeyError:
            raise RuntimeError(  # pragma: no cover (design-time error)
                f"unrecognized Coinbase kline resolution, was {bar_agg}",
            )

    def parse_internal_bar_agg(self, bar_agg: BarAggregation) -> str:
        try:
            return self.int_to_ext_bar_agg[bar_agg]
        except KeyError:
            raise RuntimeError(  # pragma: no cover (design-time error)
                "unrecognized or non-supported Nautilus BarAggregation,",
                f"was {bar_aggregation_to_str(bar_agg)}",  # pragma: no cover
            )

    def parse_coinbase_kline_interval_to_bar_spec(
        self,
        kline_interval: CoinbaseKlineInterval,
    ) -> BarSpecification:
        step = kline_interval.value[:-1]
        coinbase_bar_agg = kline_interval.value[-1]
        return BarSpecification(
            step=int(step),
            aggregation=self.parse_coinbase_bar_agg(coinbase_bar_agg),
            price_type=PriceType.LAST,
        )

    def parse_coinbase_trigger_type(self, trigger_type: str) -> TriggerType:
        # Replace method in child class, if compatible
        raise NotImplementedError(  # pragma: no cover (design-time error)
            "Cannot parse Coinbase trigger type (not implemented).",  # pragma: no cover
        )
