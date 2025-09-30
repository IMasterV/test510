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
class AInput:
    type_sensor: ModbusField
    ain_h: ModbusField
    ain_l: ModbusField
    value_float: ModbusField
    value_int: ModbusField
    timestamp: ModbusField

    def __post_init__(self):
        if self.type_sensor.value is not None and not (0 <= self.type_sensor.value <= 5):
            raise ValueError(f'тип датчика должен быть в диапазоне 0–5, а не {self.type_sensor.value}')

@dataclass
class Ai102:
    ai1: AInput = field(default_factory=lambda: AInput(type_sensor=ModbusField(addr=0x1004, count=2),
                                                        ain_h=ModbusField(addr=0x100C, count=2),
                                                        ain_l=ModbusField(addr=0x100E, count=2),
                                                        value_float=ModbusField(addr=0x0FA0, count=2),
                                                        value_int=ModbusField(addr=0x0FE0, count=1),
                                                        timestamp=ModbusField(addr=0x0FA2, count=1)
                                                        ))

    ai2: AInput = field(default_factory=lambda: AInput(type_sensor=ModbusField(addr=0x1014, count=2),
                                                        ain_h=ModbusField(addr=0x101C, count=2),
                                                        ain_l=ModbusField(addr=0x101E, count=2),
                                                        value_float=ModbusField(addr=0x0FA3, count=2),
                                                        value_int=ModbusField(addr=0x0FE1, count=1),
                                                        timestamp=ModbusField(addr=0x0FA5, count=1)
                                                        ))

    ai3: AInput = field(default_factory=lambda: AInput(type_sensor=ModbusField(addr=0x1024, count=2),
                                                        ain_h=ModbusField(addr=0x102C, count=2),
                                                        ain_l=ModbusField(addr=0x102E, count=2),
                                                        value_float=ModbusField(addr=0x0FA6, count=2),
                                                        value_int=ModbusField(addr=0x0FE2, count=1),
                                                        timestamp=ModbusField(addr=0x0FA8, count=1)
                                                        ))

    ai4: AInput = field(default_factory=lambda: AInput(type_sensor=ModbusField(addr=0x1034, count=2),
                                                        ain_h=ModbusField(addr=0x103C, count=2),
                                                        ain_l=ModbusField(addr=0x103E, count=2),
                                                        value_float=ModbusField(addr=0x0FA9, count=2),
                                                        value_int=ModbusField(addr=0x0FE3, count=1),
                                                        timestamp=ModbusField(addr=0x0FAB, count=1)
                                                        ))

    ai5: AInput = field(default_factory=lambda: AInput(type_sensor=ModbusField(addr=0x1044, count=2),
                                                        ain_h=ModbusField(addr=0x104C, count=2),
                                                        ain_l=ModbusField(addr=0x104E, count=2),
                                                        value_float=ModbusField(addr=0x0FAC, count=2),
                                                        value_int=ModbusField(addr=0x0FE4, count=1),
                                                        timestamp=ModbusField(addr=0x0FAE, count=1)
                                                        ))

    ai6: AInput = field(default_factory=lambda: AInput(type_sensor=ModbusField(addr=0x1054, count=2),
                                                        ain_h=ModbusField(addr=0x105C, count=2),
                                                        ain_l=ModbusField(addr=0x105E, count=2),
                                                        value_float=ModbusField(addr=0x0FAF, count=2),
                                                        value_int=ModbusField(addr=0x0FE5, count=1),
                                                        timestamp=ModbusField(addr=0x0FB1, count=1)
                                                        ))

    ai7: AInput = field(default_factory=lambda: AInput(type_sensor=ModbusField(addr=0x1064, count=2),
                                                        ain_h=ModbusField(addr=0x106C, count=2),
                                                        ain_l=ModbusField(addr=0x106E, count=2),
                                                        value_float=ModbusField(addr=0x0FB2, count=2),
                                                        value_int=ModbusField(addr=0x0FE6, count=1),
                                                        timestamp=ModbusField(addr=0x0FB4, count=1)
                                                        ))

    ai8: AInput = field(default_factory=lambda: AInput(type_sensor=ModbusField(addr=0x1074, count=2),
                                                        ain_h=ModbusField(addr=0x107C, count=2),
                                                        ain_l=ModbusField(addr=0x107E, count=2),
                                                        value_float=ModbusField(addr=0x0FB5, count=2),
                                                        value_int=ModbusField(addr=0x0FE7, count=1),
                                                        timestamp=ModbusField(addr=0x0FB7, count=1)
                                                        ))