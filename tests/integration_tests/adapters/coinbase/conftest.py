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

from nautilus_trader.adapters.coinbase.common.constants import COINBASE_VENUE
from nautilus_trader.adapters.coinbase.http.client import CoinbaseHttpClient
from nautilus_trader.common.component import LiveClock
from nautilus_trader.common.component import Logger
from nautilus_trader.model.identifiers import Venue


@pytest.fixture(scope="session")
def loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope="session")
def live_clock():
    return LiveClock()


@pytest.fixture(scope="session")
def live_logger():
    return Logger("TEST_LOGGER")


@pytest.fixture(scope="session")
def coinbase_http_client(loop, live_clock):
    client = CoinbaseHttpClient(
        clock=live_clock,
        key="SOME_COINBASE_API_KEY",
        secret="SOME_COINBASE_API_SECRET",
        base_url="https://api.coinbase.com/",
    )
    return client


@pytest.fixture()
def venue() -> Venue:
    raise COINBASE_VENUE


@pytest.fixture()
def data_client():
    pass


@pytest.fixture()
def exec_client():
    pass


@pytest.fixture()
def instrument():
    pass


@pytest.fixture()
def account_state():
    pass
