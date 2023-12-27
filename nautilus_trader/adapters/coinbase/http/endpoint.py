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

from typing import Any

import msgspec

from nautilus_trader.adapters.coinbase.enums import CoinbaseMethodType
from nautilus_trader.adapters.coinbase.enums import CoinbaseSecurityType
from nautilus_trader.adapters.coinbase.schemas.symbol import CoinbaseSymbol
from nautilus_trader.adapters.coinbase.schemas.symbol import CoinbaseSymbols
from nautilus_trader.adapters.coinbase.http.client import CoinbaseHttpClient


def enc_hook(obj: Any) -> Any:
    if isinstance(obj, CoinbaseSymbol):
        return str(obj)  # serialize CoinbaseSymbol as string.
    elif isinstance(obj, CoinbaseSymbols):
        return str(obj)  # serialize CoinbaseSymbol as string.
    else:
        raise TypeError(f"Objects of type {type(obj)} are not supported")


class CoinbaseHttpEndpoint:
    """
    Base functionality of endpoints connecting to the Coinbase REST API.

    Warnings
    --------
    This class should not be used directly, but through a concrete subclass.
    """

    def __init__(
        self,
        client: CoinbaseHttpClient,
        methods_desc: dict[CoinbaseMethodType, CoinbaseSecurityType],
        url_path: str,
    ):
        self.client = client
        self.methods_desc = methods_desc
        self.url_path = url_path

        self.decoder = msgspec.json.Decoder()
        self.encoder = msgspec.json.Encoder(enc_hook=enc_hook)

        self._method_request = {
            CoinbaseSecurityType.NONE: self.client.send_request,
            CoinbaseSecurityType.USER_STREAM: self.client.send_request,
            CoinbaseSecurityType.MARKET_DATA: self.client.send_request,
            CoinbaseSecurityType.TRADE: self.client.sign_request,
            CoinbaseSecurityType.MARGIN: self.client.sign_request,
            CoinbaseSecurityType.USER_DATA: self.client.sign_request,
        }

    async def _method(self, method_type: CoinbaseMethodType, parameters: Any) -> bytes:
        payload: dict = self.decoder.decode(self.encoder.encode(parameters))
        if self.methods_desc[method_type] is None:
            raise RuntimeError(
                f"{method_type.name} not available for {self.url_path}",
            )
        raw: bytes = await self._method_request[self.methods_desc[method_type]](
            http_method=method_type.name,
            url_path=self.url_path,
            payload=payload,
        )
        return raw
