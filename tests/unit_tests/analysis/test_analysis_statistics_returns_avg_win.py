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

import pandas as pd
from numpy import float64

from nautilus_trader.analysis.statistics.returns_avg_win import ReturnsAverageWin


class TestReturnsAverageWinPortfolioStatistic:
    def test_name_returns_expected_returns_expected(self):
        # Arrange
        stat = ReturnsAverageWin()

        # Act
        result = stat.name

        # Assert
        assert result == "Average Win (Return)"

    def test_calculate_given_empty_series_returns_nan(self):
        # Arrange
        stat = ReturnsAverageWin()
        data = pd.Series([], dtype=float64)

        # Act
        result = stat.calculate_from_returns(data)

        # Assert
        assert pd.isna(result)

    def test_calculate_given_mix_of_pnls1_returns_expected(self):
        # Arrange
        stat = ReturnsAverageWin()
        data = pd.Series([1.0, -1.0], dtype=float64)

        # Act
        result = stat.calculate_from_returns(data)

        # Assert
        assert result == 1.0

    def test_calculate_given_mix_of_pnls2_returns_expected(self):
        # Arrange
        stat = ReturnsAverageWin()
        data = pd.Series([2.0, 2.0, 1.0, -1.0, -2.0], dtype=float64)

        # Act
        result = stat.calculate_from_returns(data)

        # Assert
        assert result == 1.6666666666666667
