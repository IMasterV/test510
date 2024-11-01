from enum import Enum

class MachineErrorMessages(Enum):
    WRONG_STATUS_CODE = "Received status code is not to expected"
    WRONG_STATE_CODE = "Received state code is not to expected"
    INVALID_REQUESTED_STATE = "INVALID_REQUESTED_STATE_CHANGE"
