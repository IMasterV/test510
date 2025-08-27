from dataclasses import dataclass, asdict, field
from typing import Any, Optional

@dataclass
class ModbusField:
    addr: int
    count: int
    value: Optional[Any] = None

@dataclass
class System:
    name = ModbusField(addr=0x0000, count=16)
    firmware_ver = ModbusField(addr=0x0010, count=8)
    hardware_ver = ModbusField(addr=0x0018, count=8)
    module_position = ModbusField(addr=0x0020, count=8)
    system_time = ModbusField(addr=0x0030, count=2) #count = 2?
    fsm_current_state = ModbusField(addr=0x0102, count=1)
    fsm_control_state = ModbusField(addr=0x0103, count=1)
    fsm_status = ModbusField(addr=0x0104, count=1)
    so_timeout = ModbusField(addr=0x0110, count=1)
    restart = ModbusField(addr=0x0180, count=1)

@dataclass
class DOutput13:
    out_mode: ModbusField
    pwm_period: ModbusField
    pwm_duty: ModbusField
    hs_pwm_freq: ModbusField
    impgen_freq: ModbusField
    impgen_num: ModbusField
    impgen_count_out: ModbusField

    def __post_init__(self):
        if self.out_mode.value is not None and not (0 <= self.out_mode.value <= 3):
            raise ValueError(f'mode должен быть в диапазоне 0–3, а не {self.out_mode.value}')

@dataclass
class DOutput48:
    out_mode: ModbusField
    pwm_period: ModbusField
    pwm_duty: ModbusField
    hs_pwm_freq: ModbusField

    def __post_init__(self):
        if self.out_mode.value is not None and not (0 <= self.out_mode.value <= 3):
            raise ValueError(f'mode должен быть в диапазоне 0–3, а не {self.out_mode.value}')

@dataclass
class DOutput932:
    out_mode: ModbusField
    pwm_period: ModbusField
    pwm_duty: ModbusField

    def __post_init__(self):
        if self.out_mode.value is not None and not (0 <= self.out_mode.value <= 3):
            raise ValueError(f'mode должен быть в диапазоне 0–3, а не {self.out_mode.value}')

@dataclass
class DOutput:
    outputs_states: ModbusField
    out_mask: ModbusField
    power_mask: ModbusField

@dataclass
class Do32:
    do: DOutput = field(default_factory=lambda: DOutput(outputs_states=ModbusField(addr=0x1000, count=2),
                                                        out_mask=ModbusField(addr=0x1002, count=2),
                                                        power_mask=ModbusField(addr=0x10E4, count=1)
                                                        ))

    do1: DOutput13 = field(default_factory=lambda: DOutput13(out_mode=ModbusField(addr=0x1004, count=1),
                                                             pwm_period=ModbusField(addr=0x1005, count=1),
                                                             pwm_duty=ModbusField(addr=0x1006, count=1),
                                                             hs_pwm_freq=ModbusField(addr=0x1007, count=1),
                                                             impgen_freq=ModbusField(addr=0x1008, count=1),
                                                             impgen_num=ModbusField(addr=0x1009, count=1),
                                                             impgen_count_out=ModbusField(addr=0x100A, count=1)
                                                             ))

    do2: DOutput13 = field(default_factory=lambda: DOutput13(out_mode=ModbusField(addr=0x100B, count=1),
                                                             pwm_period=ModbusField(addr=0x100C, count=1),
                                                             pwm_duty=ModbusField(addr=0x100D, count=1),
                                                             hs_pwm_freq=ModbusField(addr=0x100E, count=1),
                                                             impgen_freq=ModbusField(addr=0x100F, count=1),
                                                             impgen_num=ModbusField(addr=0x1010, count=1),
                                                             impgen_count_out=ModbusField(addr=0x1011, count=1)
                                                             ))

    do3: DOutput13 = field(default_factory=lambda: DOutput13(out_mode=ModbusField(addr=0x1012, count=1),
                                                             pwm_period=ModbusField(addr=0x1013, count=1),
                                                             pwm_duty=ModbusField(addr=0x1014, count=1),
                                                             hs_pwm_freq=ModbusField(addr=0x1015, count=1),
                                                             impgen_freq=ModbusField(addr=0x1016, count=1),
                                                             impgen_num=ModbusField(addr=0x1017, count=1),
                                                             impgen_count_out=ModbusField(addr=0x1018, count=1)
                                                             ))

    do4: DOutput48 = field(default_factory=lambda: DOutput48(out_mode=ModbusField(addr=0x1019, count=1),
                                                             pwm_period=ModbusField(addr=0x101A, count=1),
                                                             pwm_duty=ModbusField(addr=0x101B, count=1),
                                                             hs_pwm_freq=ModbusField(addr=0x101C, count=1)
                                                             ))

    do5: DOutput48 = field(default_factory=lambda: DOutput48(out_mode=ModbusField(addr=0x1020, count=1),
                                                             pwm_period=ModbusField(addr=0x1021, count=1),
                                                             pwm_duty=ModbusField(addr=0x1022, count=1),
                                                             hs_pwm_freq=ModbusField(addr=0x1023, count=1)
                                                             ))

    do6: DOutput48 = field(default_factory=lambda: DOutput48(out_mode=ModbusField(addr=0x1027, count=1),
                                                             pwm_period=ModbusField(addr=0x1028, count=1),
                                                             pwm_duty=ModbusField(addr=0x1029, count=1),
                                                             hs_pwm_freq=ModbusField(addr=0x102A, count=1)
                                                             ))

    do7: DOutput48 = field(default_factory=lambda: DOutput48(out_mode=ModbusField(addr=0x102E, count=1),
                                                             pwm_period=ModbusField(addr=0x102F, count=1),
                                                             pwm_duty=ModbusField(addr=0x1030, count=1),
                                                             hs_pwm_freq=ModbusField(addr=0x1031, count=1)
                                                             ))

    do8: DOutput48 = field(default_factory=lambda: DOutput48(out_mode=ModbusField(addr=0x1035, count=1),
                                                             pwm_period=ModbusField(addr=0x1036, count=1),
                                                             pwm_duty=ModbusField(addr=0x1037, count=1),
                                                             hs_pwm_freq=ModbusField(addr=0x1038, count=1)
                                                             ))

    do9: DOutput48 = field(default_factory=lambda: DOutput932(out_mode=ModbusField(addr=0x103C, count=1),
                                                              pwm_period=ModbusField(addr=0x103D, count=1),
                                                              pwm_duty=ModbusField(addr=0x103E, count=1)
                                                              ))

    do10: DOutput48 = field(default_factory=lambda: DOutput932(out_mode=ModbusField(addr=0x1043, count=1),
                                                               pwm_period=ModbusField(addr=0x1044, count=1),
                                                               pwm_duty=ModbusField(addr=0x1045, count=1)
                                                               ))

    do11: DOutput48 = field(default_factory=lambda: DOutput932(out_mode=ModbusField(addr=0x104A, count=1),
                                                               pwm_period=ModbusField(addr=0x104B, count=1),
                                                               pwm_duty=ModbusField(addr=0x104C, count=1)
                                                               ))

    do12: DOutput48 = field(default_factory=lambda: DOutput932(out_mode=ModbusField(addr=0x1051, count=1),
                                                               pwm_period=ModbusField(addr=0x1052, count=1),
                                                               pwm_duty=ModbusField(addr=0x1053, count=1)
                                                               ))

    do13: DOutput48 = field(default_factory=lambda: DOutput932(out_mode=ModbusField(addr=0x1058, count=1),
                                                               pwm_period=ModbusField(addr=0x1059, count=1),
                                                               pwm_duty=ModbusField(addr=0x105A, count=1)
                                                               ))

    do14: DOutput48 = field(default_factory=lambda: DOutput932(out_mode=ModbusField(addr=0x105F, count=1),
                                                               pwm_period=ModbusField(addr=0x1060, count=1),
                                                               pwm_duty=ModbusField(addr=0x1061, count=1)
                                                               ))

    do15: DOutput48 = field(default_factory=lambda: DOutput932(out_mode=ModbusField(addr=0x1066, count=1),
                                                               pwm_period=ModbusField(addr=0x1067, count=1),
                                                               pwm_duty=ModbusField(addr=0x1068, count=1)
                                                               ))

    do16: DOutput48 = field(default_factory=lambda: DOutput932(out_mode=ModbusField(addr=0x106D, count=1),
                                                               pwm_period=ModbusField(addr=0x106E, count=1),
                                                               pwm_duty=ModbusField(addr=0x106F, count=1)
                                                               ))

    do17: DOutput48 = field(default_factory=lambda: DOutput932(out_mode=ModbusField(addr=0x1074, count=1),
                                                               pwm_period=ModbusField(addr=0x1075, count=1),
                                                               pwm_duty=ModbusField(addr=0x1076, count=1)
                                                               ))

    do18: DOutput48 = field(default_factory=lambda: DOutput932(out_mode=ModbusField(addr=0x107B, count=1),
                                                               pwm_period=ModbusField(addr=0x107C, count=1),
                                                               pwm_duty=ModbusField(addr=0x107D, count=1)
                                                               ))

    do19: DOutput48 = field(default_factory=lambda: DOutput932(out_mode=ModbusField(addr=0x1082, count=1),
                                                               pwm_period=ModbusField(addr=0x1083, count=1),
                                                               pwm_duty=ModbusField(addr=0x1084, count=1)
                                                               ))

    do20: DOutput48 = field(default_factory=lambda: DOutput932(out_mode=ModbusField(addr=0x1089, count=1),
                                                               pwm_period=ModbusField(addr=0x108A, count=1),
                                                               pwm_duty=ModbusField(addr=0x108B, count=1)
                                                               ))

    do21: DOutput48 = field(default_factory=lambda: DOutput932(out_mode=ModbusField(addr=0x1090, count=1),
                                                               pwm_period=ModbusField(addr=0x1091, count=1),
                                                               pwm_duty=ModbusField(addr=0x1092, count=1)
                                                               ))

    do22: DOutput48 = field(default_factory=lambda: DOutput932(out_mode=ModbusField(addr=0x1097, count=1),
                                                               pwm_period=ModbusField(addr=0x1098, count=1),
                                                               pwm_duty=ModbusField(addr=0x1099, count=1)
                                                               ))

    do23: DOutput48 = field(default_factory=lambda: DOutput932(out_mode=ModbusField(addr=0x109E, count=1),
                                                               pwm_period=ModbusField(addr=0x109F, count=1),
                                                               pwm_duty=ModbusField(addr=0x10A0, count=1)
                                                               ))

    do24: DOutput48 = field(default_factory=lambda: DOutput932(out_mode=ModbusField(addr=0x10A5, count=1),
                                                               pwm_period=ModbusField(addr=0x10A6, count=1),
                                                               pwm_duty=ModbusField(addr=0x10A7, count=1)
                                                               ))

    do25: DOutput48 = field(default_factory=lambda: DOutput932(out_mode=ModbusField(addr=0x10AC, count=1),
                                                               pwm_period=ModbusField(addr=0x10AD, count=1),
                                                               pwm_duty=ModbusField(addr=0x10AE, count=1)
                                                               ))

    do26: DOutput48 = field(default_factory=lambda: DOutput932(out_mode=ModbusField(addr=0x10B3, count=1),
                                                               pwm_period=ModbusField(addr=0x10B4, count=1),
                                                               pwm_duty=ModbusField(addr=0x10B5, count=1)
                                                               ))

    do27: DOutput48 = field(default_factory=lambda: DOutput932(out_mode=ModbusField(addr=0x10BA, count=1),
                                                               pwm_period=ModbusField(addr=0x10BB, count=1),
                                                               pwm_duty=ModbusField(addr=0x10BC, count=1)
                                                               ))

    do28: DOutput48 = field(default_factory=lambda: DOutput932(out_mode=ModbusField(addr=0x10C1, count=1),
                                                               pwm_period=ModbusField(addr=0x10C2, count=1),
                                                               pwm_duty=ModbusField(addr=0x10C3, count=1)
                                                               ))
    do29: DOutput48 = field(default_factory=lambda: DOutput932(out_mode=ModbusField(addr=0x10C8, count=1),
                                                               pwm_period=ModbusField(addr=0x10C9, count=1),
                                                               pwm_duty=ModbusField(addr=0x10CA, count=1)
                                                               ))

    do30: DOutput48 = field(default_factory=lambda: DOutput932(out_mode=ModbusField(addr=0x10CF, count=1),
                                                               pwm_period=ModbusField(addr=0x10D0, count=1),
                                                               pwm_duty=ModbusField(addr=0x10D1, count=1)
                                                               ))

    do31: DOutput48 = field(default_factory=lambda: DOutput932(out_mode=ModbusField(addr=0x10D6, count=1),
                                                               pwm_period=ModbusField(addr=0x10D7, count=1),
                                                               pwm_duty=ModbusField(addr=0x10D8, count=1)
                                                               ))

    do32: DOutput48 = field(default_factory=lambda: DOutput932(out_mode=ModbusField(addr=0x10DD, count=1),
                                                               pwm_period=ModbusField(addr=0x10DE, count=1),
                                                               pwm_duty=ModbusField(addr=0x10DF, count=1)
                                                               ))