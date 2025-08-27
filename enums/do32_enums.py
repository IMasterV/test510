from enum import IntEnum

class OutMode(IntEnum):
    LOGICAL = 0
    PWM_SLOW = 1
    PWM_FAST = 2
    IMP_GEN = 3