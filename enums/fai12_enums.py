from enum import IntEnum

class InputMode(IntEnum):
    DISABLE = 0
    VOLTAGE01 = 1
    VOLTAGE010 = 2
    CURRENT05 = 3
    CURRENT020 = 4
    CURRENT420 = 5

class TypeFilter(IntEnum):
    ONE = 0
    TWO = 1
    THREE = 2
    FOUR = 3
    FIVE = 4


class TypeBreakage(IntEnum):
    DISABLE = 0
    SERVICE = 1
    CYCLE = 2

class Status(IntEnum):
    NO_ERRORS = 0
    DATA_NOT_READY = 6
    SENSOR_OFF = 7
    VALUE_TOO_HIGH = 10
    VALUE_TOO_LOW = 11
    SHORT_CIRCUIT = 12
    BREAK = 13
    HARDWARE_ERROR = 14
    CALIBRATION_ERROR = 15






# class Fai12Regs(IntEnum):
#     FILTER_TYPE = 0x1000
#     TYPE_BREAKAGE = 0x1001
#
#     VALUE1 = 0x1002
#     STATUS1 = 0x1004
#     TIMESTAMP1 = 0x1005
#     INPUT_MODE1 = 0x1006
#
#     # VALUE5 = 0x101C
#     # STATUS5 = 0x101E
#     # TIMESTAMP5 = 0x101F
#     # INPUT_MODE5 = 0x1020
#     #
#     # VALUE9 = 0x1036
#     # STATUS9 = 0x1038
#     # TIMESTAMP9 = 0x1039
#     # INPUT_MODE9 = 0x103A
#
# class MapperFai12(IntEnum):
#     FILTER_TYPE = 0xFF00
#     TYPE_BREAKAGE = 0xFF01
#
#     VALUE1 = 0xFF02
#     STATUS1 = 0xFF04
#     TIMESTAMP1 = 0xFF05
#     INPUT_MODE1 = 0xFF06
#
#     # VALUE5 = 0xFF07
#     # STATUS5 = 0xFF09
#     # TIMESTAMP5 = 0xFF0A
#     # INPUT_MODE5 = 0xFF0B
#     #
#     # VALUE9 = 0xFF0C
#     # STATUS9 = 0xFF0E
#     # TIMESTAMP9 = 0xFF0F
#     # INPUT_MODE9 = 0xFF10