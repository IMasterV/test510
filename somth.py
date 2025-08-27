import json
from md_dataclasses.modbus_database import ModbusDatabase, ModbusDataFromJson
from baseclasses.mapper import Mapper
from md_dataclasses import fields
from copy import deepcopy

from baseclasses.response import SpeWriteRead
from baseclasses.modbus_operations import ConnectModule, ModbusFeatures

with open("json_files/fai12_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

conf_fai12 = ModbusDataFromJson(data)
mapper_fai12 = deepcopy(conf_fai12)

build = Mapper(module_id=4)

build.build_map_struct(conf_fai12, mapper_fai12)

print(mapper_fai12.group1.typeFilter.addr)
print(conf_fai12.group1.typeFilter.addr)



# module_name = ModbusFeatures.registers_to_ascii(SpeWriteRead(device_address=4).read_data(rd_registers=0x0000, count=16)[0])
# print(module_name)



# base_map_region = 0xfe00
# base_map_regs = 0xff00
#
# SpeWriteRead(device_address=4).write_data(wr_registers=0x0103,
#                                           data=[0b0001])
# SpeWriteRead(device_address=4).write_data(wr_registers=0x0103,
#                                           data=[0b0010])
#
#
#
#
# SpeWriteRead(device_address=4).write_data(wr_registers=0x0103,
#                                           data=[0b0100])
#
# SpeWriteRead(device_address=4).write_data(wr_registers=0x0103,
#                                           data=[0b1000])



#
# print(mapper_modbus_db.group1.typeFilter.addr)


# for reg_address, reg_name, reg_quantity in zip(configure_address, configure_name, configure_quantity):
#     mapper_modbus_regs[reg_name] = (base_map_regs, reg_quantity)
#
#     for offset in range(reg_quantity):
#         SpeWriteRead(device_address=module_id).write_data(wr_registers=base_map_region,
#                                                           data=[reg_address + offset])
#         base_map_region += 1
#         base_map_regs += 1





# class Mapper:
#     def __init__(self, configure_address, configure_name, configure_quantity):
#         self.configure_address = configure_address
#         self.configure_name = configure_name
#         self.configure_quantity = configure_quantity
#
#     def build_map(self, module_id):
#
#
#         mapper_modbus_regs = defaultdict(tuple)
#         for state in range(4):
#             SpeWriteRead(device_address=module_id).write_data(wr_registers=RegisterNumber.CONTROL,
#                                                                    data=[1 << state])
#
#             # configure mapper in preop
#             if 1 << state == 2:
#                 for reg_address, reg_name, reg_quantity in zip(self.configure_address, self.configure_name, self.configure_quantity):
#                     mapper_modbus_regs[reg_name] = (base_map_regs, reg_quantity)
#
#                     for offset in range(reg_quantity):
#                         SpeWriteRead(device_address=module_id).write_data(wr_registers=base_map_region,
#                                                                                data=[reg_address + offset])
#                         base_map_region += 1
#                         base_map_regs += 1
#
#             if 1 << state == 8:
#                 return mapper_modbus_regs
