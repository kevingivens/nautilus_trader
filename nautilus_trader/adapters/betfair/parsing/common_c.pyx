
from nautilus_trader.adapters.betfair.common import BETFAIR_PRICE_PRECISION
from nautilus_trader.adapters.betfair.common import BETFAIR_QUANTITY_PRECISION

from libc.stdint cimport int64_t

from nautilus_trader.core.correctness cimport Condition
from nautilus_trader.model.enums_c cimport BookAction
from nautilus_trader.model.enums_c cimport BookType
from nautilus_trader.model.enums_c cimport OrderSide
from nautilus_trader.model.identifiers cimport InstrumentId
from nautilus_trader.model.objects cimport Price
from nautilus_trader.model.objects cimport Quantity
from nautilus_trader.model.orderbook.data cimport BookOrder
from nautilus_trader.model.orderbook.data cimport OrderBookDelta


PRICE_ONE = Price(1, BETFAIR_PRICE_PRECISION)
BETFAIR_BOOK_TYPE = BookType.L2_MBP

cpdef OrderBookDelta price_volume_to_order_book_delta(
        InstrumentId instrument_id, double price_f, double volume, OrderSide side, int64_t ts_event, int64_t ts_init,
):
    cdef:
        OrderBookDelta delta
        BookAction action
        BookOrder order = price_volume_to_book_order(price_f, volume, side)
    if volume == 0.0:
        action = BookAction.DELETE
    else:
        action = BookAction.UPDATE

    delta = OrderBookDelta(
        instrument_id=instrument_id,
        book_type=BETFAIR_BOOK_TYPE,
        action=action,
        order=order,
        ts_init=ts_init,
        ts_event=ts_event,
    )
    return delta

cdef BookOrder price_volume_to_book_order(double price_f, double volume, OrderSide side):
    cdef:
        Price price = float_to_price(price_f)
        Price prob = price_to_probability_fast(price)
        Quantity quantity = Quantity(volume, BETFAIR_QUANTITY_PRECISION)
        BookOrder order = BookOrder(prob, volume, side)


cpdef Price float_to_price(double raw) except *:
    cdef:
        Price price
    price = Price(raw, BETFAIR_PRICE_PRECISION)
    return price


cdef Price price_to_probability_slow(Price price) except *:
    """  This is likely a trade tick that has been currency adjusted, simply return the nearest price """
    cdef Price probability
    Condition.true(price.raw_int64_c() >= 0, "Price should be greater than 1.01")
    Condition.true(price.raw_int64_c() <= 1000000000000, "Price should be less than 1000")

    probability = Price(PRICE_ONE / price, BETFAIR_PRICE_PRECISION)
    return probability


cpdef Price price_to_probability_fast(Price price) except *:
    if price.raw_int64_c() == 1010000000:
        return Price.from_raw_c(990099000, 7)
    elif price.raw_int64_c() == 1020000000:
        return Price.from_raw_c(980392200, 7)
    elif price.raw_int64_c() == 1030000000:
        return Price.from_raw_c(970873800, 7)
    elif price.raw_int64_c() == 1040000000:
        return Price.from_raw_c(961538500, 7)
    elif price.raw_int64_c() == 1050000000:
        return Price.from_raw_c(952381000, 7)
    elif price.raw_int64_c() == 1060000000:
        return Price.from_raw_c(943396200, 7)
    elif price.raw_int64_c() == 1070000000:
        return Price.from_raw_c(934579400, 7)
    elif price.raw_int64_c() == 1080000000:
        return Price.from_raw_c(925925900, 7)
    elif price.raw_int64_c() == 1090000000:
        return Price.from_raw_c(917431200, 7)
    elif price.raw_int64_c() == 1100000000:
        return Price.from_raw_c(909090900, 7)
    elif price.raw_int64_c() == 1110000000:
        return Price.from_raw_c(900900900, 7)
    elif price.raw_int64_c() == 1120000000:
        return Price.from_raw_c(892857100, 7)
    elif price.raw_int64_c() == 1130000000:
        return Price.from_raw_c(884955800, 7)
    elif price.raw_int64_c() == 1140000000:
        return Price.from_raw_c(877193000, 7)
    elif price.raw_int64_c() == 1150000000:
        return Price.from_raw_c(869565200, 7)
    elif price.raw_int64_c() == 1160000000:
        return Price.from_raw_c(862069000, 7)
    elif price.raw_int64_c() == 1170000000:
        return Price.from_raw_c(854700900, 7)
    elif price.raw_int64_c() == 1180000000:
        return Price.from_raw_c(847457600, 7)
    elif price.raw_int64_c() == 1190000000:
        return Price.from_raw_c(840336100, 7)
    elif price.raw_int64_c() == 1200000000:
        return Price.from_raw_c(833333300, 7)
    elif price.raw_int64_c() == 1210000000:
        return Price.from_raw_c(826446300, 7)
    elif price.raw_int64_c() == 1220000000:
        return Price.from_raw_c(819672100, 7)
    elif price.raw_int64_c() == 1230000000:
        return Price.from_raw_c(813008100, 7)
    elif price.raw_int64_c() == 1240000000:
        return Price.from_raw_c(806451600, 7)
    elif price.raw_int64_c() == 1250000000:
        return Price.from_raw_c(800000000, 7)
    elif price.raw_int64_c() == 1260000000:
        return Price.from_raw_c(793650800, 7)
    elif price.raw_int64_c() == 1270000000:
        return Price.from_raw_c(787401600, 7)
    elif price.raw_int64_c() == 1280000000:
        return Price.from_raw_c(781250000, 7)
    elif price.raw_int64_c() == 1290000000:
        return Price.from_raw_c(775193800, 7)
    elif price.raw_int64_c() == 1300000000:
        return Price.from_raw_c(769230800, 7)
    elif price.raw_int64_c() == 1310000000:
        return Price.from_raw_c(763358800, 7)
    elif price.raw_int64_c() == 1320000000:
        return Price.from_raw_c(757575800, 7)
    elif price.raw_int64_c() == 1330000000:
        return Price.from_raw_c(751879700, 7)
    elif price.raw_int64_c() == 1340000000:
        return Price.from_raw_c(746268700, 7)
    elif price.raw_int64_c() == 1350000000:
        return Price.from_raw_c(740740700, 7)
    elif price.raw_int64_c() == 1360000000:
        return Price.from_raw_c(735294100, 7)
    elif price.raw_int64_c() == 1370000000:
        return Price.from_raw_c(729927000, 7)
    elif price.raw_int64_c() == 1380000000:
        return Price.from_raw_c(724637700, 7)
    elif price.raw_int64_c() == 1390000000:
        return Price.from_raw_c(719424500, 7)
    elif price.raw_int64_c() == 1400000000:
        return Price.from_raw_c(714285700, 7)
    elif price.raw_int64_c() == 1410000000:
        return Price.from_raw_c(709219900, 7)
    elif price.raw_int64_c() == 1420000000:
        return Price.from_raw_c(704225400, 7)
    elif price.raw_int64_c() == 1430000000:
        return Price.from_raw_c(699300700, 7)
    elif price.raw_int64_c() == 1440000000:
        return Price.from_raw_c(694444400, 7)
    elif price.raw_int64_c() == 1450000000:
        return Price.from_raw_c(689655200, 7)
    elif price.raw_int64_c() == 1460000000:
        return Price.from_raw_c(684931500, 7)
    elif price.raw_int64_c() == 1470000000:
        return Price.from_raw_c(680272100, 7)
    elif price.raw_int64_c() == 1480000000:
        return Price.from_raw_c(675675700, 7)
    elif price.raw_int64_c() == 1490000000:
        return Price.from_raw_c(671140900, 7)
    elif price.raw_int64_c() == 1500000000:
        return Price.from_raw_c(666666700, 7)
    elif price.raw_int64_c() == 1510000000:
        return Price.from_raw_c(662251700, 7)
    elif price.raw_int64_c() == 1520000000:
        return Price.from_raw_c(657894700, 7)
    elif price.raw_int64_c() == 1530000000:
        return Price.from_raw_c(653594800, 7)
    elif price.raw_int64_c() == 1540000000:
        return Price.from_raw_c(649350600, 7)
    elif price.raw_int64_c() == 1550000000:
        return Price.from_raw_c(645161300, 7)
    elif price.raw_int64_c() == 1560000000:
        return Price.from_raw_c(641025600, 7)
    elif price.raw_int64_c() == 1570000000:
        return Price.from_raw_c(636942700, 7)
    elif price.raw_int64_c() == 1580000000:
        return Price.from_raw_c(632911400, 7)
    elif price.raw_int64_c() == 1590000000:
        return Price.from_raw_c(628930800, 7)
    elif price.raw_int64_c() == 1600000000:
        return Price.from_raw_c(625000000, 7)
    elif price.raw_int64_c() == 1610000000:
        return Price.from_raw_c(621118000, 7)
    elif price.raw_int64_c() == 1620000000:
        return Price.from_raw_c(617284000, 7)
    elif price.raw_int64_c() == 1630000000:
        return Price.from_raw_c(613496900, 7)
    elif price.raw_int64_c() == 1640000000:
        return Price.from_raw_c(609756100, 7)
    elif price.raw_int64_c() == 1650000000:
        return Price.from_raw_c(606060600, 7)
    elif price.raw_int64_c() == 1660000000:
        return Price.from_raw_c(602409600, 7)
    elif price.raw_int64_c() == 1670000000:
        return Price.from_raw_c(598802400, 7)
    elif price.raw_int64_c() == 1680000000:
        return Price.from_raw_c(595238100, 7)
    elif price.raw_int64_c() == 1690000000:
        return Price.from_raw_c(591716000, 7)
    elif price.raw_int64_c() == 1700000000:
        return Price.from_raw_c(588235300, 7)
    elif price.raw_int64_c() == 1710000000:
        return Price.from_raw_c(584795300, 7)
    elif price.raw_int64_c() == 1720000000:
        return Price.from_raw_c(581395300, 7)
    elif price.raw_int64_c() == 1730000000:
        return Price.from_raw_c(578034700, 7)
    elif price.raw_int64_c() == 1740000000:
        return Price.from_raw_c(574712600, 7)
    elif price.raw_int64_c() == 1750000000:
        return Price.from_raw_c(571428600, 7)
    elif price.raw_int64_c() == 1760000000:
        return Price.from_raw_c(568181800, 7)
    elif price.raw_int64_c() == 1770000000:
        return Price.from_raw_c(564971800, 7)
    elif price.raw_int64_c() == 1780000000:
        return Price.from_raw_c(561797800, 7)
    elif price.raw_int64_c() == 1790000000:
        return Price.from_raw_c(558659200, 7)
    elif price.raw_int64_c() == 1800000000:
        return Price.from_raw_c(555555600, 7)
    elif price.raw_int64_c() == 1810000000:
        return Price.from_raw_c(552486200, 7)
    elif price.raw_int64_c() == 1820000000:
        return Price.from_raw_c(549450500, 7)
    elif price.raw_int64_c() == 1830000000:
        return Price.from_raw_c(546448100, 7)
    elif price.raw_int64_c() == 1840000000:
        return Price.from_raw_c(543478300, 7)
    elif price.raw_int64_c() == 1850000000:
        return Price.from_raw_c(540540500, 7)
    elif price.raw_int64_c() == 1860000000:
        return Price.from_raw_c(537634400, 7)
    elif price.raw_int64_c() == 1870000000:
        return Price.from_raw_c(534759400, 7)
    elif price.raw_int64_c() == 1880000000:
        return Price.from_raw_c(531914899, 7)
    elif price.raw_int64_c() == 1890000000:
        return Price.from_raw_c(529100500, 7)
    elif price.raw_int64_c() == 1900000000:
        return Price.from_raw_c(526315800, 7)
    elif price.raw_int64_c() == 1910000000:
        return Price.from_raw_c(523560200, 7)
    elif price.raw_int64_c() == 1920000000:
        return Price.from_raw_c(520833300, 7)
    elif price.raw_int64_c() == 1930000000:
        return Price.from_raw_c(518134699, 7)
    elif price.raw_int64_c() == 1940000000:
        return Price.from_raw_c(515463900, 7)
    elif price.raw_int64_c() == 1950000000:
        return Price.from_raw_c(512820500, 7)
    elif price.raw_int64_c() == 1960000000:
        return Price.from_raw_c(510204100, 7)
    elif price.raw_int64_c() == 1970000000:
        return Price.from_raw_c(507614200, 7)
    elif price.raw_int64_c() == 1980000000:
        return Price.from_raw_c(505050499, 7)
    elif price.raw_int64_c() == 1990000000:
        return Price.from_raw_c(502512600, 7)
    elif price.raw_int64_c() == 2000000000:
        return Price.from_raw_c(500000000, 7)
    elif price.raw_int64_c() == 2020000000:
        return Price.from_raw_c(495049500, 7)
    elif price.raw_int64_c() == 2040000000:
        return Price.from_raw_c(490196100, 7)
    elif price.raw_int64_c() == 2060000000:
        return Price.from_raw_c(485436900, 7)
    elif price.raw_int64_c() == 2080000000:
        return Price.from_raw_c(480769200, 7)
    elif price.raw_int64_c() == 2100000000:
        return Price.from_raw_c(476190500, 7)
    elif price.raw_int64_c() == 2120000000:
        return Price.from_raw_c(471698100, 7)
    elif price.raw_int64_c() == 2140000000:
        return Price.from_raw_c(467289700, 7)
    elif price.raw_int64_c() == 2160000000:
        return Price.from_raw_c(462963000, 7)
    elif price.raw_int64_c() == 2180000000:
        return Price.from_raw_c(458715600, 7)
    elif price.raw_int64_c() == 2200000000:
        return Price.from_raw_c(454545500, 7)
    elif price.raw_int64_c() == 2220000000:
        return Price.from_raw_c(450450500, 7)
    elif price.raw_int64_c() == 2240000000:
        return Price.from_raw_c(446428600, 7)
    elif price.raw_int64_c() == 2260000000:
        return Price.from_raw_c(442477900, 7)
    elif price.raw_int64_c() == 2280000000:
        return Price.from_raw_c(438596500, 7)
    elif price.raw_int64_c() == 2300000000:
        return Price.from_raw_c(434782600, 7)
    elif price.raw_int64_c() == 2320000000:
        return Price.from_raw_c(431034500, 7)
    elif price.raw_int64_c() == 2340000000:
        return Price.from_raw_c(427350400, 7)
    elif price.raw_int64_c() == 2360000000:
        return Price.from_raw_c(423728800, 7)
    elif price.raw_int64_c() == 2380000000:
        return Price.from_raw_c(420168100, 7)
    elif price.raw_int64_c() == 2400000000:
        return Price.from_raw_c(416666700, 7)
    elif price.raw_int64_c() == 2420000000:
        return Price.from_raw_c(413223100, 7)
    elif price.raw_int64_c() == 2440000000:
        return Price.from_raw_c(409836100, 7)
    elif price.raw_int64_c() == 2460000000:
        return Price.from_raw_c(406504100, 7)
    elif price.raw_int64_c() == 2480000000:
        return Price.from_raw_c(403225800, 7)
    elif price.raw_int64_c() == 2500000000:
        return Price.from_raw_c(400000000, 7)
    elif price.raw_int64_c() == 2520000000:
        return Price.from_raw_c(396825400, 7)
    elif price.raw_int64_c() == 2540000000:
        return Price.from_raw_c(393700800, 7)
    elif price.raw_int64_c() == 2560000000:
        return Price.from_raw_c(390625000, 7)
    elif price.raw_int64_c() == 2580000000:
        return Price.from_raw_c(387596900, 7)
    elif price.raw_int64_c() == 2600000000:
        return Price.from_raw_c(384615400, 7)
    elif price.raw_int64_c() == 2620000000:
        return Price.from_raw_c(381679400, 7)
    elif price.raw_int64_c() == 2640000000:
        return Price.from_raw_c(378787900, 7)
    elif price.raw_int64_c() == 2660000000:
        return Price.from_raw_c(375939800, 7)
    elif price.raw_int64_c() == 2680000000:
        return Price.from_raw_c(373134300, 7)
    elif price.raw_int64_c() == 2700000000:
        return Price.from_raw_c(370370400, 7)
    elif price.raw_int64_c() == 2720000000:
        return Price.from_raw_c(367647100, 7)
    elif price.raw_int64_c() == 2740000000:
        return Price.from_raw_c(364963500, 7)
    elif price.raw_int64_c() == 2760000000:
        return Price.from_raw_c(362318800, 7)
    elif price.raw_int64_c() == 2780000000:
        return Price.from_raw_c(359712200, 7)
    elif price.raw_int64_c() == 2800000000:
        return Price.from_raw_c(357142900, 7)
    elif price.raw_int64_c() == 2820000000:
        return Price.from_raw_c(354609900, 7)
    elif price.raw_int64_c() == 2840000000:
        return Price.from_raw_c(352112700, 7)
    elif price.raw_int64_c() == 2860000000:
        return Price.from_raw_c(349650300, 7)
    elif price.raw_int64_c() == 2880000000:
        return Price.from_raw_c(347222200, 7)
    elif price.raw_int64_c() == 2900000000:
        return Price.from_raw_c(344827600, 7)
    elif price.raw_int64_c() == 2920000000:
        return Price.from_raw_c(342465800, 7)
    elif price.raw_int64_c() == 2940000000:
        return Price.from_raw_c(340136100, 7)
    elif price.raw_int64_c() == 2960000000:
        return Price.from_raw_c(337837800, 7)
    elif price.raw_int64_c() == 2980000000:
        return Price.from_raw_c(335570500, 7)
    elif price.raw_int64_c() == 3000000000:
        return Price.from_raw_c(333333300, 7)
    elif price.raw_int64_c() == 3050000000:
        return Price.from_raw_c(327868900, 7)
    elif price.raw_int64_c() == 3100000000:
        return Price.from_raw_c(322580600, 7)
    elif price.raw_int64_c() == 3150000000:
        return Price.from_raw_c(317460300, 7)
    elif price.raw_int64_c() == 3200000000:
        return Price.from_raw_c(312500000, 7)
    elif price.raw_int64_c() == 3250000000:
        return Price.from_raw_c(307692300, 7)
    elif price.raw_int64_c() == 3300000000:
        return Price.from_raw_c(303030300, 7)
    elif price.raw_int64_c() == 3350000000:
        return Price.from_raw_c(298507500, 7)
    elif price.raw_int64_c() == 3400000000:
        return Price.from_raw_c(294117600, 7)
    elif price.raw_int64_c() == 3450000000:
        return Price.from_raw_c(289855100, 7)
    elif price.raw_int64_c() == 3500000000:
        return Price.from_raw_c(285714300, 7)
    elif price.raw_int64_c() == 3550000000:
        return Price.from_raw_c(281690100, 7)
    elif price.raw_int64_c() == 3600000000:
        return Price.from_raw_c(277777800, 7)
    elif price.raw_int64_c() == 3650000000:
        return Price.from_raw_c(273972600, 7)
    elif price.raw_int64_c() == 3700000000:
        return Price.from_raw_c(270270300, 7)
    elif price.raw_int64_c() == 3750000000:
        return Price.from_raw_c(266666699, 7)
    elif price.raw_int64_c() == 3800000000:
        return Price.from_raw_c(263157900, 7)
    elif price.raw_int64_c() == 3850000000:
        return Price.from_raw_c(259740299, 7)
    elif price.raw_int64_c() == 3900000000:
        return Price.from_raw_c(256410299, 7)
    elif price.raw_int64_c() == 3950000000:
        return Price.from_raw_c(253164600, 7)
    elif price.raw_int64_c() == 4000000000:
        return Price.from_raw_c(250000000, 7)
    elif price.raw_int64_c() == 4099999999:
        return Price.from_raw_c(243902400, 7)
    elif price.raw_int64_c() == 4200000000:
        return Price.from_raw_c(238095200, 7)
    elif price.raw_int64_c() == 4300000000:
        return Price.from_raw_c(232558100, 7)
    elif price.raw_int64_c() == 4400000000:
        return Price.from_raw_c(227272700, 7)
    elif price.raw_int64_c() == 4500000000:
        return Price.from_raw_c(222222200, 7)
    elif price.raw_int64_c() == 4600000000:
        return Price.from_raw_c(217391300, 7)
    elif price.raw_int64_c() == 4700000000:
        return Price.from_raw_c(212766000, 7)
    elif price.raw_int64_c() == 4800000000:
        return Price.from_raw_c(208333300, 7)
    elif price.raw_int64_c() == 4900000000:
        return Price.from_raw_c(204081600, 7)
    elif price.raw_int64_c() == 5000000000:
        return Price.from_raw_c(200000000, 7)
    elif price.raw_int64_c() == 5100000000:
        return Price.from_raw_c(196078400, 7)
    elif price.raw_int64_c() == 5200000000:
        return Price.from_raw_c(192307700, 7)
    elif price.raw_int64_c() == 5300000000:
        return Price.from_raw_c(188679200, 7)
    elif price.raw_int64_c() == 5400000000:
        return Price.from_raw_c(185185200, 7)
    elif price.raw_int64_c() == 5500000000:
        return Price.from_raw_c(181818200, 7)
    elif price.raw_int64_c() == 5600000000:
        return Price.from_raw_c(178571400, 7)
    elif price.raw_int64_c() == 5700000000:
        return Price.from_raw_c(175438600, 7)
    elif price.raw_int64_c() == 5800000000:
        return Price.from_raw_c(172413800, 7)
    elif price.raw_int64_c() == 5900000000:
        return Price.from_raw_c(169491500, 7)
    elif price.raw_int64_c() == 6000000000:
        return Price.from_raw_c(166666700, 7)
    elif price.raw_int64_c() == 6200000000:
        return Price.from_raw_c(161290300, 7)
    elif price.raw_int64_c() == 6400000000:
        return Price.from_raw_c(156250000, 7)
    elif price.raw_int64_c() == 6600000000:
        return Price.from_raw_c(151515200, 7)
    elif price.raw_int64_c() == 6800000000:
        return Price.from_raw_c(147058800, 7)
    elif price.raw_int64_c() == 7000000000:
        return Price.from_raw_c(142857100, 7)
    elif price.raw_int64_c() == 7200000000:
        return Price.from_raw_c(138888900, 7)
    elif price.raw_int64_c() == 7400000000:
        return Price.from_raw_c(135135100, 7)
    elif price.raw_int64_c() == 7600000000:
        return Price.from_raw_c(131578900, 7)
    elif price.raw_int64_c() == 7800000000:
        return Price.from_raw_c(128205099, 7)
    elif price.raw_int64_c() == 8000000000:
        return Price.from_raw_c(125000000, 7)
    elif price.raw_int64_c() == 8199999999:
        return Price.from_raw_c(121951200, 7)
    elif price.raw_int64_c() == 8400000000:
        return Price.from_raw_c(119047600, 7)
    elif price.raw_int64_c() == 8600000000:
        return Price.from_raw_c(116279100, 7)
    elif price.raw_int64_c() == 8800000000:
        return Price.from_raw_c(113636400, 7)
    elif price.raw_int64_c() == 9000000000:
        return Price.from_raw_c(111111100, 7)
    elif price.raw_int64_c() == 9200000000:
        return Price.from_raw_c(108695700, 7)
    elif price.raw_int64_c() == 9400000000:
        return Price.from_raw_c(106383000, 7)
    elif price.raw_int64_c() == 9600000000:
        return Price.from_raw_c(104166700, 7)
    elif price.raw_int64_c() == 9800000000:
        return Price.from_raw_c(102040800, 7)
    elif price.raw_int64_c() == 10000000000:
        return Price.from_raw_c(100000000, 7)
    elif price.raw_int64_c() == 10500000000:
        return Price.from_raw_c(95238100, 7)
    elif price.raw_int64_c() == 11000000000:
        return Price.from_raw_c(90909100, 7)
    elif price.raw_int64_c() == 11500000000:
        return Price.from_raw_c(86956500, 7)
    elif price.raw_int64_c() == 12000000000:
        return Price.from_raw_c(83333300, 7)
    elif price.raw_int64_c() == 12500000000:
        return Price.from_raw_c(80000000, 7)
    elif price.raw_int64_c() == 13000000000:
        return Price.from_raw_c(76923100, 7)
    elif price.raw_int64_c() == 13500000000:
        return Price.from_raw_c(74074100, 7)
    elif price.raw_int64_c() == 14000000000:
        return Price.from_raw_c(71428600, 7)
    elif price.raw_int64_c() == 14500000000:
        return Price.from_raw_c(68965500, 7)
    elif price.raw_int64_c() == 15000000000:
        return Price.from_raw_c(66666699, 7)
    elif price.raw_int64_c() == 15500000000:
        return Price.from_raw_c(64516100, 7)
    elif price.raw_int64_c() == 16000000000:
        return Price.from_raw_c(62500000, 7)
    elif price.raw_int64_c() == 16500000000:
        return Price.from_raw_c(60606100, 7)
    elif price.raw_int64_c() == 17000000000:
        return Price.from_raw_c(58823500, 7)
    elif price.raw_int64_c() == 17500000000:
        return Price.from_raw_c(57142900, 7)
    elif price.raw_int64_c() == 18000000000:
        return Price.from_raw_c(55555600, 7)
    elif price.raw_int64_c() == 18500000000:
        return Price.from_raw_c(54054100, 7)
    elif price.raw_int64_c() == 19000000000:
        return Price.from_raw_c(52631600, 7)
    elif price.raw_int64_c() == 19500000000:
        return Price.from_raw_c(51282100, 7)
    elif price.raw_int64_c() == 20000000000:
        return Price.from_raw_c(50000000, 7)
    elif price.raw_int64_c() == 21000000000:
        return Price.from_raw_c(47619000, 7)
    elif price.raw_int64_c() == 22000000000:
        return Price.from_raw_c(45454500, 7)
    elif price.raw_int64_c() == 23000000000:
        return Price.from_raw_c(43478300, 7)
    elif price.raw_int64_c() == 24000000000:
        return Price.from_raw_c(41666700, 7)
    elif price.raw_int64_c() == 25000000000:
        return Price.from_raw_c(40000000, 7)
    elif price.raw_int64_c() == 26000000000:
        return Price.from_raw_c(38461500, 7)
    elif price.raw_int64_c() == 27000000000:
        return Price.from_raw_c(37037000, 7)
    elif price.raw_int64_c() == 28000000000:
        return Price.from_raw_c(35714300, 7)
    elif price.raw_int64_c() == 29000000000:
        return Price.from_raw_c(34482800, 7)
    elif price.raw_int64_c() == 30000000000:
        return Price.from_raw_c(33333300, 7)
    elif price.raw_int64_c() == 32000000000:
        return Price.from_raw_c(31250000, 7)
    elif price.raw_int64_c() == 34000000000:
        return Price.from_raw_c(29411800, 7)
    elif price.raw_int64_c() == 36000000000:
        return Price.from_raw_c(27777800, 7)
    elif price.raw_int64_c() == 38000000000:
        return Price.from_raw_c(26315800, 7)
    elif price.raw_int64_c() == 40000000000:
        return Price.from_raw_c(25000000, 7)
    elif price.raw_int64_c() == 42000000000:
        return Price.from_raw_c(23809500, 7)
    elif price.raw_int64_c() == 44000000000:
        return Price.from_raw_c(22727300, 7)
    elif price.raw_int64_c() == 46000000000:
        return Price.from_raw_c(21739100, 7)
    elif price.raw_int64_c() == 48000000000:
        return Price.from_raw_c(20833300, 7)
    elif price.raw_int64_c() == 50000000000:
        return Price.from_raw_c(20000000, 7)
    elif price.raw_int64_c() == 55000000000:
        return Price.from_raw_c(18181800, 7)
    elif price.raw_int64_c() == 60000000000:
        return Price.from_raw_c(16666700, 7)
    elif price.raw_int64_c() == 65000000000:
        return Price.from_raw_c(15384600, 7)
    elif price.raw_int64_c() == 70000000000:
        return Price.from_raw_c(14285700, 7)
    elif price.raw_int64_c() == 75000000000:
        return Price.from_raw_c(13333300, 7)
    elif price.raw_int64_c() == 80000000000:
        return Price.from_raw_c(12500000, 7)
    elif price.raw_int64_c() == 85000000000:
        return Price.from_raw_c(11764700, 7)
    elif price.raw_int64_c() == 90000000000:
        return Price.from_raw_c(11111100, 7)
    elif price.raw_int64_c() == 95000000000:
        return Price.from_raw_c(10526300, 7)
    elif price.raw_int64_c() == 100000000000:
        return Price.from_raw_c(10000000, 7)
    elif price.raw_int64_c() == 110000000000:
        return Price.from_raw_c(9090900, 7)
    elif price.raw_int64_c() == 120000000000:
        return Price.from_raw_c(8333300, 7)
    elif price.raw_int64_c() == 130000000000:
        return Price.from_raw_c(7692300, 7)
    elif price.raw_int64_c() == 140000000000:
        return Price.from_raw_c(7142900, 7)
    elif price.raw_int64_c() == 150000000000:
        return Price.from_raw_c(6666700, 7)
    elif price.raw_int64_c() == 160000000000:
        return Price.from_raw_c(6250000, 7)
    elif price.raw_int64_c() == 170000000000:
        return Price.from_raw_c(5882400, 7)
    elif price.raw_int64_c() == 180000000000:
        return Price.from_raw_c(5555600, 7)
    elif price.raw_int64_c() == 190000000000:
        return Price.from_raw_c(5263200, 7)
    elif price.raw_int64_c() == 200000000000:
        return Price.from_raw_c(5000000, 7)
    elif price.raw_int64_c() == 210000000000:
        return Price.from_raw_c(4761900, 7)
    elif price.raw_int64_c() == 220000000000:
        return Price.from_raw_c(4545500, 7)
    elif price.raw_int64_c() == 230000000000:
        return Price.from_raw_c(4347800, 7)
    elif price.raw_int64_c() == 240000000000:
        return Price.from_raw_c(4166699, 7)
    elif price.raw_int64_c() == 250000000000:
        return Price.from_raw_c(4000000, 7)
    elif price.raw_int64_c() == 260000000000:
        return Price.from_raw_c(3846200, 7)
    elif price.raw_int64_c() == 270000000000:
        return Price.from_raw_c(3703700, 7)
    elif price.raw_int64_c() == 280000000000:
        return Price.from_raw_c(3571400, 7)
    elif price.raw_int64_c() == 290000000000:
        return Price.from_raw_c(3448300, 7)
    elif price.raw_int64_c() == 300000000000:
        return Price.from_raw_c(3333300, 7)
    elif price.raw_int64_c() == 310000000000:
        return Price.from_raw_c(3225800, 7)
    elif price.raw_int64_c() == 320000000000:
        return Price.from_raw_c(3125000, 7)
    elif price.raw_int64_c() == 330000000000:
        return Price.from_raw_c(3030300, 7)
    elif price.raw_int64_c() == 340000000000:
        return Price.from_raw_c(2941200, 7)
    elif price.raw_int64_c() == 350000000000:
        return Price.from_raw_c(2857100, 7)
    elif price.raw_int64_c() == 360000000000:
        return Price.from_raw_c(2777800, 7)
    elif price.raw_int64_c() == 370000000000:
        return Price.from_raw_c(2702700, 7)
    elif price.raw_int64_c() == 380000000000:
        return Price.from_raw_c(2631600, 7)
    elif price.raw_int64_c() == 390000000000:
        return Price.from_raw_c(2564100, 7)
    elif price.raw_int64_c() == 400000000000:
        return Price.from_raw_c(2500000, 7)
    elif price.raw_int64_c() == 410000000000:
        return Price.from_raw_c(2439000, 7)
    elif price.raw_int64_c() == 420000000000:
        return Price.from_raw_c(2381000, 7)
    elif price.raw_int64_c() == 430000000000:
        return Price.from_raw_c(2325600, 7)
    elif price.raw_int64_c() == 440000000000:
        return Price.from_raw_c(2272700, 7)
    elif price.raw_int64_c() == 450000000000:
        return Price.from_raw_c(2222200, 7)
    elif price.raw_int64_c() == 460000000000:
        return Price.from_raw_c(2173900, 7)
    elif price.raw_int64_c() == 470000000000:
        return Price.from_raw_c(2127700, 7)
    elif price.raw_int64_c() == 480000000000:
        return Price.from_raw_c(2083300, 7)
    elif price.raw_int64_c() == 490000000000:
        return Price.from_raw_c(2040800, 7)
    elif price.raw_int64_c() == 500000000000:
        return Price.from_raw_c(2000000, 7)
    elif price.raw_int64_c() == 510000000000:
        return Price.from_raw_c(1960800, 7)
    elif price.raw_int64_c() == 520000000000:
        return Price.from_raw_c(1923100, 7)
    elif price.raw_int64_c() == 530000000000:
        return Price.from_raw_c(1886800, 7)
    elif price.raw_int64_c() == 540000000000:
        return Price.from_raw_c(1851900, 7)
    elif price.raw_int64_c() == 550000000000:
        return Price.from_raw_c(1818200, 7)
    elif price.raw_int64_c() == 560000000000:
        return Price.from_raw_c(1785700, 7)
    elif price.raw_int64_c() == 570000000000:
        return Price.from_raw_c(1754400, 7)
    elif price.raw_int64_c() == 580000000000:
        return Price.from_raw_c(1724100, 7)
    elif price.raw_int64_c() == 590000000000:
        return Price.from_raw_c(1694900, 7)
    elif price.raw_int64_c() == 600000000000:
        return Price.from_raw_c(1666700, 7)
    elif price.raw_int64_c() == 610000000000:
        return Price.from_raw_c(1639300, 7)
    elif price.raw_int64_c() == 620000000000:
        return Price.from_raw_c(1612900, 7)
    elif price.raw_int64_c() == 630000000000:
        return Price.from_raw_c(1587300, 7)
    elif price.raw_int64_c() == 640000000000:
        return Price.from_raw_c(1562500, 7)
    elif price.raw_int64_c() == 650000000000:
        return Price.from_raw_c(1538500, 7)
    elif price.raw_int64_c() == 660000000000:
        return Price.from_raw_c(1515200, 7)
    elif price.raw_int64_c() == 670000000000:
        return Price.from_raw_c(1492500, 7)
    elif price.raw_int64_c() == 680000000000:
        return Price.from_raw_c(1470600, 7)
    elif price.raw_int64_c() == 690000000000:
        return Price.from_raw_c(1449300, 7)
    elif price.raw_int64_c() == 700000000000:
        return Price.from_raw_c(1428600, 7)
    elif price.raw_int64_c() == 710000000000:
        return Price.from_raw_c(1408500, 7)
    elif price.raw_int64_c() == 720000000000:
        return Price.from_raw_c(1388900, 7)
    elif price.raw_int64_c() == 730000000000:
        return Price.from_raw_c(1369900, 7)
    elif price.raw_int64_c() == 740000000000:
        return Price.from_raw_c(1351400, 7)
    elif price.raw_int64_c() == 750000000000:
        return Price.from_raw_c(1333300, 7)
    elif price.raw_int64_c() == 760000000000:
        return Price.from_raw_c(1315800, 7)
    elif price.raw_int64_c() == 770000000000:
        return Price.from_raw_c(1298700, 7)
    elif price.raw_int64_c() == 780000000000:
        return Price.from_raw_c(1282100, 7)
    elif price.raw_int64_c() == 790000000000:
        return Price.from_raw_c(1265800, 7)
    elif price.raw_int64_c() == 800000000000:
        return Price.from_raw_c(1250000, 7)
    elif price.raw_int64_c() == 810000000000:
        return Price.from_raw_c(1234600, 7)
    elif price.raw_int64_c() == 820000000000:
        return Price.from_raw_c(1219500, 7)
    elif price.raw_int64_c() == 830000000000:
        return Price.from_raw_c(1204800, 7)
    elif price.raw_int64_c() == 840000000000:
        return Price.from_raw_c(1190500, 7)
    elif price.raw_int64_c() == 850000000000:
        return Price.from_raw_c(1176500, 7)
    elif price.raw_int64_c() == 860000000000:
        return Price.from_raw_c(1162800, 7)
    elif price.raw_int64_c() == 870000000000:
        return Price.from_raw_c(1149400, 7)
    elif price.raw_int64_c() == 880000000000:
        return Price.from_raw_c(1136400, 7)
    elif price.raw_int64_c() == 890000000000:
        return Price.from_raw_c(1123600, 7)
    elif price.raw_int64_c() == 900000000000:
        return Price.from_raw_c(1111100, 7)
    elif price.raw_int64_c() == 910000000000:
        return Price.from_raw_c(1098900, 7)
    elif price.raw_int64_c() == 920000000000:
        return Price.from_raw_c(1087000, 7)
    elif price.raw_int64_c() == 930000000000:
        return Price.from_raw_c(1075300, 7)
    elif price.raw_int64_c() == 940000000000:
        return Price.from_raw_c(1063800, 7)
    elif price.raw_int64_c() == 950000000000:
        return Price.from_raw_c(1052600, 7)
    elif price.raw_int64_c() == 960000000000:
        return Price.from_raw_c(1041700, 7)
    elif price.raw_int64_c() == 970000000000:
        return Price.from_raw_c(1030900, 7)
    elif price.raw_int64_c() == 980000000000:
        return Price.from_raw_c(1020400, 7)
    elif price.raw_int64_c() == 990000000000:
        return Price.from_raw_c(1010100, 7)
    elif price.raw_int64_c() == 1000000000000:
        return Price.from_raw_c(1000000, 7)
    else:
        return price_to_probability_slow(price)
