from dataclasses import dataclass, asdict, field
from typing import Any, Optional

@dataclass
class ModbusField:
    addr: int
    count: int
    value: Optional[Any] = None

# @dataclass
# class System:
#     name = ModbusField(addr=0x0000, count=16)
#     firmware_ver = ModbusField(addr=0x0010, count=8)
#     hardware_ver = ModbusField(addr=0x0018, count=8)
#     module_position = ModbusField(addr=0x0020, count=8)
#     system_time = ModbusField(addr=0x0030, count=2) #count = 2?
#     fsm_current_state = ModbusField(addr=0x0102, count=1)
#     fsm_control_state = ModbusField(addr=0x0103, count=1)
#     fsm_status = ModbusField(addr=0x0104, count=1)
#     so_timeout = ModbusField(addr=0x0110, count=1)
#     restart = ModbusField(addr=0x0180, count=1)

@dataclass
class DInput12:
    input_mode: ModbusField
    filter_bounce: ModbusField
    period: ModbusField
    counter_value: ModbusField
    reset_counter: ModbusField

    def __post_init__(self):
        if self.input_mode.value is not None and not (0 <= self.input_mode.value <= 3):
            raise ValueError(f'mode должен быть в диапазоне 0–3, а не {self.input_mode.value}')

@dataclass
class DInput18:
    input_mode: ModbusField
    filter_bounce: ModbusField
    period_measure: ModbusField
    counter_value: ModbusField
    reset_counter: ModbusField

    def __post_init__(self):
        if self.input_mode.value is not None and not (0 <= self.input_mode.value <= 4):
            raise ValueError(f'mode должен быть в диапазоне 0–4, а не {self.input_mode.value}')

@dataclass
class DInput920:
    filter_bounce: ModbusField
    counter_value: ModbusField
    reset_counter: ModbusField

@dataclass
class DInput:
    input_states: ModbusField


@dataclass
class Di202:
    di: DInput = field(default_factory=lambda: DInput(input_states=ModbusField(addr=0x0033, count=2)))

    di1: DInput18 = field(default_factory=lambda: DInput18(input_mode=ModbusField(addr=0x0040, count=1),
                                                        filter_bounce=ModbusField(addr=0x0060, count=1),
                                                        period_measure=ModbusField(addr=0x0080, count=1),
                                                        counter_value=ModbusField(addr=0x00A0, count=2),
                                                        reset_counter=ModbusField(addr=0x00E0, count=1)
                                                        ))

    di2: DInput18 = field(default_factory=lambda: DInput18(input_mode=ModbusField(addr=0x0041, count=1),
                                                        filter_bounce=ModbusField(addr=0x0061, count=1),
                                                        period_measure=ModbusField(addr=0x0081, count=1),
                                                        counter_value=ModbusField(addr=0x00A2, count=2),
                                                        reset_counter=ModbusField(addr=0x00E1, count=1)
                                                        ))

    di3: DInput18 = field(default_factory=lambda: DInput18(input_mode=ModbusField(addr=0x0042, count=1),
                                                        filter_bounce=ModbusField(addr=0x0062, count=1),
                                                        period_measure=ModbusField(addr=0x0082, count=1),
                                                        counter_value=ModbusField(addr=0x00A4, count=2),
                                                        reset_counter=ModbusField(addr=0x00E2, count=1)
                                                        ))

    di4: DInput18 = field(default_factory=lambda: DInput18(input_mode=ModbusField(addr=0x0043, count=1),
                                                        filter_bounce=ModbusField(addr=0x0063, count=1),
                                                        period_measure=ModbusField(addr=0x0083, count=1),
                                                        counter_value=ModbusField(addr=0x00A6, count=2),
                                                        reset_counter=ModbusField(addr=0x00E3, count=1)
                                                        ))

    di5: DInput18 = field(default_factory=lambda: DInput18(input_mode=ModbusField(addr=0x0044, count=1),
                                                        filter_bounce=ModbusField(addr=0x0064, count=1),
                                                        period_measure=ModbusField(addr=0x0084, count=1),
                                                        counter_value=ModbusField(addr=0x00A8, count=2),
                                                        reset_counter=ModbusField(addr=0x00E4, count=1)
                                                        ))

    di6: DInput18 = field(default_factory=lambda: DInput18(input_mode=ModbusField(addr=0x0045, count=1),
                                                        filter_bounce=ModbusField(addr=0x0065, count=1),
                                                        period_measure=ModbusField(addr=0x0085, count=1),
                                                        counter_value=ModbusField(addr=0x00AA, count=2),
                                                        reset_counter=ModbusField(addr=0x00E5, count=1)
                                                        ))

    di7: DInput18 = field(default_factory=lambda: DInput18(input_mode=ModbusField(addr=0x0046, count=1),
                                                        filter_bounce=ModbusField(addr=0x0066, count=1),
                                                        period_measure=ModbusField(addr=0x0086, count=1),
                                                        counter_value=ModbusField(addr=0x00AC, count=2),
                                                        reset_counter=ModbusField(addr=0x00E6, count=1)
                                                        ))

    di8: DInput18 = field(default_factory=lambda: DInput18(input_mode=ModbusField(addr=0x0047, count=1),
                                                        filter_bounce=ModbusField(addr=0x0067, count=1),
                                                        period_measure=ModbusField(addr=0x0087, count=1),
                                                        counter_value=ModbusField(addr=0x00AE, count=2),
                                                        reset_counter=ModbusField(addr=0x00E7, count=1)
                                                        ))

    di9: DInput920 = field(default_factory=lambda: DInput920(filter_bounce=ModbusField(addr=0x0068, count=1),
                                                        counter_value=ModbusField(addr=0x00B0, count=2),
                                                        reset_counter=ModbusField(addr=0x00E8, count=1)
                                                        ))

    di10: DInput920 = field(default_factory=lambda: DInput920(filter_bounce=ModbusField(addr=0x0069, count=1),
                                                        counter_value=ModbusField(addr=0x00B2, count=2),
                                                        reset_counter=ModbusField(addr=0x00E9, count=1)
                                                        ))

    di11: DInput920 = field(default_factory=lambda: DInput920(filter_bounce=ModbusField(addr=0x006A, count=1),
                                                        counter_value=ModbusField(addr=0x00B4, count=2),
                                                        reset_counter=ModbusField(addr=0x00EA, count=1)
                                                        ))

    di12: DInput920 = field(default_factory=lambda: DInput920(filter_bounce=ModbusField(addr=0x006B, count=1),
                                                        counter_value=ModbusField(addr=0x00B6, count=2),
                                                        reset_counter=ModbusField(addr=0x00EB, count=1)
                                                        ))

    di13: DInput920 = field(default_factory=lambda: DInput920(filter_bounce=ModbusField(addr=0x006C, count=1),
                                                        counter_value=ModbusField(addr=0x00B8, count=2),
                                                        reset_counter=ModbusField(addr=0x00EC, count=1)
                                                        ))

    di14: DInput920 = field(default_factory=lambda: DInput920(filter_bounce=ModbusField(addr=0x006D, count=1),
                                                        counter_value=ModbusField(addr=0x00BA, count=2),
                                                        reset_counter=ModbusField(addr=0x00ED, count=1)
                                                        ))

    di15: DInput920 = field(default_factory=lambda: DInput920(filter_bounce=ModbusField(addr=0x006E, count=1),
                                                        counter_value=ModbusField(addr=0x00BC, count=2),
                                                        reset_counter=ModbusField(addr=0x00EE, count=1)
                                                        ))

    di16: DInput920 = field(default_factory=lambda: DInput920(filter_bounce=ModbusField(addr=0x006F, count=1),
                                                        counter_value=ModbusField(addr=0x00BE, count=2),
                                                        reset_counter=ModbusField(addr=0x00EF, count=1)
                                                        ))

    di17: DInput920 = field(default_factory=lambda: DInput920(filter_bounce=ModbusField(addr=0x0070, count=1),
                                                        counter_value=ModbusField(addr=0x00C0, count=2),
                                                        reset_counter=ModbusField(addr=0x00F0, count=1)
                                                        ))

    di18: DInput920 = field(default_factory=lambda: DInput920(filter_bounce=ModbusField(addr=0x0071, count=1),
                                                        counter_value=ModbusField(addr=0x00C2, count=2),
                                                        reset_counter=ModbusField(addr=0x00F1, count=1)
                                                        ))

    di19: DInput920 = field(default_factory=lambda: DInput920(filter_bounce=ModbusField(addr=0x0072, count=1),
                                                        counter_value=ModbusField(addr=0x00C4, count=2),
                                                        reset_counter=ModbusField(addr=0x00F2, count=1)
                                                        ))

    di20: DInput920 = field(default_factory=lambda: DInput920(filter_bounce=ModbusField(addr=0x0073, count=1),
                                                        counter_value=ModbusField(addr=0x00C6, count=2),
                                                        reset_counter=ModbusField(addr=0x00F3, count=1)
                                                        ))


    #
    # do1: DOutput13 = field(default_factory=lambda: DOutput13(out_mode=ModbusField(addr=0x1004, count=1),
    #                                                          pwm_period=ModbusField(addr=0x1005, count=1),
    #                                                          pwm_duty=ModbusField(addr=0x1006, count=1),
    #                                                          hs_pwm_freq=ModbusField(addr=0x1007, count=1),
    #                                                          impgen_freq=ModbusField(addr=0x1008, count=1),
    #                                                          impgen_num=ModbusField(addr=0x1009, count=1),
    #                                                          impgen_count_out=ModbusField(addr=0x100A, count=1)
    #                                                          ))