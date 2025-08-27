from enum import Enum
from enum import IntEnum

class MachineErrorMessages(Enum):
    WRONG_STATUS_CODE = "Received status code is not to expected"
    WRONG_STATE_CODE = "Received state code is not to expected"
    INVALID_REQUESTED_STATE = "INVALID_REQUESTED_STATE_CHANGE"

class StateCode(IntEnum):
    INIT = 1            # 0001
    PREOP = 2           # 0010
    BOOTSTRAP = 3       # 0011
    SAFEOP = 4          # 0100
    OP = 8              # 1000
    INVALID_INIT = 17   # 0001 0001
    INVALID_PREOP = 18  # 0001 0010
    INVALID_SAFEOP = 20 # 0001 0100
    INVALID_OP = 24     # 0001 1000

class ControlCode(IntEnum):
    INIT = 1            # 0001
    PREOP = 2           # 0010
    BOOTSTRAP = 3       # 0011
    SAFEOP = 4          # 0100
    OP = 8              # 1000
    TEST_VALUE1 = 10    # 1010
    TEST_VALUE2 = 1000  # 0011 1110 1000
    RESET_ERRORS = 16   # 0001 0000

class StatusCode(IntEnum):
    NO_ERROR = 0x0000
    UNSPECIFIED_ERROR = 0x0001
    # INVALID_DEVICE_SETUP = 0x0003
    INVALID_REQUESTED_STATE_CHANGE = 0x0011
    UNKNOW_REQUEST_STATE = 0x0012
    BOOTSTRAP_NOT_SUPPORTED = 0x0013
    INVALID_CONFIGURTION = 0x0014
    MASTER_TIMEOUT = 0x002A

class RegisterNumber(IntEnum):
    STATE = 0x0102
    CONTROL = 0x0103
    STATUS = 0x0104