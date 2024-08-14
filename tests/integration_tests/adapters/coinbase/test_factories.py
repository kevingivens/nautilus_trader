# -------------------------------------------------------------------------------------------------
#  Copyright (C) 2015-2024 Nautech Systems Pty Ltd. All rights reserved.
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

import pytest

from nautilus_trader.adapters.coinbase.common.enums import CoinbaseAccountType
from nautilus_trader.adapters.coinbase.config import CoinbaseDataClientConfig
from nautilus_trader.adapters.coinbase.config import CoinbaseExecClientConfig
from nautilus_trader.adapters.coinbase.factories import CoinbaseLiveDataClientFactory
from nautilus_trader.adapters.coinbase.factories import CoinbaseLiveExecClientFactory
from nautilus_trader.adapters.coinbase.factories import _get_http_base_url
from nautilus_trader.adapters.coinbase.factories import _get_ws_base_url
from nautilus_trader.adapters.coinbase.data import CoinbaseDataClient
from nautilus_trader.adapters.coinbase.execution import CoinbaseExecutionClient
# from nautilus_trader.adapters.coinbase.spot.data import CoinbaseSpotDataClient
# from nautilus_trader.adapters.coinbase.spot.execution import CoinbaseSpotExecutionClient
from nautilus_trader.cache.cache import Cache
from nautilus_trader.common.component import LiveClock
from nautilus_trader.common.component import MessageBus
from nautilus_trader.test_kit.mocks.cache_database import MockCacheDatabase
from nautilus_trader.test_kit.stubs.identifiers import TestIdStubs


class TestCoinbaseFactories:
    def setup(self):
        # Fixture Setup
        self.loop = asyncio.get_event_loop()
        self.clock = LiveClock()
        self.trader_id = TestIdStubs.trader_id()
        self.strategy_id = TestIdStubs.strategy_id()
        self.account_id = TestIdStubs.account_id()

        self.msgbus = MessageBus(
            trader_id=self.trader_id,
            clock=self.clock,
        )

        self.cache_db = MockCacheDatabase()

        self.cache = Cache(
            database=self.cache_db,
        )

    @pytest.mark.parametrize(
        ("account_type", "is_testnet", "is_us", "expected"),
        [
            [
                CoinbaseAccountType.SPOT,
                False,
                False,
                "https://api.coinbase.com",
            ],
            [
                CoinbaseAccountType.MARGIN,
                False,
                False,
                "https://sapi.coinbase.com",
            ],
            [
                CoinbaseAccountType.ISOLATED_MARGIN,
                False,
                False,
                "https://sapi.coinbase.com",
            ],
            [
                CoinbaseAccountType.USDT_FUTURE,
                False,
                False,
                "https://fapi.coinbase.com",
            ],
            [
                CoinbaseAccountType.COIN_FUTURE,
                False,
                False,
                "https://dapi.coinbase.com",
            ],
            [
                CoinbaseAccountType.SPOT,
                False,
                True,
                "https://api.coinbase.us",
            ],
            [
                CoinbaseAccountType.MARGIN,
                False,
                True,
                "https://sapi.coinbase.us",
            ],
            [
                CoinbaseAccountType.ISOLATED_MARGIN,
                False,
                True,
                "https://sapi.coinbase.us",
            ],
            [
                CoinbaseAccountType.USDT_FUTURE,
                False,
                True,
                "https://fapi.coinbase.us",
            ],
            [
                CoinbaseAccountType.COIN_FUTURE,
                False,
                True,
                "https://dapi.coinbase.us",
            ],
            [
                CoinbaseAccountType.SPOT,
                True,
                False,
                "https://testnet.coinbase.vision",
            ],
            [
                CoinbaseAccountType.MARGIN,
                True,
                False,
                "https://testnet.coinbase.vision",
            ],
            [
                CoinbaseAccountType.ISOLATED_MARGIN,
                True,
                False,
                "https://testnet.coinbase.vision",
            ],
            [
                CoinbaseAccountType.USDT_FUTURE,
                True,
                False,
                "https://testnet.coinbasefuture.com",
            ],
        ],
    )
    def test_get_http_base_url(self, account_type, is_testnet, is_us, expected):
        # Arrange, Act
        base_url = _get_http_base_url(account_type, is_testnet, is_us)

        # Assert
        assert base_url == expected

    @pytest.mark.parametrize(
        ("account_type", "is_testnet", "is_us", "expected"),
        [
            [
                CoinbaseAccountType.SPOT,
                False,
                False,
                "wss://stream.coinbase.com:9443",
            ],
            [
                CoinbaseAccountType.MARGIN,
                False,
                False,
                "wss://stream.coinbase.com:9443",
            ],
            [
                CoinbaseAccountType.ISOLATED_MARGIN,
                False,
                False,
                "wss://stream.coinbase.com:9443",
            ],
            [
                CoinbaseAccountType.USDT_FUTURE,
                False,
                False,
                "wss://fstream.coinbase.com",
            ],
            [
                CoinbaseAccountType.COIN_FUTURE,
                False,
                False,
                "wss://dstream.coinbase.com",
            ],
            [
                CoinbaseAccountType.SPOT,
                False,
                True,
                "wss://stream.coinbase.us:9443",
            ],
            [
                CoinbaseAccountType.MARGIN,
                False,
                True,
                "wss://stream.coinbase.us:9443",
            ],
            [
                CoinbaseAccountType.ISOLATED_MARGIN,
                False,
                True,
                "wss://stream.coinbase.us:9443",
            ],
            [
                CoinbaseAccountType.USDT_FUTURE,
                False,
                True,
                "wss://fstream.coinbase.us",
            ],
            [
                CoinbaseAccountType.COIN_FUTURE,
                False,
                True,
                "wss://dstream.coinbase.us",
            ],
            [
                CoinbaseAccountType.SPOT,
                True,
                False,
                "wss://testnet.coinbase.vision",
            ],
            [
                CoinbaseAccountType.MARGIN,
                True,
                False,
                "wss://testnet.coinbase.vision",
            ],
            [
                CoinbaseAccountType.ISOLATED_MARGIN,
                True,
                False,
                "wss://testnet.coinbase.vision",
            ],
            [
                CoinbaseAccountType.USDT_FUTURE,
                True,
                False,
                "wss://stream.coinbasefuture.com",
            ],
        ],
    )
    def test_get_ws_base_url(self, account_type, is_testnet, is_us, expected):
        # Arrange, Act
        base_url = _get_ws_base_url(account_type, is_testnet, is_us)

        # Assert
        assert base_url == expected

    def test_create_coinbase_live_data_client(self, coinbase_http_client):
        # Arrange, Act
        data_client = CoinbaseLiveDataClientFactory.create(
            loop=self.loop,
            name="COINBASE",
            config=CoinbaseDataClientConfig(  # (S106 Possible hardcoded password)
                api_key="SOME_COINBASE_API_KEY",  # Do not remove or will fail in CI
                api_secret="SOME_COINBASE_API_SECRET",  # Do not remove or will fail in CI
                account_type=CoinbaseAccountType.SPOT,
            ),
            msgbus=self.msgbus,
            cache=self.cache,
            clock=self.clock,
        )

        assert isinstance(data_client, CoinbaseDataClient)


    def test_create_coinbase_exec_client(self, coinbase_http_client):
        # Arrange, Act
        exec_client = CoinbaseLiveExecClientFactory.create(
            loop=self.loop,
            name="COINBASE",
            config=CoinbaseExecClientConfig(  # (S106 Possible hardcoded password)
                api_key="SOME_COINBASE_API_KEY",  # Do not remove or will fail in CI
                api_secret="SOME_COINBASE_API_SECRET",  # Do not remove or will fail in CI
                account_type=CoinbaseAccountType.SPOT,
            ),
            msgbus=self.msgbus,
            cache=self.cache,
            clock=self.clock,
        )

        assert isinstance(exec_client, CoinbaseExecutionClient)
