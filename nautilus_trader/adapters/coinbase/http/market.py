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

from typing import Optional

import msgspec

from nautilus_trader.adapters.coinbase.enums import CoinbaseAccountType
from nautilus_trader.adapters.coinbase.enums import CoinbaseKlineInterval
from nautilus_trader.adapters.coinbase.enums import CoinbaseMethodType
from nautilus_trader.adapters.coinbase.enums import CoinbaseSecurityType
from nautilus_trader.adapters.coinbase.schemas.market import CoinbaseAggTrade
from nautilus_trader.adapters.coinbase.schemas.market import CoinbaseDepth
from nautilus_trader.adapters.coinbase.schemas.market import CoinbaseKline
from nautilus_trader.adapters.coinbase.schemas.market import CoinbaseTicker24hr
from nautilus_trader.adapters.coinbase.schemas.market import CoinbaseTickerBook
from nautilus_trader.adapters.coinbase.schemas.market import CoinbaseTickerPrice
from nautilus_trader.adapters.coinbase.schemas.market import CoinbaseTime
from nautilus_trader.adapters.coinbase.schemas.market import CoinbaseTrade
from nautilus_trader.adapters.coinbase.schemas.symbol import CoinbaseSymbol
from nautilus_trader.adapters.coinbase.schemas.symbol import CoinbaseSymbols
from nautilus_trader.adapters.coinbase.types import CoinbaseBar
from nautilus_trader.adapters.coinbase.http.client import CoinbaseHttpClient
from nautilus_trader.adapters.coinbase.http.endpoint import CoinbaseHttpEndpoint
from nautilus_trader.core.correctness import PyCondition
from nautilus_trader.model.data.bar import BarType
from nautilus_trader.model.data.tick import TradeTick
from nautilus_trader.model.identifiers import InstrumentId
from nautilus_trader.model.orderbook.data import OrderBookSnapshot


#class CoinbasePingHttp(CoinbaseHttpEndpoint):
#    """
#    Endpoint for testing connectivity to the REST API.
#
#    `GET /api/v3/ping`
#
#    References
#    ----------
#    https://binance-docs.github.io/apidocs/spot/en/#test-connectivity
#    """
#
#    def __init__(
#        self,
#        client: CoinbaseHttpClient,
#        base_endpoint: str,
#    ):
#        methods = {
#            CoinbaseMethodType.GET: CoinbaseSecurityType.NONE,
#        }
#        url_path = base_endpoint + "ping"
#        super().__init__(
#            client,
#            methods,
#            url_path,
#        )
#        self._get_resp_decoder = msgspec.json.Decoder()
#
#    async def _get(self) -> dict:
#        method_type = CoinbaseMethodType.GET
#        raw = await self._method(method_type, None)
#        return self._get_resp_decoder.decode(raw)


#class CoinbaseTimeHttp(CoinbaseHttpEndpoint):
#    """
#    Endpoint for testing connectivity to the REST API and receiving current server time.
#
#    `GET /api/v3/time`
#
#    References
#    ----------
#    https://binance-docs.github.io/apidocs/spot/en/#check-server-time
#    """
#
#    def __init__(
#        self,
#        client: CoinbaseHttpClient,
#        base_endpoint: str,
#    ):
#        methods = {
#            CoinbaseMethodType.GET: CoinbaseSecurityType.NONE,
#        }
#        url_path = base_endpoint + "time"
#        super().__init__(client, methods, url_path)
#        self._get_resp_decoder = msgspec.json.Decoder(CoinbaseTime)
#
#    async def _get(self) -> CoinbaseTime:
#        method_type = CoinbaseMethodType.GET
#        raw = await self._method(method_type, None)
#        return self._get_resp_decoder.decode(raw)


#class CoinbaseDepthHttp(CoinbaseHttpEndpoint):
#    """
#    Endpoint of orderbook depth.
#
#    `GET /api/v3/depth`
#
#    References
#    ----------
#    https://binance-docs.github.io/apidocs/spot/en/#order-book
#    """
#
#    def __init__(
#        self,
#        client: CoinbaseHttpClient,
#        base_endpoint: str,
#    ):
#        methods = {
#            CoinbaseMethodType.GET: CoinbaseSecurityType.NONE,
#        }
#        url_path = base_endpoint + "depth"
#        super().__init__(
#            client,
#            methods,
#            url_path,
#        )
#        self._get_resp_decoder = msgspec.json.Decoder(CoinbaseDepth)
#
#    class GetParameters(msgspec.Struct, omit_defaults=True, frozen=True):
#        """
#        Orderbook depth GET endpoint parameters.
#
#        Parameters
#        ----------
#        symbol : CoinbaseSymbol
#            The trading pair.
#        limit : int, optional, default 100
#            The limit for the response.
#            SPOT/MARGIN (GET /api/v3/depth)
#                Default 100; max 5000.
#            FUTURES (GET /*api/v1/depth)
#                Default 500; max 1000.
#                Valid limits:[5, 10, 20, 50, 100, 500, 1000].
#        """
#
#        symbol: CoinbaseSymbol
#        limit: Optional[int] = None
#
#    async def _get(self, parameters: GetParameters) -> CoinbaseDepth:
#        method_type = CoinbaseMethodType.GET
#        raw = await self._method(method_type, parameters)
#        return self._get_resp_decoder.decode(raw)


class CoinbaseTradesHttp(CoinbaseHttpEndpoint):
    """
    Endpoint of recent market trades.

    `GET /api/v3/brokerage/products/{product_id}/ticker`

    References
    ----------
    https://docs.cloud.coinbase.com/advanced-trade-api/reference/retailbrokerageapi_getmarkettrades
    """

    def __init__(
        self,
        client: CoinbaseHttpClient,
        base_endpoint: str,
    ):
        methods = {
            CoinbaseMethodType.GET: CoinbaseSecurityType.NONE,
        }
        # url_path = base_endpoint + "trades"
        url_path = base_endpoint + f"products/{product_id}/ticker"

        super().__init__(
            client,
            methods,
            url_path,
        )
        self._get_resp_decoder = msgspec.json.Decoder(list[CoinbaseTrade])

    class GetParameters(msgspec.Struct, omit_defaults=True, frozen=True):
        """
        GET parameters for recent trades

        Parameters
        ----------
        symbol : CoinbaseSymbol
            The trading pair.
        limit : int, optional
            The limit for the response. Default 500; max 1000.
        """

        symbol: CoinbaseSymbol
        limit: Optional[int] = None

    async def _get(self, parameters: GetParameters) -> list[CoinbaseTrade]:
        method_type = CoinbaseMethodType.GET
        raw = await self._method(method_type, parameters)
        return self._get_resp_decoder.decode(raw)


class CoinbaseHistoricalTradesHttp(CoinbaseHttpEndpoint):
    """
    Endpoint of older market historical trades

    `GET /api/v3/historicalTrades`

    References
    ----------
    https://binance-docs.github.io/apidocs/spot/en/#old-trade-lookup-market_data
    """

    def __init__(
        self,
        client: CoinbaseHttpClient,
        base_endpoint: str,
    ):
        methods = {
            CoinbaseMethodType.GET: CoinbaseSecurityType.MARKET_DATA,
        }
        url_path = base_endpoint + "historicalTrades"
        super().__init__(
            client,
            methods,
            url_path,
        )
        self._get_resp_decoder = msgspec.json.Decoder(list[CoinbaseTrade])

    class GetParameters(msgspec.Struct, omit_defaults=True, frozen=True):
        """
        GET parameters for historical trades

        Parameters
        ----------
        symbol : CoinbaseSymbol
            The trading pair.
        limit : int, optional
            The limit for the response. Default 500; max 1000.
        fromId : str, optional
            Trade id to fetch from. Default gets most recent trades
        """

        symbol: CoinbaseSymbol
        limit: Optional[int] = None
        fromId: Optional[str] = None

    async def _get(self, parameters: GetParameters) -> list[CoinbaseTrade]:
        method_type = CoinbaseMethodType.GET
        raw = await self._method(method_type, parameters)
        return self._get_resp_decoder.decode(raw)


class CoinbaseAggTradesHttp(CoinbaseHttpEndpoint):
    """
    Endpoint of compressed and aggregated market trades.
    Market trades that fill in 100ms with the same price and same taking side
    will have the quantity aggregated.

    `GET /api/v3/aggTrades`

    References
    ----------
    https://binance-docs.github.io/apidocs/spot/en/#compressed-aggregate-trades-list
    """

    def __init__(
        self,
        client: CoinbaseHttpClient,
        base_endpoint: str,
    ):
        methods = {
            CoinbaseMethodType.GET: CoinbaseSecurityType.NONE,
        }
        url_path = base_endpoint + "aggTrades"
        super().__init__(
            client,
            methods,
            url_path,
        )
        self._get_resp_decoder = msgspec.json.Decoder(list[CoinbaseAggTrade])

    class GetParameters(msgspec.Struct, omit_defaults=True, frozen=True):
        """
        GET parameters for aggregate trades.

        Parameters
        ----------
        symbol : CoinbaseSymbol
            The trading pair.
        limit : int, optional
            The limit for the response. Default 500; max 1000.
        fromId : str, optional
            Trade id to fetch from INCLUSIVE.
        startTime : str, optional
            Timestamp in ms to get aggregate trades from INCLUSIVE.
        endTime : str, optional
            Timestamp in ms to get aggregate trades until INCLUSIVE.
        """

        symbol: CoinbaseSymbol
        limit: Optional[int] = None
        fromId: Optional[str] = None
        startTime: Optional[str] = None
        endTime: Optional[str] = None

    async def _get(self, parameters: GetParameters) -> list[CoinbaseAggTrade]:
        method_type = CoinbaseMethodType.GET
        raw = await self._method(method_type, parameters)
        return self._get_resp_decoder.decode(raw)


class CoinbaseCandlesHttp(CoinbaseHttpEndpoint):
    """
    Endpoint of Candlestick bars for a symbol.
    Klines are uniquely identified by their open time.

    `GET /api/v3/brokerage/products/{product_id}/candles`

    References
    ----------
    https://docs.cloud.coinbase.com/advanced-trade-api/reference/retailbrokerageapi_getcandles
    """

    def __init__(
        self,
        client: CoinbaseHttpClient,
        base_endpoint: str,
    ):
        methods = {
            CoinbaseMethodType.GET: CoinbaseSecurityType.NONE,
        }
        # url_path = base_endpoint + "klines"
        url_path = base_endpoint + f"products/{product_id}/candles"

        super().__init__(
            client,
            methods,
            url_path,
        )
        self._get_resp_decoder = msgspec.json.Decoder(list[CoinbaseKline])

    class GetParameters(msgspec.Struct, omit_defaults=True, frozen=True):
        """
        GET parameters for klines.

        Parameters
        ----------
        symbol : CoinbaseSymbol
            The trading pair.
        interval : str
            The interval of kline, e.g 1m, 5m, 1h, 1d, etc.
        limit : int, optional
            The limit for the response. Default 500; max 1000.
        startTime : str, optional
            Timestamp in ms to get klines from INCLUSIVE.
        endTime : str, optional
            Timestamp in ms to get klines until INCLUSIVE.
        """

        symbol: CoinbaseSymbol
        interval: CoinbaseKlineInterval
        limit: Optional[int] = None
        startTime: Optional[str] = None
        endTime: Optional[str] = None

    async def _get(self, parameters: GetParameters) -> list[CoinbaseKline]:
        method_type = CoinbaseMethodType.GET
        raw = await self._method(method_type, parameters)
        return self._get_resp_decoder.decode(raw)


class CoinbaseTicker24hrHttp(CoinbaseHttpEndpoint):
    """
    Endpoint of 24-hour rolling window price change statistics.

    `GET /api/v3/ticker/24hr`

    Warnings
    --------
    Care should be taken when accessing this endpoint with no symbol specified.
    The weight usage can be very large, which may cause rate limits to be hit.

    References
    ----------
    https://binance-docs.github.io/apidocs/spot/en/#24hr-ticker-price-change-statistics
    """

    def __init__(
        self,
        client: CoinbaseHttpClient,
        base_endpoint: str,
    ):
        methods = {
            CoinbaseMethodType.GET: CoinbaseSecurityType.NONE,
        }
        url_path = base_endpoint + "ticker/24hr"
        super().__init__(
            client,
            methods,
            url_path,
        )
        self._get_obj_resp_decoder = msgspec.json.Decoder(CoinbaseTicker24hr)
        self._get_arr_resp_decoder = msgspec.json.Decoder(list[CoinbaseTicker24hr])

    class GetParameters(msgspec.Struct, omit_defaults=True, frozen=True):
        """
        GET parameters for 24hr ticker.

        Parameters
        ----------
        symbol : CoinbaseSymbol
            The trading pair. When given, endpoint will return a single CoinbaseTicker24hr
            When omitted, endpoint will return a list of CoinbaseTicker24hr for all trading pairs.
        symbols : CoinbaseSymbols
            SPOT/MARGIN only!
            List of trading pairs. When given, endpoint will return a list of CoinbaseTicker24hr.
        type : str
            SPOT/MARGIN only!
            Select between FULL and MINI 24hr ticker responses to save bandwidth.
        """

        symbol: Optional[CoinbaseSymbol] = None
        symbols: Optional[CoinbaseSymbols] = None  # SPOT/MARGIN only
        type: Optional[str] = None  # SPOT/MARIN only

    async def _get(self, parameters: GetParameters) -> list[CoinbaseTicker24hr]:
        method_type = CoinbaseMethodType.GET
        raw = await self._method(method_type, parameters)
        if parameters.symbol is not None:
            return [self._get_obj_resp_decoder.decode(raw)]
        else:
            return self._get_arr_resp_decoder.decode(raw)


class CoinbaseTickerPriceHttp(CoinbaseHttpEndpoint):
    """
    Endpoint of latest price for a symbol or symbols.

    `GET /api/v3/ticker/price`

    References
    ----------
    https://binance-docs.github.io/apidocs/spot/en/#symbol-price-ticker
    """

    def __init__(
        self,
        client: CoinbaseHttpClient,
        base_endpoint: str,
    ):
        methods = {
            CoinbaseMethodType.GET: CoinbaseSecurityType.NONE,
        }
        url_path = base_endpoint + "ticker/price"
        super().__init__(
            client,
            methods,
            url_path,
        )
        self._get_obj_resp_decoder = msgspec.json.Decoder(CoinbaseTickerPrice)
        self._get_arr_resp_decoder = msgspec.json.Decoder(list[CoinbaseTickerPrice])

    class GetParameters(msgspec.Struct, omit_defaults=True, frozen=True):
        """
        GET parameters for price ticker.

        Parameters
        ----------
        symbol : CoinbaseSymbol
            The trading pair. When given, endpoint will return a single CoinbaseTickerPrice.
            When omitted, endpoint will return a list of CoinbaseTickerPrice for all trading pairs.
        symbols : str
            SPOT/MARGIN only!
            List of trading pairs. When given, endpoint will return a list of CoinbaseTickerPrice.
        """

        symbol: Optional[CoinbaseSymbol] = None
        symbols: Optional[CoinbaseSymbols] = None  # SPOT/MARGIN only

    async def _get(self, parameters: GetParameters) -> list[CoinbaseTickerPrice]:
        method_type = CoinbaseMethodType.GET
        raw = await self._method(method_type, parameters)
        if parameters.symbol is not None:
            return [self._get_obj_resp_decoder.decode(raw)]
        else:
            return self._get_arr_resp_decoder.decode(raw)


class CoinbaseTickerBookHttp(CoinbaseHttpEndpoint):
    """
    Endpoint of best price/qty on the order book for a symbol or symbols.

    `GET /api/v3/ticker/bookTicker`

    References
    ----------
    https://binance-docs.github.io/apidocs/spot/en/#symbol-order-book-ticker
    """

    def __init__(
        self,
        client: CoinbaseHttpClient,
        base_endpoint: str,
    ):
        methods = {
            CoinbaseMethodType.GET: CoinbaseSecurityType.NONE,
        }
        url_path = base_endpoint + "ticker/price"
        super().__init__(
            client,
            methods,
            url_path,
        )
        self._get_arr_resp_decoder = msgspec.json.Decoder(list[CoinbaseTickerBook])
        self._get_obj_resp_decoder = msgspec.json.Decoder(CoinbaseTickerBook)

    class GetParameters(msgspec.Struct, omit_defaults=True, frozen=True):
        """
        GET parameters for order book ticker.

        Parameters
        ----------
        symbol : str
            The trading pair. When given, endpoint will return a single CoinbaseTickerBook
            When omitted, endpoint will return a list of CoinbaseTickerBook for all trading pairs.
        symbols : str
            SPOT/MARGIN only!
            List of trading pairs. When given, endpoint will return a list of CoinbaseTickerBook.
        """

        symbol: Optional[CoinbaseSymbol] = None
        symbols: Optional[CoinbaseSymbols] = None  # SPOT/MARGIN only

    async def _get(self, parameters: GetParameters) -> list[CoinbaseTickerBook]:
        method_type = CoinbaseMethodType.GET
        raw = await self._method(method_type, parameters)
        if parameters.symbol is not None:
            return [self._get_obj_resp_decoder.decode(raw)]
        else:
            return self._get_arr_resp_decoder.decode(raw)


class CoinbaseMarketHttpAPI:
    """
    Provides access to the Coinbase Market HTTP REST API.

    Parameters
    ----------
    client : CoinbaseHttpClient
        The Coinbase REST API client.
    account_type : CoinbaseAccountType
        The Coinbase account type, used to select the endpoint prefix.

    Warnings
    --------
    This class should not be used directly, but through a concrete subclass.
    """

    def __init__(
        self,
        client: CoinbaseHttpClient,
        account_type: CoinbaseAccountType,
    ):
        PyCondition.not_none(client, "client")
        self.client = client

        if account_type.is_spot_or_margin:
            self.base_endpoint = "/api/v3/"
        elif account_type == CoinbaseAccountType.FUTURES_USDT:
            self.base_endpoint = "/fapi/v1/"
        elif account_type == CoinbaseAccountType.FUTURES_COIN:
            self.base_endpoint = "/dapi/v1/"
        else:
            raise RuntimeError(  # pragma: no cover (design-time error)
                f"invalid `CoinbaseAccountType`, was {account_type}",  # pragma: no cover
            )

        # Create Endpoints
        #self._endpoint_ping = CoinbasePingHttp(client, self.base_endpoint)
        #self._endpoint_time = CoinbaseTimeHttp(client, self.base_endpoint)
        self._endpoint_depth = CoinbaseDepthHttp(client, self.base_endpoint)
        self._endpoint_trades = CoinbaseTradesHttp(client, self.base_endpoint)
        self._endpoint_historical_trades = CoinbaseHistoricalTradesHttp(client, self.base_endpoint)
        self._endpoint_agg_trades = CoinbaseAggTradesHttp(client, self.base_endpoint)
        #self._endpoint_klines = CoinbaseKlinesHttp(client, self.base_endpoint)
        self._endpoint_klines = CoinbaseCandlesHttp(client, self.base_endpoint)
        self._endpoint_ticker_24hr = CoinbaseTicker24hrHttp(client, self.base_endpoint)
        self._endpoint_ticker_price = CoinbaseTickerPriceHttp(client, self.base_endpoint)
        self._endpoint_ticker_book = CoinbaseTickerBookHttp(client, self.base_endpoint)

    async def ping(self) -> dict:
        """Ping Coinbase REST API."""
        return await self._endpoint_ping._get()

    async def request_server_time(self) -> int:
        """Request server time from Coinbase."""
        response = await self._endpoint_time._get()
        return response.serverTime

    async def query_depth(
        self,
        symbol: str,
        limit: Optional[int] = None,
    ) -> CoinbaseDepth:
        """Query order book depth for a symbol."""
        return await self._endpoint_depth._get(
            parameters=self._endpoint_depth.GetParameters(
                symbol=CoinbaseSymbol(symbol),
                limit=limit,
            ),
        )

    async def request_order_book_snapshot(
        self,
        instrument_id: InstrumentId,
        ts_init: int,
        limit: Optional[int] = None,
    ) -> OrderBookSnapshot:
        """Request snapshot of order book depth."""
        depth = await self.query_depth(instrument_id.symbol.value, limit)
        return depth.parse_to_order_book_snapshot(
            instrument_id=instrument_id,
            ts_init=ts_init,
        )

    async def query_trades(
        self,
        symbol: str,
        limit: Optional[int] = None,
    ) -> list[CoinbaseTrade]:
        """Query trades for symbol."""
        return await self._endpoint_trades._get(
            parameters=self._endpoint_trades.GetParameters(
                symbol=CoinbaseSymbol(symbol),
                limit=limit,
            ),
        )

    async def request_trade_ticks(
        self,
        instrument_id: InstrumentId,
        ts_init: int,
        limit: Optional[int] = None,
    ) -> list[TradeTick]:
        """Request TradeTicks from Coinbase."""
        trades = await self.query_trades(instrument_id.symbol.value, limit)
        return [
            trade.parse_to_trade_tick(
                instrument_id=instrument_id,
                ts_init=ts_init,
            )
            for trade in trades
        ]

    async def query_agg_trades(
        self,
        symbol: str,
        limit: Optional[int] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        from_id: Optional[str] = None,
    ) -> list[CoinbaseAggTrade]:
        """Query aggregated trades for symbol."""
        return await self._endpoint_agg_trades._get(
            parameters=self._endpoint_agg_trades.GetParameters(
                symbol=CoinbaseSymbol(symbol),
                limit=limit,
                startTime=start_time,
                endTime=end_time,
                fromId=from_id,
            ),
        )

    async def request_agg_trade_ticks(
        self,
        instrument_id: InstrumentId,
        ts_init: int,
        limit: int = 1000,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        from_id: Optional[str] = None,
    ) -> list[TradeTick]:
        """
        Request TradeTicks from Coinbase aggregated trades.
        If start_time and end_time are both specified, will fetch *all* TradeTicks
        in the interval, making multiple requests if necessary.
        """
        ticks: list[TradeTick] = []
        next_start_time = start_time

        if from_id is not None and (start_time or end_time) is not None:
            raise RuntimeError(
                "Cannot specify both fromId and startTime or endTime.",
            )

        # Only split into separate requests if both start_time and end_time are specified
        max_interval = (1000 * 60 * 60) - 1  # 1ms under an hour, as specified in Futures docs.
        last_id = 0
        interval_limited = False

        def _calculate_next_end_time(start_time: str, end_time: str):
            next_interval = int(start_time) + max_interval
            interval_limited = next_interval < int(end_time)
            next_end_time = str(next_interval) if interval_limited is True else end_time
            return next_end_time, interval_limited

        if start_time is not None and end_time is not None:
            next_end_time, interval_limited = _calculate_next_end_time(start_time, end_time)
        else:
            next_end_time = end_time

        while True:
            response = await self.query_agg_trades(
                instrument_id.symbol.value,
                limit,
                start_time=next_start_time,
                end_time=next_end_time,
                from_id=from_id,
            )

            for trade in response:
                if not trade.a > last_id:
                    # Skip duplicate trades
                    continue
                ticks.append(
                    trade.parse_to_trade_tick(
                        instrument_id=instrument_id,
                        ts_init=ts_init,
                    ),
                )

            if len(response) < limit and interval_limited is False:
                # end loop regardless when limit is not hit
                break
            if start_time is None or end_time is None:
                break
            else:
                last = response[-1]
                last_id = last.a
                next_start_time = str(last.T)
                next_end_time, interval_limited = _calculate_next_end_time(
                    next_start_time,
                    end_time,
                )
                continue

        return ticks

    async def query_historical_trades(
        self,
        symbol: str,
        limit: Optional[int] = None,
        from_id: Optional[str] = None,
    ) -> list[CoinbaseTrade]:
        """Query historical trades for symbol."""
        return await self._endpoint_historical_trades._get(
            parameters=self._endpoint_historical_trades.GetParameters(
                symbol=CoinbaseSymbol(symbol),
                limit=limit,
                fromId=from_id,
            ),
        )

    async def request_historical_trade_ticks(
        self,
        instrument_id: InstrumentId,
        ts_init: int,
        limit: Optional[int] = None,
        from_id: Optional[str] = None,
    ) -> list[TradeTick]:
        """Request historical TradeTicks from Coinbase."""
        historical_trades = await self.query_historical_trades(
            symbol=instrument_id.symbol.value,
            limit=limit,
            from_id=from_id,
        )
        return [
            trade.parse_to_trade_tick(
                instrument_id=instrument_id,
                ts_init=ts_init,
            )
            for trade in historical_trades
        ]

    async def query_klines(
        self,
        symbol: str,
        interval: CoinbaseKlineInterval,
        limit: Optional[int] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
    ) -> list[CoinbaseKline]:
        """Query klines for a symbol over an interval."""
        return await self._endpoint_klines._get(
            parameters=self._endpoint_klines.GetParameters(
                symbol=CoinbaseSymbol(symbol),
                interval=interval,
                limit=limit,
                startTime=start_time,
                endTime=end_time,
            ),
        )

    async def request_binance_bars(
        self,
        bar_type: BarType,
        ts_init: int,
        interval: CoinbaseKlineInterval,
        limit: Optional[int] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
    ) -> list[CoinbaseBar]:
        """Request Coinbase Bars from Klines."""
        klines = await self.query_klines(
            symbol=bar_type.instrument_id.symbol.value,
            interval=interval,
            limit=limit,
            start_time=start_time,
            end_time=end_time,
        )
        bars: list[CoinbaseBar] = [kline.parse_to_binance_bar(bar_type, ts_init) for kline in klines]
        return bars

    async def query_ticker_24hr(
        self,
        symbol: Optional[str] = None,
        symbols: Optional[list[str]] = None,
        response_type: Optional[str] = None,
    ) -> list[CoinbaseTicker24hr]:
        """Query 24hr ticker for symbol or symbols."""
        if symbol is not None and symbols is not None:
            raise RuntimeError(
                "Cannot specify both symbol and symbols parameters.",
            )
        return await self._endpoint_ticker_24hr._get(
            parameters=self._endpoint_ticker_24hr.GetParameters(
                symbol=CoinbaseSymbol(symbol),
                symbols=CoinbaseSymbols(symbols),
                type=response_type,
            ),
        )

    async def query_ticker_price(
        self,
        symbol: Optional[str] = None,
        symbols: Optional[list[str]] = None,
    ) -> list[CoinbaseTickerPrice]:
        """Query price ticker for symbol or symbols."""
        if symbol is not None and symbols is not None:
            raise RuntimeError(
                "Cannot specify both symbol and symbols parameters.",
            )
        return await self._endpoint_ticker_price._get(
            parameters=self._endpoint_ticker_price.GetParameters(
                symbol=CoinbaseSymbol(symbol),
                symbols=CoinbaseSymbols(symbols),
            ),
        )

    async def query_ticker_book(
        self,
        symbol: Optional[str] = None,
        symbols: Optional[list[str]] = None,
    ) -> list[CoinbaseTickerBook]:
        """Query book ticker for symbol or symbols."""
        if symbol is not None and symbols is not None:
            raise RuntimeError(
                "Cannot specify both symbol and symbols parameters.",
            )
        return await self._endpoint_ticker_book._get(
            parameters=self._endpoint_ticker_book.GetParameters(
                symbol=CoinbaseSymbol(symbol),
                symbols=CoinbaseSymbols(symbols),
            ),
        )
