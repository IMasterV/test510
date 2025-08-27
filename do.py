import time
from md_dataclasses.modbus_database import Fai12, System
from md_dataclasses.mb_32do import System, Do32
from md_dataclasses.mb_202 import Di202
from baseclasses.mapper import Mapper
from enums.fai12_enums import InputMode
#from md_dataclasses import fields

from baseclasses.response import SpeWriteRead
from baseclasses.modbus_operations import ConnectModule, ModbusFeatures
from enums.do32_enums import OutMode


conf_32do = Do32()
mapper_32do = Do32()
system_params = System

di202= Di202()

module_id = 1

build = Mapper(module_id)

build.build_map_struct(conf_32do, mapper_32do)


system_params.name.value = ModbusFeatures.registers_to_ascii(SpeWriteRead(device_address=module_id).
                                                read_data(rd_registers=system_params.name.addr,
                                                          count=system_params.name.count)[0])

system_params.firmware_ver.value = ModbusFeatures.registers_to_ascii(SpeWriteRead(device_address=module_id).
                                                     read_data(rd_registers=system_params.firmware_ver.addr,
                                                               count=system_params.firmware_ver.count)[0])

system_params.hardware_ver.value = ModbusFeatures.registers_to_ascii(SpeWriteRead(device_address=module_id).
                                                     read_data(rd_registers=system_params.hardware_ver.addr,
                                                               count=system_params.hardware_ver.count)[0])
#добавить проверку на имя
print(f'address: {module_id}, name: {system_params.name.value}, '
      f'firmware: {system_params.firmware_ver.value}, hardware: {system_params.hardware_ver.value}')



module1 = ConnectModule(comm='tcp', host='10.77.151.34').request_module()
module2 = ConnectModule(comm='tcp', host='10.77.151.35').request_module()
module3 = ConnectModule(comm='tcp', host='10.77.151.36').request_module()
module4 = ConnectModule(comm='tcp', host='10.77.151.37').request_module()


# di202.di.input_states.value = module1.rd_holding_registers(address=di202.di.input_states.addr,
#                              count=di202.di.input_states.count)
#
# print(di202.di.input_states.value)




# LOG MODE
#конф маппер, переходим в ОП

# проверить машину состояния
# регистры 102 и 104

# включить режим лог на всех выходах

def
for channel in range(1, 9):
    modbus_output_field = getattr(mapper_32do, f"do{channel}")

    modbus_output_field.out_mode.value = OutMode.LOGICAL
    SpeWriteRead(device_address=module_id).write_data(
        wr_registers=modbus_output_field.out_mode.addr,
        data=[modbus_output_field.out_mode.value])

#добавить включение на всех модулях
for channel in range(1, 9):
    modbus_input_field = getattr(di202, f"di{channel}")

    modbus_input_field.input_mode.value = 0
    module1.wr_holding_registers(address=modbus_input_field.input_mode.addr,
                                values=[modbus_input_field.input_mode.value])



def split_32bit_to_4x8(mask):
    """
    Делит 32-битную маску [low, high] на 4 части по 8 бит.
    Возвращает список из 4 масок [[x,0], [x,0], [x,0], [x,0]]
    для модулей DI1..DI4.
    """
    low, high = mask
    full = (high << 16) | low   # собираем одно число из 32 бит
    parts = []
    for i in range(4):
        part = (full >> (i * 8)) & 0xFF   # берём по 8 бит
        parts.append([part, 0])           # храним в формате [val, 0]
    return parts


for offset in range(32):
    print(f'number output {offset+1}')

    if offset <= 15:
        mapper_32do.do.out_mask.value = [1 << offset, 0]
    else:
        mapper_32do.do.out_mask.value = [0, 1 << (offset - 16)]

    #set bitmask_output
    SpeWriteRead(device_address=module_id).write_data(
        wr_registers=mapper_32do.do.out_mask.addr,
        data=[*mapper_32do.do.out_mask.value])

    #check bitmask_output
    bitmask = SpeWriteRead(device_address=module_id).read_data(
        rd_registers=mapper_32do.do.outputs_states.addr,
        count=mapper_32do.do.outputs_states.count)[0]

    assert bitmask == mapper_32do.do.out_mask.value


    parts = split_32bit_to_4x8(mapper_32do.do.out_mask.value)
    time.sleep(0.01)

    module_index = offset // 8
    modules = [module1, module2, module3, module4]
    if module_index < len(modules):
        di202.di.input_states.value = modules[module_index].rd_holding_registers(
            address=di202.di.input_states.addr,
            count=di202.di.input_states.count
        )

        print(f'output_mask = {mapper_32do.do.out_mask.value}, module{module_index+1} = {di202.di.input_states.value}, parts_module_index = {parts[module_index]}')

        assert parts[module_index] == di202.di.input_states.value




mapper_32do.do.out_mask.value = [65535, 65535]
SpeWriteRead(device_address=module_id).write_data(
    wr_registers=mapper_32do.do.out_mask.addr,
    data=[*mapper_32do.do.out_mask.value])
time.sleep(0.01)

result = []
modules = [module1, module2, module3, module4]
for module in modules:
    result.append(module.rd_holding_registers(
        address=di202.di.input_states.addr,
        count=di202.di.input_states.count
    ))

parts = split_32bit_to_4x8(mapper_32do.do.out_mask.value)

print(f'parts = {parts}')
print(f'result = {result}')

time.sleep(0.5)
SpeWriteRead(device_address=module_id).write_data(
    wr_registers=mapper_32do.do.out_mask.addr,
    data=[*[0, 0]])



















    # if offset <= 7:
    #     di202.di.input_states.value = module1.rd_holding_registers(address=di202.di.input_states.addr,
    #                                                                count=di202.di.input_states.count)
    #
    #     print(f'output_mask = {mapper_32do.do.out_mask.value}, module1 = {di202.di.input_states.value}')
    #
    # if 8 <= offset <= 15:
    #     di202.di.input_states.value = module2.rd_holding_registers(address=di202.di.input_states.addr,
    #                                                                count=di202.di.input_states.count)
    #
    #     print(f'output_mask = {mapper_32do.do.out_mask.value}, module2 = {di202.di.input_states.value}')
    #
    # if 16 <= offset <= 24:
    #     di202.di.input_states.value = module3.rd_holding_registers(address=di202.di.input_states.addr,
    #                                                                count=di202.di.input_states.count)
    #
    #     print(f'output_mask = {mapper_32do.do.out_mask.value}, module3 = {di202.di.input_states.value}')
    #
    # if 25 <= offset <= 32:
    #     di202.di.input_states.value = module4.rd_holding_registers(address=di202.di.input_states.addr,
    #                                                                count=di202.di.input_states.count)
    #
    #     print(f'output_mask = {mapper_32do.do.out_mask.value}, module4 = {di202.di.input_states.value}')

    #time.sleep(1)







# for offset in range(16):
#     mapper_32do.do.out_mask.value = [0, 1 << offset]
#     SpeWriteRead(device_address=module_id).write_data(
#         wr_registers=mapper_32do.do.out_mask.addr,
#         data=[*mapper_32do.do.out_mask.value])
#
#
#     di202.di.input_states.value = module1.rd_holding_registers(address=di202.di.input_states.addr,
#                                                                count=di202.di.input_states.count)


# bitmask_out и module1 (202 10.77.151.34) и module2 (202 10.77.151.35) и
#module3 (202 10.77.151.36) и module4 (202 10.77.151.37)

# поочереди включаем
# все включаем, все выключаем






# mapper_32do.do1.out_mode.value = 0
# SpeWriteRead(device_address=module_id).write_data(
#     wr_registers=mapper_32do.do1.out_mode.addr,
#     data=[mapper_32do.do1.out_mode.value])
#
# time.sleep(1)
#
# mapper_32do.do.out_mask.value = [65535, 65535]
# SpeWriteRead(device_address=module_id).write_data(
#     wr_registers=mapper_32do.do.out_mask.addr,
#     data=[*mapper_32do.do.out_mask.value])
#
# time.sleep(1)
# mapper_32do.do.out_mask.value = SpeWriteRead(device_address=module_id).read_data(rd_registers=mapper_32do.do.out_mask.addr,
#                                                                count=mapper_32do.do.out_mask.count)[0]
# print(f'BitOutput = {mapper_32do.do.out_mask.value}')



# time.sleep(5)
# mapper_32do.do.out_mask.value = 0
# SpeWriteRead(device_address=module_id).write_data(
#     wr_registers=mapper_32do.do.out_mask.addr,
#     data=[mapper_32do.do.out_mask.value])
#
# mapper_32do.do.out_mask.value = 0
# SpeWriteRead(device_address=module_id).write_data(
#     wr_registers=mapper_32do.do.out_mask.addr+1,
#     data=[mapper_32do.do.out_mask.value])
#
# mapper_32do.do.out_mask.value = SpeWriteRead(device_address=module_id).read_data(rd_registers=mapper_32do.do.out_mask.addr,
#                                                                count=mapper_32do.do.out_mask.count)[0]
# print(f'BitOutput = {mapper_32do.do.out_mask.value}')
#
# mapper_32do.do1.out_mode.count = SpeWriteRead(device_address=module_id).read_data(rd_registers=mapper_32do.do1.out_mode.addr,
#                                                                count=mapper_32do.do1.out_mode.count)[0]
# print(f'Mode1 = {mapper_32do.do1.out_mode.count}')