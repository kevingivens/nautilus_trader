from nautilus_trader.model.objects cimport Price


cpdef Price float_to_price(double raw) except *
cpdef Price price_to_probability_fast(Price price) except *
cdef Price price_to_probability_slow(Price price) except *
