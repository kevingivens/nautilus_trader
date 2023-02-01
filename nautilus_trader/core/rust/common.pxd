# Warning, this file is autogenerated by cbindgen. Don't modify this manually. */

from cpython.object cimport PyObject
from libc.stdint cimport uint8_t, uint64_t, uintptr_t
from nautilus_trader.core.rust.core cimport UUID4_t

cdef extern from "../includes/common.h":

    cpdef enum ComponentState:
        PRE_INITIALIZED # = 0,
        READY # = 1,
        STARTING # = 2,
        RUNNING # = 3,
        STOPPING # = 4,
        STOPPED # = 5,
        RESUMING # = 6,
        RESETTING # = 7,
        DISPOSING # = 8,
        DISPOSED # = 9,
        DEGRADING # = 10,
        DEGRADED # = 11,
        FAULTING # = 12,
        FAULTED # = 13,

    cpdef enum ComponentTrigger:
        INITIALIZE # = 1,
        START # = 2,
        START_COMPLETED # = 3,
        STOP # = 4,
        STOP_COMPLETED # = 5,
        RESUME # = 6,
        RESUME_COMPLETED # = 7,
        RESET # = 8,
        RESET_COMPLETED # = 9,
        DISPOSE # = 10,
        DISPOSE_COMPLETED # = 11,
        DEGRADE # = 12,
        DEGRADE_COMPLETED # = 13,
        FAULT # = 14,
        FAULT_COMPLETED # = 15,

    cpdef enum LogColor:
        NORMAL # = 0,
        GREEN # = 1,
        BLUE # = 2,
        MAGENTA # = 3,
        CYAN # = 4,
        YELLOW # = 5,
        RED # = 6,

    cpdef enum LogLevel:
        DEBUG # = 10,
        INFO # = 20,
        WARNING # = 30,
        ERROR # = 40,
        CRITICAL # = 50,

    cdef struct Logger_t:
        pass

    cdef struct Rc_String:
        pass

    cdef struct TestClock:
        pass

    cdef struct CTestClock:
        TestClock *_0;

    # Represents a time event occurring at the event timestamp.
    cdef struct TimeEvent_t:
        # The event name.
        Rc_String *name;
        # The event ID.
        UUID4_t event_id;
        # The message category
        uint64_t ts_event;
        # The UNIX timestamp (nanoseconds) when the object was initialized.
        uint64_t ts_init;

    cdef struct Vec_TimeEvent:
        const TimeEvent_t *ptr;
        uintptr_t len;

    # Logger is not C FFI safe, so we box and pass it as an opaque pointer.
    # This works because Logger fields don't need to be accessed, only functions
    # are called.
    cdef struct CLogger:
        Logger_t *_0;

    CTestClock test_clock_new();

    void test_clock_free(CTestClock clock);

    void test_clock_set_time(CTestClock *clock, uint64_t to_time_ns);

    uint64_t test_clock_time_ns(const CTestClock *clock);

    PyObject *test_clock_timer_names(const CTestClock *clock);

    uintptr_t test_clock_timer_count(CTestClock *clock);

    # # Safety
    # - Assumes `name_ptr` is a valid C string pointer.
    void test_clock_set_time_alert_ns(CTestClock *clock,
                                      const char *name_ptr,
                                      uint64_t alert_time_ns);

    # # Safety
    # - Assumes `name_ptr` is a valid C string pointer.
    void test_clock_set_timer_ns(CTestClock *clock,
                                 const char *name_ptr,
                                 uint64_t interval_ns,
                                 uint64_t start_time_ns,
                                 uint64_t stop_time_ns);

    # # Safety
    # - Assumes `set_time` is a correct `uint8_t` of either 0 or 1.
    Vec_TimeEvent test_clock_advance_time(CTestClock *clock, uint64_t to_time_ns, uint8_t set_time);

    void vec_time_events_drop(Vec_TimeEvent v);

    # # Safety
    # - Assumes `name_ptr` is a valid C string pointer.
    uint64_t test_clock_next_time_ns(CTestClock *clock, const char *name_ptr);

    # # Safety
    # - Assumes `name_ptr` is a valid C string pointer.
    void test_clock_cancel_timer(CTestClock *clock, const char *name_ptr);

    void test_clock_cancel_timers(CTestClock *clock);

    const char *component_state_to_cstr(ComponentState value);

    # Returns an enum from a Python string.
    #
    # # Safety
    # - Assumes `ptr` is a valid C string pointer.
    ComponentState component_state_from_cstr(const char *ptr);

    const char *component_trigger_to_cstr(ComponentTrigger value);

    # Returns an enum from a Python string.
    #
    # # Safety
    # - Assumes `ptr` is a valid C string pointer.
    ComponentTrigger component_trigger_from_cstr(const char *ptr);

    const char *log_level_to_cstr(LogLevel value);

    # Returns an enum from a Python string.
    #
    # # Safety
    # - Assumes `ptr` is a valid C string pointer.
    LogLevel log_level_from_cstr(const char *ptr);

    const char *log_color_to_cstr(LogColor value);

    # Returns an enum from a Python string.
    #
    # # Safety
    # - Assumes `ptr` is a valid C string pointer.
    LogColor log_color_from_cstr(const char *ptr);

    # Creates a new logger.
    #
    # # Safety
    # - Assumes `trader_id_ptr` is a valid C string pointer.
    # - Assumes `machine_id_ptr` is a valid C string pointer.
    # - Assumes `instance_id_ptr` is a valid C string pointer.
    CLogger logger_new(const char *trader_id_ptr,
                       const char *machine_id_ptr,
                       const char *instance_id_ptr,
                       LogLevel level_stdout,
                       uint8_t is_bypassed);

    void logger_free(CLogger logger);

    void flush(CLogger *logger);

    const char *logger_get_trader_id_cstr(const CLogger *logger);

    const char *logger_get_machine_id_cstr(const CLogger *logger);

    UUID4_t logger_get_instance_id(const CLogger *logger);

    uint8_t logger_is_bypassed(const CLogger *logger);

    # Log a message.
    #
    # # Safety
    # - Assumes `component_ptr` is a valid C string pointer.
    # - Assumes `msg_ptr` is a valid C string pointer.
    void logger_log(CLogger *logger,
                    uint64_t timestamp_ns,
                    LogLevel level,
                    LogColor color,
                    const char *component_ptr,
                    const char *msg_ptr);

    # # Safety
    # - Assumes `name` is borrowed from a valid Python UTF-8 `str`.
    TimeEvent_t time_event_new(const char *name,
                               UUID4_t event_id,
                               uint64_t ts_event,
                               uint64_t ts_init);

    TimeEvent_t time_event_copy(const TimeEvent_t *event);

    void time_event_free(TimeEvent_t event);

    const char *time_event_name_cstr(const TimeEvent_t *event);
