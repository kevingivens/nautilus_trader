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

import asyncio
import os
from functools import lru_cache
from typing import Optional, Union

from nautilus_trader.adapters.coinbase.common.enums import CoinbaseAccountType
from nautilus_trader.adapters.coinbase.config import CoinbaseDataClientConfig
from nautilus_trader.adapters.coinbase.config import BinanceExecClientConfig
# from nautilus_trader.adapters.coinbase.futures.data import BinanceFuturesDataClient
# from nautilus_trader.adapters.coinbase.futures.execution import BinanceFuturesExecutionClient
# from nautilus_trader.adapters.coinbase.futures.providers import BinanceFuturesInstrumentProvider
from nautilus_trader.adapters.coinbase.http.client import CoinbaseHttpClient
# from nautilus_trader.adapters.coinbase.spot.data import BinanceSpotDataClient
# from nautilus_trader.adapters.coinbase.spot.execution import BinanceSpotExecutionClient
# from nautilus_trader.adapters.coinbase.spot.providers import BinanceSpotInstrumentProvider
from nautilus_trader.cache.cache import Cache
from nautilus_trader.common.clock import LiveClock
from nautilus_trader.common.logging import Logger
from nautilus_trader.config import InstrumentProviderConfig
from nautilus_trader.live.factories import LiveDataClientFactory
from nautilus_trader.live.factories import LiveExecClientFactory
from nautilus_trader.msgbus.bus import MessageBus


COINBASE_HTTP_CLIENTS: dict[str, CoinbaseHttpClient] = {}


def get_cached_binance_http_client(
    loop: asyncio.AbstractEventLoop,
    clock: LiveClock,
    logger: Logger,
    account_type: CoinbaseAccountType,
    key: Optional[str] = None,
    secret: Optional[str] = None,
    base_url: Optional[str] = None,
    is_testnet: bool = False,
    is_us: bool = False,
) -> CoinbaseHttpClient:
    """
    Cache and return a Coinbase HTTP client with the given key and secret.

    If a cached client with matching key and secret already exists, then that
    cached client will be returned.

    Parameters
    ----------
    loop : asyncio.AbstractEventLoop
        The event loop for the client.
    clock : LiveClock
        The clock for the client.
    logger : Logger
        The logger for the client.
    account_type : CoinbaseAccountType
        The account type for the client.
    key : str, optional
        The API key for the client.
    secret : str, optional
        The API secret for the client.
    base_url : str, optional
        The base URL for the API endpoints.
    is_testnet : bool, default False
        If the client is connecting to the testnet API.
    is_us : bool, default False
        If the client is connecting to Coinbase US.

    Returns
    -------
    BinanceHttpClient

    """
    global COINBASE_HTTP_CLIENTS

    key = key or _get_api_key(account_type, is_testnet)
    secret = secret or _get_api_secret(account_type, is_testnet)
    default_http_base_url = _get_http_base_url(account_type, is_testnet, is_us)

    client_key: str = "|".join((key, secret))
    if client_key not in COINBASE_HTTP_CLIENTS:
        client = CoinbaseHttpClient(
            loop=loop,
            clock=clock,
            logger=logger,
            key=key,
            secret=secret,
            base_url=base_url or default_http_base_url,
        )
        COINBASE_HTTP_CLIENTS[client_key] = client
    return COINBASE_HTTP_CLIENTS[client_key]


@lru_cache(1)
def get_cached_binance_spot_instrument_provider(
    client: CoinbaseHttpClient,
    logger: Logger,
    clock: LiveClock,
    account_type: CoinbaseAccountType,
    config: InstrumentProviderConfig,
) -> BinanceSpotInstrumentProvider:
    """
    Cache and return an instrument provider for the `Binance Spot/Margin` exchange.

    If a cached provider already exists, then that provider will be returned.

    Parameters
    ----------
    client : BinanceHttpClient
        The client for the instrument provider.
    logger : Logger
        The logger for the instrument provider.
    clock : LiveClock
        The clock for the instrument provider.
    account_type : BinanceAccountType
        The Binance account type for the instrument provider.
    config : InstrumentProviderConfig
        The configuration for the instrument provider.

    Returns
    -------
    CoinbaseSpotInstrumentProvider

    """
    return CoinbaseSpotInstrumentProvider(
        client=client,
        logger=logger,
        clock=clock,
        account_type=account_type,
        config=config,
    )


@lru_cache(1)
def get_cached_binance_futures_instrument_provider(
    client: CoinbaseHttpClient,
    logger: Logger,
    clock: LiveClock,
    account_type: CoinbaseAccountType,
    config: InstrumentProviderConfig,
) -> CoinbaseFuturesInstrumentProvider:
    """
    Cache and return an instrument provider for the `Binance Futures` exchange.

    If a cached provider already exists, then that provider will be returned.

    Parameters
    ----------
    client : BinanceHttpClient
        The client for the instrument provider.
    logger : Logger
        The logger for the instrument provider.
    clock : LiveClock
        The clock for the instrument provider.
    account_type : BinanceAccountType
        The Binance account type for the instrument provider.
    config : InstrumentProviderConfig
        The configuration for the instrument provider.

    Returns
    -------
    BinanceFuturesInstrumentProvider

    """
    return CoinbaseFuturesInstrumentProvider(
        client=client,
        logger=logger,
        clock=clock,
        account_type=account_type,
        config=config,
    )


class BinanceLiveDataClientFactory(LiveDataClientFactory):
    """
    Provides a `Binance` live data client factory.
    """

    @staticmethod
    def create(  # type: ignore
        loop: asyncio.AbstractEventLoop,
        name: str,
        config: CoinbaseDataClientConfig,
        msgbus: MessageBus,
        cache: Cache,
        clock: LiveClock,
        logger: Logger,
    ) -> Union[CoinbaseSpotDataClient, CoinbaseFuturesDataClient]:
        """
        Create a new Coinbase data client.

        Parameters
        ----------
        loop : asyncio.AbstractEventLoop
            The event loop for the client.
        name : str
            The client name.
        config : CoinbaseDataClientConfig
            The client configuration.
        msgbus : MessageBus
            The message bus for the client.
        cache : Cache
            The cache for the client.
        clock : LiveClock
            The clock for the client.
        logger : Logger
            The logger for the client.

        Returns
        -------
        CoinbaseSpotDataClient or CoinbaseFuturesDataClient

        Raises
        ------
        ValueError
            If `config.account_type` is not a valid `CoinbaseAccountType`.

        """
        # Get HTTP client singleton
        client: CoinbaseHttpClient = get_cached_coinbase_http_client(
            loop=loop,
            clock=clock,
            logger=logger,
            account_type=config.account_type,
            key=config.api_key,
            secret=config.api_secret,
            base_url=config.base_url_http,
            is_testnet=config.testnet,
            is_us=config.us,
        )

        default_base_url_ws: str = _get_ws_base_url(
            account_type=config.account_type,
            is_testnet=config.testnet,
            is_us=config.us,
        )

        provider: Union[CoinbaseSpotInstrumentProvider, BinanceFuturesInstrumentProvider]
        if config.account_type.is_spot_or_margin:
            # Get instrument provider singleton
            provider = get_cached_binance_spot_instrument_provider(
                client=client,
                logger=logger,
                clock=clock,
                account_type=config.account_type,
                config=config.instrument_provider,
            )

            # Create client
            return CoinbaseSpotDataClient(
                loop=loop,
                client=client,
                msgbus=msgbus,
                cache=cache,
                clock=clock,
                logger=logger,
                instrument_provider=provider,
                account_type=config.account_type,
                base_url_ws=config.base_url_ws or default_base_url_ws,
                use_agg_trade_ticks=config.use_agg_trade_ticks,
            )
        else:
            # Get instrument provider singleton
            provider = get_cached_coinbase_futures_instrument_provider(
                client=client,
                logger=logger,
                clock=clock,
                account_type=config.account_type,
                config=config.instrument_provider,
            )

            # Create client
            return CoinbaseFuturesDataClient(
                loop=loop,
                client=client,
                msgbus=msgbus,
                cache=cache,
                clock=clock,
                logger=logger,
                instrument_provider=provider,
                account_type=config.account_type,
                base_url_ws=config.base_url_ws or default_base_url_ws,
                use_agg_trade_ticks=config.use_agg_trade_ticks,
            )


class CoinbaseLiveExecClientFactory(LiveExecClientFactory):
    """
    Provides a `Coinbase` live execution client factory.
    """

    @staticmethod
    def create(  # type: ignore
        loop: asyncio.AbstractEventLoop,
        name: str,
        config: CoinbaseExecClientConfig,
        msgbus: MessageBus,
        cache: Cache,
        clock: LiveClock,
        logger: Logger,
    ) -> Union[CoinbaseSpotExecutionClient, CoinbaseFuturesExecutionClient]:
        """
        Create a new Coinbase execution client.

        Parameters
        ----------
        loop : asyncio.AbstractEventLoop
            The event loop for the client.
        name : str
            The client name.
        config : CoinbaseExecClientConfig
            The configuration for the client.
        msgbus : MessageBus
            The message bus for the client.
        cache : Cache
            The cache for the client.
        clock : LiveClock
            The clock for the client.
        logger : Logger
            The logger for the client.

        Returns
        -------
        BinanceExecutionClient

        Raises
        ------
        ValueError
            If `config.account_type` is not a valid `BinanceAccountType`.

        """
        # Get HTTP client singleton
        client: CoinbaseHttpClient = get_cached_coinbase_http_client(
            loop=loop,
            clock=clock,
            logger=logger,
            account_type=config.account_type,
            key=config.api_key,
            secret=config.api_secret,
            base_url=config.base_url_http,
            is_testnet=config.testnet,
            is_us=config.us,
        )

        default_base_url_ws: str = _get_ws_base_url(
            account_type=config.account_type,
            is_testnet=config.testnet,
            is_us=config.us,
        )

        provider: Union[CoinbaseSpotInstrumentProvider, CoinbaseFuturesInstrumentProvider]
        if config.account_type.is_spot or config.account_type.is_margin:
            # Get instrument provider singleton
            provider = get_cached_coinbase_spot_instrument_provider(
                client=client,
                logger=logger,
                clock=clock,
                account_type=config.account_type,
                config=config.instrument_provider,
            )

            # Create client
            return CoinbaseSpotExecutionClient(
                loop=loop,
                client=client,
                msgbus=msgbus,
                cache=cache,
                clock=clock,
                logger=logger,
                instrument_provider=provider,
                account_type=config.account_type,
                base_url_ws=config.base_url_ws or default_base_url_ws,
                warn_gtd_to_gtc=config.warn_gtd_to_gtc,
            )
        else:
            # Get instrument provider singleton
            provider = get_cached_coinbase_futures_instrument_provider(
                client=client,
                logger=logger,
                clock=clock,
                account_type=config.account_type,
                config=config.instrument_provider,
            )

            # Create client
            return CoinbaseFuturesExecutionClient(
                loop=loop,
                client=client,
                msgbus=msgbus,
                cache=cache,
                clock=clock,
                logger=logger,
                instrument_provider=provider,
                account_type=config.account_type,
                base_url_ws=config.base_url_ws or default_base_url_ws,
                warn_gtd_to_gtc=config.warn_gtd_to_gtc,
            )


def _get_api_key(account_type: CoinbaseAccountType, is_testnet: bool) -> str:
    if is_testnet:
        if account_type.is_spot_or_margin:
            return os.environ["COINBASE_TESTNET_API_KEY"]
        else:
            return os.environ["COINBASE_FUTURES_TESTNET_API_KEY"]

    if account_type.is_spot_or_margin:
        return os.environ["COINBASE_API_KEY"]
    else:
        return os.environ["COINBASE_FUTURES_API_KEY"]


def _get_api_secret(account_type: CoinbaseAccountType, is_testnet: bool) -> str:
    if is_testnet:
        if account_type.is_spot_or_margin:
            return os.environ["COINBASE_TESTNET_API_SECRET"]
        else:
            return os.environ["COINBASE_FUTURES_TESTNET_API_SECRET"]

    if account_type.is_spot_or_margin:
        return os.environ["COINBASE_API_SECRET"]
    else:
        return os.environ["COINBASE_FUTURES_API_SECRET"]


def _get_http_base_url(account_type: CoinbaseAccountType, is_testnet: bool, is_us: bool) -> str:
    # Testnet base URLs
    if is_testnet:
        if account_type.is_spot_or_margin:
            return "https://testnet.binance.vision"
        elif account_type == CoinbaseAccountType.FUTURES_USDT:
            return "https://testnet.binancefuture.com"
        elif account_type == CoinbaseAccountType.FUTURES_COIN:
            return "https://testnet.binancefuture.com"
        else:
            raise RuntimeError(  # pragma: no cover (design-time error)
                f"invalid `BinanceAccountType`, was {account_type}",  # pragma: no cover
            )

    # Live base URLs
    top_level_domain: str = "us" if is_us else "com"
    if account_type.is_spot:
        return f"https://api.binance.{top_level_domain}"
    elif account_type.is_margin:
        return f"https://sapi.binance.{top_level_domain}"
    elif account_type == CoinbaseAccountType.FUTURES_USDT:
        return f"https://fapi.binance.{top_level_domain}"
    elif account_type == CoinbaseAccountType.FUTURES_COIN:
        return f"https://dapi.binance.{top_level_domain}"
    else:
        raise RuntimeError(  # pragma: no cover (design-time error)
            f"invalid `BinanceAccountType`, was {account_type}",  # pragma: no cover
        )


def _get_ws_base_url(account_type: CoinbaseAccountType, is_testnet: bool, is_us: bool) -> str:
    # Testnet base URLs
    if is_testnet:
        if account_type.is_spot_or_margin:
            return "wss://testnet.binance.vision"
        elif account_type == CoinbaseAccountType.FUTURES_USDT:
            return "wss://stream.binancefuture.com"
        elif account_type == CoinbaseAccountType.FUTURES_COIN:
            raise ValueError("no testnet for COIN-M futures")
        else:
            raise RuntimeError(  # pragma: no cover (design-time error)
                f"invalid `BinanceAccountType`, was {account_type}",  # pragma: no cover
            )

    # Live base URLs
    top_level_domain: str = "us" if is_us else "com"
    if account_type.is_spot_or_margin:
        return f"wss://stream.binance.{top_level_domain}:9443"
    elif account_type == CoinbaseAccountType.FUTURES_USDT:
        return f"wss://fstream.binance.{top_level_domain}"
    elif account_type == CoinbaseAccountType.FUTURES_COIN:
        return f"wss://dstream.binance.{top_level_domain}"
    else:
        raise RuntimeError(
            f"invalid `BinanceAccountType`, was {account_type}",
        )  # pragma: no cover (design-time error)  # noqa
