import ctypes
from ctypes import c_uint32, c_char_p, c_float, c_uint16, c_bool
from nrf_ble_lib_model import *

# NOTE: the nrf_ble_library is highly hardware dependent, that the
#       helper class should be singleton design
# TODO: so far just load dll once in python import but still better design a class with singleton

# TODO: try catch here ensure dll load successfully, otherwise set instance to None prevent function calls
nrf_ble_lib = ctypes.CDLL("./bin/nrf_ble_library.dll", ctypes.RTLD_LOCAL)
# EXTERNC NRFBLEAPI uint32_t dongle_init(char* serial_port, uint32_t baud_rate);
nrf_ble_lib.dongle_init.argtypes = [c_char_p, c_uint32]
nrf_ble_lib.dongle_init.restype = c_uint32
# EXTERNC NRFBLEAPI uint32_t scan_start(float interval, float window, bool active, uint16_t timeout);
nrf_ble_lib.scan_start.argtypes = [c_float, c_float, c_bool, c_uint16]
nrf_ble_lib.scan_start.restype = c_uint32
# EXTERNC NRFBLEAPI uint32_t scan_stop();
nrf_ble_lib.scan_stop.argtypes = []
nrf_ble_lib.scan_stop.restype = c_uint32

print(f"ctypes load library {nrf_ble_lib}")

def dongle_init(args: NrfBleInitArgs):
    """ returns: NRF_STAUTS, 0=NRF_SUCCESS """
    # convert str to byte stream for the ctypes.c_char_p
    bstr = args.serial_port.encode("utf-8")
    # uint32_t to NRF_STATUS
    result = 0
    # call c export function
    result = nrf_ble_lib.dongle_init(bstr, args.baud_rate)
    print(f"call dongle init {result}")
    return result

def scan_start(args: NrfBleScanArgs):
    result = nrf_ble_lib.scan_start(args.interval, args.window, args.activated, args.timeout)
    print(f"call scan start {result}")
    return result

def scan_stop():
    result = nrf_ble_lib.scan_stop()
    print(f"call scan stop {result}")
    return result
