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

import json
from typing import Optional

from nautilus_trader.adapters.coinbase.common.enums import CoinbaseAccountType


################################################################################
# HTTP responses
################################################################################


class CoinbaseSymbol(str):
    """Coinbase compatible symbol."""

    def __new__(cls, symbol: Optional[str]):
        if symbol is not None:
            # Format the string on construction to be Binance compatible
            return super().__new__(
                cls,
                symbol.upper().replace(" ", "").replace("/", "").replace("-PERP", ""),
            )

    def parse_coinbase_to_internal(self, account_type: CoinbaseAccountType) -> str:
        if account_type.is_spot_or_margin:
            return str(self)

        # Parse Futures symbol
        if self[-1].isdigit():
            return str(self)  # Deliverable
        if self.endswith("_PERP"):
            return str(self).replace("_", "-")
        else:
            return str(self) + "-PERP"


class CoinbaseSymbols(str):
    """Coinbase compatible list of symbols."""

    def __new__(cls, symbols: Optional[list[str]]):
        if symbols is not None:
            coinbase_symbols: list[CoinbaseSymbol] = [CoinbaseSymbol(symbol) for symbol in symbols]
            return super().__new__(cls, json.dumps(coinbase_symbols).replace(" ", ""))

    def parse_str_to_list(self) -> list[CoinbaseSymbol]:
        binance_symbols: list[CoinbaseSymbol] = json.loads(self)
        return binance_symbols
