from collections import defaultdict
from baseclasses.response import SpeWriteRead
from enums.global_enums import RegisterNumber
from dataclasses import fields

class Mapper:
    def __init__(self, module_id):
        self.base_map_region = 0xfe00
        self.base_map_regs = 0xff00

        self.module_id = module_id

    def build_map(self, configure_address, configure_name, configure_quantity):
        mapper_modbus_regs = defaultdict(tuple)
        for state in range(4):
            SpeWriteRead(device_address=self.module_id).write_data(wr_registers=RegisterNumber.CONTROL,
                                                                   data=[1 << state])

            # configure mapper in preop
            if 1 << state == 2:
                for reg_address, reg_name, reg_quantity in zip(configure_address, configure_name, configure_quantity):
                    mapper_modbus_regs[reg_name] = (self.base_map_regs, reg_quantity)

                    for offset in range(reg_quantity):
                        SpeWriteRead(device_address=self.module_id).write_data(wr_registers=self.base_map_region,
                                                                               data=[reg_address + offset])
                        self.base_map_region += 1
                        self.base_map_regs += 1

            if 1 << state == 8:
                return mapper_modbus_regs


    def build_map_struct(self, struct_conf, struct_mapper):

        for state in range(4):
            SpeWriteRead(device_address=self.module_id).write_data(wr_registers=RegisterNumber.CONTROL,
                                                                   data=[1 << state])

            # configure mapper in preop
            if 1 << state == 2:

                for field in fields(struct_conf):
                    name = field.name
                    all_obj = getattr(struct_conf, name)

                    def get_nested_attr(obj, *attrs):
                        for attr in attrs:
                            obj = getattr(obj, attr)
                        return obj

                    for field_name, modbus_field in all_obj.__dict__.items():

                        modbus_field_obj = get_nested_attr(struct_mapper, name, field_name)
                        modbus_field_obj.addr = self.base_map_regs

                        for offset in range(modbus_field.count):
                            SpeWriteRead(device_address=self.module_id).write_data(wr_registers=self.base_map_region,
                                                                      data=[modbus_field.addr + offset])

                            self.base_map_region += 1
                            self.base_map_regs += 1