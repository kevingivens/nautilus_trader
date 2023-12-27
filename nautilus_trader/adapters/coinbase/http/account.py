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
from nautilus_trader.adapters.coinbase.enums import CoinbaseMethodType
from nautilus_trader.adapters.coinbase.enums import CoinbaseNewOrderRespType
from nautilus_trader.adapters.coinbase.enums import CoinbaseOrderSide
from nautilus_trader.adapters.coinbase.enums import CoinbaseOrderType
from nautilus_trader.adapters.coinbase.enums import CoinbaseSecurityType
from nautilus_trader.adapters.coinbase.enums import CoinbaseTimeInForce
from nautilus_trader.adapters.coinbase.schemas.account import CoinbaseOrder
from nautilus_trader.adapters.coinbase.schemas.account import CoinbaseUserTrade
from nautilus_trader.adapters.coinbase.schemas.symbol import CoinbaseSymbol
from nautilus_trader.adapters.coinbase.http.client import CoinbaseHttpClient
from nautilus_trader.adapters.coinbase.http.endpoint import CoinbaseHttpEndpoint
from nautilus_trader.common.clock import LiveClock
from nautilus_trader.core.correctness import PyCondition


class CoinbaseOrderHttp(CoinbaseHttpEndpoint):
    """
    Endpoint for managing orders.

    `GET /api/v3/order`
    `GET /api/v3/order/test`
  
    `POST /api/v3/brokerage/orders`

    `DELETE /api/v3/order`

    References
    ----------
    https://docs.cloud.coinbase.com/advanced-trade-api/reference/retailbrokerageapi_postorder
    """

    def __init__(
        self,
        client: CoinbaseHttpClient,
        base_endpoint: str,
        testing_endpoint: Optional[bool] = False,
    ):
        methods = {
            CoinbaseMethodType.GET: CoinbaseSecurityType.USER_DATA,
            CoinbaseMethodType.POST: CoinbaseSecurityType.TRADE,
            CoinbaseMethodType.DELETE: CoinbaseSecurityType.TRADE,
        }
        url_path = base_endpoint + "order"
        if testing_endpoint:
            url_path = url_path + "/test"
        super().__init__(
            client,
            methods,
            url_path,
        )
        self._resp_decoder = msgspec.json.Decoder(CoinbaseOrder)

    class GetDeleteParameters(msgspec.Struct, omit_defaults=True, frozen=True):
        """
        Order management GET & DELETE endpoint parameters

        Parameters
        ----------
        symbol : CoinbaseSymbol
            The symbol of the order
        timestamp : str
            The millisecond timestamp of the request
        orderId : str, optional
            the order identifier
        origClientOrderId : str, optional
            the client specified order identifier
        recvWindow : str, optional
            the millisecond timeout window.

        Warnings
        --------
        Either orderId or origClientOrderId must be sent.
        """

        symbol: CoinbaseSymbol
        timestamp: str
        orderId: Optional[str] = None
        origClientOrderId: Optional[str] = None
        recvWindow: Optional[str] = None

    class PostParameters(msgspec.Struct, omit_defaults=True, frozen=True):
        """
        Order creation POST endpoint parameters.

        Parameters
        ----------
        client_order_id : str, required
            Client set unique uuid for this order

        product_id : str, required
            The product this order was created for e.g. 'BTC-USD'

        side : str CoinbaseOrderSide
            Possible values: [UNKNOWN_ORDER_SIDE, BUY, SELL]

        order_configuration : object
        
            market_market_ioc : object
                quote_size, str
                    Amount of quote currency to spend on order. Required for BUY orders.

                base_size: str
                    Amount of base currency to spend on order. Required for SELL orders.

            limit_limit_gtc : object
                base_size, str
                    Amount of base currency to spend on order

                limit_price: str
                    Ceiling price for which the order should get filled

                post_only : boolean
                    Post only limit order


            limit_limit_gtd : object
                base_size : str
                    Amount of base currency to spend on order

                limit_price : str
                    Ceiling price for which the order should get filled

                end_time : date-time
                    Time at which the order should be cancelled if it's not filled. mm/dd/yyyy, --:-- --

                post_only: bool
                    Post only limit order


            stop_limit_stop_limit_gtc : object
                base_size : str
                    Amount of base currency to spend on order

                limit_price : str
                    Ceiling price for which the order should get filled

                stop_price : str
                    Price at which the order should trigger - if stop direction is Up, then the order will trigger 
                    when the last trade price goes above this, otherwise order will trigger when last trade price goes below this price.

                stop_direction : str
                    Possible values: [UNKNOWN_STOP_DIRECTION, STOP_DIRECTION_STOP_UP, STOP_DIRECTION_STOP_DOWN]

            stop_limit_stop_limit_gtd : object
                base_size : str
                    Amount of base currency to spend on order

                limit_price : str
                    Ceiling price for which the order should get filled

                stop_price : str
                    Price at which the order should trigger - 
                    if stop direction is Up, then the order will trigger when 
                    the last trade price goes above this, otherwise order will 
                    trigger when last trade price goes below this price.

                end_time : date-time
                    Time at which the order should be cancelled if it's not filled.  mm/dd/yyyy, --:-- --

                stop_direction : str CoinbaseStopDirection
                    Possible values: [UNKNOWN_STOP_DIRECTION, STOP_DIRECTION_STOP_UP, STOP_DIRECTION_STOP_DOWN]



        symbol : CoinbaseSymbol
            The symbol of the order
        timestamp : str
            The millisecond timestamp of the request
        side : CoinbaseOrderSide
            The market side of the order (BUY, SELL)
        type : CoinbaseOrderType
            The type of the order (LIMIT, STOP_LOSS..)
        timeInForce : CoinbaseTimeInForce, optional
            Mandatory for LIMIT, STOP_LOSS_LIMIT, TAKE_PROFIT_LIMIT orders.
            The time in force of the order (GTC, IOC..)
        quantity : str, optional
            Mandatory for all order types, except STOP_MARKET/TAKE_PROFIT_MARKET
            and TRAILING_STOP_MARKET orders
            The order quantity in base asset units for the request
        quoteOrderQty : str, optional
            Only for SPOT/MARGIN orders.
            Can be used alternatively to `quantity` for MARKET orders
            The order quantity in quote asset units for the request
        price : str, optional
            Mandatory for LIMIT, STOP_LOSS_LIMIT, TAKE_PROFIT_LIMIT, LIMIT_MAKER,
            STOP, TAKE_PROFIT orders
            The order price for the request
        newClientOrderId : str, optional
            The client order ID for the request. A unique ID among open orders.
            Automatically generated if not provided.
        strategyId : int,  optional
            Only for SPOT/MARGIN orders.
            The client strategy ID for the request.
        strategyType : int, optional
            Only for SPOT/MARGIN orders
            The client strategy type for thr request. Cannot be less than 1000000
        stopPrice : str, optional
            Mandatory for STOP_LOSS, STOP_LOSS_LIMIT, TAKE_PROFIT, TAKE_PROFIT_LIMIT,
            STOP, STOP_MARKET, TAKE_PROFIT_MARKET.
            The order stop price for the request.
        trailingDelta : str, optional
            Only for SPOT/MARGIN orders
            Can be used instead of or in addition to stopPrice for STOP_LOSS,
            STOP_LOSS_LIMIT, TAKE_PROFIT, TAKE_PROFIT_LIMIT orders.
            The order trailing delta of the request.
        icebergQty : str, optional
            Only for SPOT/MARGIN orders
            Can be used with LIMIT, STOP_LOSS_LIMIT, and TAKE_PROFIT_LIMIT to
            create an iceberg order.
        reduceOnly : str ('true', 'false'), optional
            Only for FUTURES orders
            Cannot be sent in Hedge Mode, cannot be sent with closePosition = 'true'
        closePosition : str ('true', 'false'), optional
            Only for FUTURES orders
            Can be used with STOP_MARKET or TAKE_PROFIT_MARKET orders
            Whether to close all open positions for the given symbol.
        activationPrice : str, optional
            Only for FUTURES orders
            Can be used with TRAILING_STOP_MARKET orders.
            Defaults to the latest price.
        callbackRate : str, optional
            Only for FUTURES orders
            Mandatory for TRAILING_STOP_MARKET orders.
            The order trailing delta of the request.
        workingType : str ("MARK_PRICE", "CONTRACT_PRICE"), optional
            Only for FUTURES orders
            The trigger type for the order.
            Defaults to "CONTRACT_PRICE"
        priceProtect : str ('true', 'false'), optional
            Only for FUTURES orders
            Whether price protection is active.
            Defaults to 'false'
        newOrderRespType : NewOrderRespType, optional
            The response type for the order request.
            SPOT/MARGIN MARKET, LIMIT orders default to FULL.
            All others default to ACK.
            FULL response only for SPOT/MARGIN orders.
        recvWindow : str, optional
            The response receive window in milliseconds for the request.
            Cannot exceed 60000.
        """

        symbol: CoinbaseSymbol
        timestamp: str
        side: CoinbaseOrderSide
        type: CoinbaseOrderType
        timeInForce: Optional[CoinbaseTimeInForce] = None
        quantity: Optional[str] = None
        quoteOrderQty: Optional[str] = None
        price: Optional[str] = None
        newClientOrderId: Optional[str] = None
        strategyId: Optional[int] = None
        strategyType: Optional[int] = None
        stopPrice: Optional[str] = None
        trailingDelta: Optional[str] = None
        icebergQty: Optional[str] = None
        reduceOnly: Optional[str] = None
        closePosition: Optional[str] = None
        activationPrice: Optional[str] = None
        callbackRate: Optional[str] = None
        workingType: Optional[str] = None
        priceProtect: Optional[str] = None
        newOrderRespType: Optional[CoinbaseNewOrderRespType] = None
        recvWindow: Optional[str] = None

    async def _get(self, parameters: GetDeleteParameters) -> CoinbaseOrder:
        method_type = CoinbaseMethodType.GET
        raw = await self._method(method_type, parameters)
        return self._resp_decoder.decode(raw)

    async def _delete(self, parameters: GetDeleteParameters) -> CoinbaseOrder:
        method_type = CoinbaseMethodType.DELETE
        raw = await self._method(method_type, parameters)
        return self._resp_decoder.decode(raw)

    async def _post(self, parameters: PostParameters) -> CoinbaseOrder:
        method_type = CoinbaseMethodType.POST
        raw = await self._method(method_type, parameters)
        return self._resp_decoder.decode(raw)


class CoinbaseAllOrdersHttp(CoinbaseHttpEndpoint):
    """
    Endpoint of all account orders, active, cancelled or filled.

    `GET /api/v3/allOrders`
    `GET /fapi/v1/allOrders`
    `GET /dapi/v1/allOrders`

    References
    ----------
    https://Coinbase-docs.github.io/apidocs/spot/en/#all-orders-user_data
    https://Coinbase-docs.github.io/apidocs/futures/en/#all-orders-user_data
    https://Coinbase-docs.github.io/apidocs/delivery/en/#all-orders-user_data
    """

    def __init__(
        self,
        client: CoinbaseHttpClient,
        base_endpoint: str,
    ):
        methods = {
            CoinbaseMethodType.GET: CoinbaseSecurityType.USER_DATA,
        }
        url_path = base_endpoint + "allOrders"
        super().__init__(
            client,
            methods,
            url_path,
        )
        self._get_resp_decoder = msgspec.json.Decoder(list[CoinbaseOrder])

    class GetParameters(msgspec.Struct, omit_defaults=True, frozen=True):
        """
        Parameters of allOrders GET request.

        Parameters
        ----------
        symbol : CoinbaseSymbol
            The symbol of the orders
        timestamp : str
            The millisecond timestamp of the request
        orderId : str, optional
            The order ID for the request.
            If included, request will return orders from this orderId INCLUSIVE
        startTime : str, optional
            The start time (UNIX milliseconds) filter for the request.
        endTime : str, optional
            The end time (UNIX milliseconds) filter for the request.
        limit : int, optional
            The limit for the response.
            Default 500, max 1000
        recvWindow : str, optional
            The response receive window for the request (cannot be greater than 60000).
        """

        symbol: CoinbaseSymbol
        timestamp: str
        orderId: Optional[str] = None
        startTime: Optional[str] = None
        endTime: Optional[str] = None
        limit: Optional[int] = None
        recvWindow: Optional[str] = None

    async def _get(self, parameters: GetParameters) -> list[CoinbaseOrder]:
        method_type = CoinbaseMethodType.GET
        raw = await self._method(method_type, parameters)
        return self._get_resp_decoder.decode(raw)


class CoinbaseOpenOrdersHttp(CoinbaseHttpEndpoint):
    """
    Endpoint of all open orders on a symbol.

    `GET /api/v3/openOrders`
    `GET /fapi/v1/openOrders`
    `GET /dapi/v1/openOrders`

    Warnings
    --------
    Care should be taken when accessing this endpoint with no symbol specified.
    The weight usage can be very large, which may cause rate limits to be hit.

    References
    ----------
    https://Coinbase-docs.github.io/apidocs/spot/en/#current-open-orders-user_data
    https://Coinbase-docs.github.io/apidocs/futures/en/#current-all-open-orders-user_data
    https://Coinbase-docs.github.io/apidocs/futures/en/#current-all-open-orders-user_data
    """

    def __init__(
        self,
        client: CoinbaseHttpClient,
        base_endpoint: str,
        methods: Optional[dict[CoinbaseMethodType, CoinbaseSecurityType]] = None,
    ):
        if methods is None:
            methods = {
                CoinbaseMethodType.GET: CoinbaseSecurityType.USER_DATA,
            }
        url_path = base_endpoint + "openOrders"
        super().__init__(
            client,
            methods,
            url_path,
        )
        self._get_resp_decoder = msgspec.json.Decoder(list[CoinbaseOrder])

    class GetParameters(msgspec.Struct, omit_defaults=True, frozen=True):
        """
        Parameters of openOrders GET request.

        Parameters
        ----------
        timestamp : str
            The millisecond timestamp of the request
        symbol : CoinbaseSymbol, optional
            The symbol of the orders
        recvWindow : str, optional
            The response receive window for the request (cannot be greater than 60000).
        """

        timestamp: str
        symbol: Optional[CoinbaseSymbol] = None
        recvWindow: Optional[str] = None

    async def _get(self, parameters: GetParameters) -> list[CoinbaseOrder]:
        method_type = CoinbaseMethodType.GET
        raw = await self._method(method_type, parameters)
        return self._get_resp_decoder.decode(raw)


class CoinbaseUserTradesHttp(CoinbaseHttpEndpoint):
    """
    Endpoint of trades for a specific account and symbol.

    `GET /api/v3/myTrades`
    `GET /fapi/v1/userTrades`
    `GET /dapi/v1/userTrades`

    References
    ----------
    https://Coinbase-docs.github.io/apidocs/spot/en/#account-trade-list-user_data
    https://Coinbase-docs.github.io/apidocs/futures/en/#account-trade-list-user_data
    https://Coinbase-docs.github.io/apidocs/delivery/en/#account-trade-list-user_data
    """

    def __init__(
        self,
        client: CoinbaseHttpClient,
        url_path: str,
    ):
        methods = {
            CoinbaseMethodType.GET: CoinbaseSecurityType.USER_DATA,
        }
        super().__init__(
            client,
            methods,
            url_path,
        )
        self._get_resp_decoder = msgspec.json.Decoder(list[CoinbaseUserTrade])

    class GetParameters(msgspec.Struct, omit_defaults=True, frozen=True):
        """
        Parameters of allOrders GET request.

        Parameters
        ----------
        symbol : CoinbaseSymbol
            The symbol of the orders
        timestamp : str
            The millisecond timestamp of the request
        orderId : str, optional
            The order ID for the request.
            If included, request will return orders from this orderId INCLUSIVE
        startTime : str, optional
            The start time (UNIX milliseconds) filter for the request.
        endTime : str, optional
            The end time (UNIX milliseconds) filter for the request.
        fromId : str, optional
            TradeId to fetch from. Default gets most recent trades.
        limit : int, optional
            The limit for the response.
            Default 500, max 1000
        recvWindow : str, optional
            The response receive window for the request (cannot be greater than 60000).
        """

        symbol: CoinbaseSymbol
        timestamp: str
        orderId: Optional[str] = None
        startTime: Optional[str] = None
        endTime: Optional[str] = None
        fromId: Optional[str] = None
        limit: Optional[int] = None
        recvWindow: Optional[str] = None

    async def _get(self, parameters: GetParameters) -> list[CoinbaseUserTrade]:
        method_type = CoinbaseMethodType.GET
        raw = await self._method(method_type, parameters)
        return self._get_resp_decoder.decode(raw)


class CoinbaseAccountHttpAPI:
    """
    Provides access to the Coinbase Account/Trade HTTP REST API.

    Parameters
    ----------
    client : CoinbaseHttpClient
        The Coinbase REST API client.
    account_type : CoinbaseAccountType
        The Coinbase account type, used to select the endpoint prefix

    Warnings
    --------
    This class should not be used directly, but through a concrete subclass.
    """

    def __init__(
        self,
        client: CoinbaseHttpClient,
        clock: LiveClock,
        account_type: CoinbaseAccountType,
    ):
        PyCondition.not_none(client, "client")
        self.client = client
        self._clock = clock

        if account_type.is_spot_or_margin:
            self.base_endpoint = "/api/v3/"
            user_trades_url = self.base_endpoint + "myTrades"
        elif account_type == CoinbaseAccountType.FUTURES_USDT:
            self.base_endpoint = "/fapi/v1/"
            user_trades_url = self.base_endpoint + "userTrades"
        elif account_type == CoinbaseAccountType.FUTURES_COIN:
            self.base_endpoint = "/dapi/v1/"
            user_trades_url = self.base_endpoint + "userTrades"
        else:
            raise RuntimeError(  # pragma: no cover (design-time error)
                f"invalid `CoinbaseAccountType`, was {account_type}",  # pragma: no cover
            )

        # Create endpoints
        self._endpoint_order = CoinbaseOrderHttp(client, self.base_endpoint)
        self._endpoint_all_orders = CoinbaseAllOrdersHttp(client, self.base_endpoint)
        self._endpoint_open_orders = CoinbaseOpenOrdersHttp(client, self.base_endpoint)
        self._endpoint_user_trades = CoinbaseUserTradesHttp(client, user_trades_url)

    def _timestamp(self) -> str:
        """Create Coinbase timestamp from internal clock."""
        return str(self._clock.timestamp_ms())

    async def query_order(
        self,
        symbol: str,
        order_id: Optional[str] = None,
        orig_client_order_id: Optional[str] = None,
        recv_window: Optional[str] = None,
    ) -> CoinbaseOrder:
        """Check an order status."""
        if order_id is None and orig_client_order_id is None:
            raise RuntimeError(
                "Either orderId or origClientOrderId must be sent.",
            )
        Coinbase_order = await self._endpoint_order._get(
            parameters=self._endpoint_order.GetDeleteParameters(
                symbol=CoinbaseSymbol(symbol),
                timestamp=self._timestamp(),
                orderId=order_id,
                origClientOrderId=orig_client_order_id,
                recvWindow=recv_window,
            ),
        )
        return Coinbase_order

    async def cancel_all_open_orders(
        self,
        symbol: str,
        recv_window: Optional[str] = None,
    ) -> bool:
        # Implement in child class
        raise NotImplementedError

    async def cancel_order(
        self,
        symbol: str,
        order_id: Optional[str] = None,
        orig_client_order_id: Optional[str] = None,
        recv_window: Optional[str] = None,
    ) -> CoinbaseOrder:
        """Cancel an active order."""
        if order_id is None and orig_client_order_id is None:
            raise RuntimeError(
                "Either orderId or origClientOrderId must be sent.",
            )
        Coinbase_order = await self._endpoint_order._delete(
            parameters=self._endpoint_order.GetDeleteParameters(
                symbol=CoinbaseSymbol(symbol),
                timestamp=self._timestamp(),
                orderId=order_id,
                origClientOrderId=orig_client_order_id,
                recvWindow=recv_window,
            ),
        )
        return Coinbase_order

    async def new_order(
        self,
        symbol: str,
        side: CoinbaseOrderSide,
        order_type: CoinbaseOrderType,
        time_in_force: Optional[CoinbaseTimeInForce] = None,
        quantity: Optional[str] = None,
        quote_order_qty: Optional[str] = None,
        price: Optional[str] = None,
        new_client_order_id: Optional[str] = None,
        strategy_id: Optional[int] = None,
        strategy_type: Optional[int] = None,
        stop_price: Optional[str] = None,
        trailing_delta: Optional[str] = None,
        iceberg_qty: Optional[str] = None,
        reduce_only: Optional[str] = None,
        close_position: Optional[str] = None,
        activation_price: Optional[str] = None,
        callback_rate: Optional[str] = None,
        working_type: Optional[str] = None,
        price_protect: Optional[str] = None,
        new_order_resp_type: Optional[CoinbaseNewOrderRespType] = None,
        recv_window: Optional[str] = None,
    ) -> CoinbaseOrder:
        """Send in a new order to Coinbase."""
        Coinbase_order = await self._endpoint_order._post(
            parameters=self._endpoint_order.PostParameters(
                symbol=CoinbaseSymbol(symbol),
                timestamp=self._timestamp(),
                side=side,
                type=order_type,
                timeInForce=time_in_force,
                quantity=quantity,
                quoteOrderQty=quote_order_qty,
                price=price,
                newClientOrderId=new_client_order_id,
                strategyId=strategy_id,
                strategyType=strategy_type,
                stopPrice=stop_price,
                trailingDelta=trailing_delta,
                icebergQty=iceberg_qty,
                reduceOnly=reduce_only,
                closePosition=close_position,
                activationPrice=activation_price,
                callbackRate=callback_rate,
                workingType=working_type,
                priceProtect=price_protect,
                newOrderRespType=new_order_resp_type,
                recvWindow=recv_window,
            ),
        )
        return Coinbase_order

    async def query_all_orders(
        self,
        symbol: str,
        order_id: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        limit: Optional[int] = None,
        recv_window: Optional[str] = None,
    ) -> list[CoinbaseOrder]:
        """Query all orders, active or filled."""
        return await self._endpoint_all_orders._get(
            parameters=self._endpoint_all_orders.GetParameters(
                symbol=CoinbaseSymbol(symbol),
                timestamp=self._timestamp(),
                orderId=order_id,
                startTime=start_time,
                endTime=end_time,
                limit=limit,
                recvWindow=recv_window,
            ),
        )

    async def query_open_orders(
        self,
        symbol: Optional[str] = None,
        recv_window: Optional[str] = None,
    ) -> list[CoinbaseOrder]:
        """Query open orders."""
        return await self._endpoint_open_orders._get(
            parameters=self._endpoint_open_orders.GetParameters(
                symbol=CoinbaseSymbol(symbol),
                timestamp=self._timestamp(),
                recvWindow=recv_window,
            ),
        )

    async def query_user_trades(
        self,
        symbol: str,
        order_id: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        from_id: Optional[str] = None,
        limit: Optional[int] = None,
        recv_window: Optional[str] = None,
    ) -> list[CoinbaseUserTrade]:
        """Query user's trade history for a symbol, with provided filters."""
        if (order_id or from_id) is not None and (start_time or end_time) is not None:
            raise RuntimeError(
                "Cannot specify both order_id/from_id AND start_time/end_time parameters.",
            )
        return await self._endpoint_user_trades._get(
            parameters=self._endpoint_user_trades.GetParameters(
                symbol=CoinbaseSymbol(symbol),
                timestamp=self._timestamp(),
                orderId=order_id,
                startTime=start_time,
                endTime=end_time,
                fromId=from_id,
                limit=limit,
                recvWindow=recv_window,
            ),
        )
