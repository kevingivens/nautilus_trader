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

import pytest

from nautilus_trader.adapters.coinbase.common.enums import CoinbaseAccountType
from nautilus_trader.adapters.coinbase.common.schemas.symbol import CoinbaseSymbol
from nautilus_trader.adapters.coinbase.common.schemas.symbol import CoinbaseSymbols


class TestCoinbaseCoreFunctions:
    def test_format_symbol(self):
        # Arrange
        symbol = "ethusdt-perp"

        # Act
        result = CoinbaseSymbol(symbol)

        # Assert
        assert result == "ETHUSDT"

    def test_convert_symbols_list_to_json_array(self):
        # Arrange
        symbols = ["BTCUSDT", "ETHUSDT-PERP", " XRDUSDT"]

        # Act
        result = CoinbaseSymbols(symbols)

        # Assert
        assert result == '["BTCUSDT","ETHUSDT","XRDUSDT"]'

    @pytest.mark.parametrize(
        ("account_type", "expected"),
        [
            [CoinbaseAccountType.SPOT, True],
            [CoinbaseAccountType.MARGIN, False],
            [CoinbaseAccountType.ISOLATED_MARGIN, False],
            [CoinbaseAccountType.USDT_FUTURE, False],
            [CoinbaseAccountType.COIN_FUTURE, False],
        ],
    )
    def test_coinbase_account_type_is_spot(self, account_type, expected):
        # Arrange, Act, Assert
        assert account_type.is_spot == expected

    @pytest.mark.parametrize(
        ("account_type", "expected"),
        [
            [CoinbaseAccountType.SPOT, False],
            [CoinbaseAccountType.MARGIN, True],
            [CoinbaseAccountType.ISOLATED_MARGIN, True],
            [CoinbaseAccountType.USDT_FUTURE, False],
            [CoinbaseAccountType.COIN_FUTURE, False],
        ],
    )
    def test_coinbase_account_type_is_margin(self, account_type, expected):
        # Arrange, Act, Assert
        assert account_type.is_margin == expected

    @pytest.mark.parametrize(
        ("account_type", "expected"),
        [
            [CoinbaseAccountType.SPOT, True],
            [CoinbaseAccountType.MARGIN, True],
            [CoinbaseAccountType.ISOLATED_MARGIN, True],
            [CoinbaseAccountType.USDT_FUTURE, False],
            [CoinbaseAccountType.COIN_FUTURE, False],
        ],
    )
    def test_coinbase_account_type_is_spot_or_margin(self, account_type, expected):
        # Arrange, Act, Assert
        assert account_type.is_spot_or_margin == expected

    @pytest.mark.parametrize(
        ("account_type", "expected"),
        [
            [CoinbaseAccountType.SPOT, False],
            [CoinbaseAccountType.MARGIN, False],
            [CoinbaseAccountType.ISOLATED_MARGIN, False],
            [CoinbaseAccountType.USDT_FUTURE, True],
            [CoinbaseAccountType.COIN_FUTURE, True],
        ],
    )
    def test_coinbase_account_type_is_futures(self, account_type, expected):
        # Arrange, Act, Assert
        assert account_type.is_futures == expected
