import time
import sys
import math

sys.path.append('/home/root/scripts')
from md_dataclasses.mb_32do import System, Do32
from md_dataclasses.mb_202 import Di202
from md_dataclasses.mb_102 import Ai102
from baseclasses.mapper import Mapper

from baseclasses.response import SpeWriteRead
from baseclasses.modbus_operations import ConnectModule
from enums.do32_enums import OutMode
from baseclasses.modbus_operations import ModbusFeatures

from utils.do_methods import (split_32bit_to_4x8, set_logical_mode_do_spe, set_logical_mode_di_tcp, check_do_mask,
                              set_imp_gen_mode_do, set_pulse_counting_mode_202, set_filter_off_di, set_data_and_check_imp_gen_mode,
                              set_pwm_fast_mode_do, set_pwm_duty_do, set_type_sensor_102, set_ain_h_102, read_values_float_102,
                              set_pwm_slow_mode_do, set_pwm_period_do, set_period_measure_mode_di, reset_pulse_counting_di)

conf_32do = Do32()
mapper_32do = Do32()
system_params = System

di202 = Di202()
ai102 = Ai102()

module_id = 1

build = Mapper(module_id)

build.build_map_struct(conf_32do, mapper_32do)

system_params.name.value = ModbusFeatures.registers_to_ascii(SpeWriteRead(device_address=module_id).
                                                             read_data(rd_registers=system_params.name.addr,
                                                                       count=system_params.name.count)[0])

system_params.firmware_ver.value = ModbusFeatures.registers_to_ascii(SpeWriteRead(device_address=module_id).
                                                                     read_data(
    rd_registers=system_params.firmware_ver.addr,
    count=system_params.firmware_ver.count)[0])

system_params.hardware_ver.value = ModbusFeatures.registers_to_ascii(SpeWriteRead(device_address=module_id).
                                                                     read_data(
    rd_registers=system_params.hardware_ver.addr,
    count=system_params.hardware_ver.count)[0])
# добавить проверку на имя
print(f'address: {module_id}, name: {system_params.name.value}, '
      f'firmware: {system_params.firmware_ver.value}, hardware: {system_params.hardware_ver.value}')

module1 = ConnectModule(comm='tcp', host='10.77.151.34').request_module()
module2 = ConnectModule(comm='tcp', host='10.77.151.35').request_module()
module3 = ConnectModule(comm='tcp', host='10.77.151.36').request_module()
module4 = ConnectModule(comm='tcp', host='10.77.151.37').request_module()
module5_102 = ConnectModule(comm='tcp', host='10.77.151.44').request_module()
modules = [module1, module2, module3, module4]


def test_do_pos_output_logic_mode():

    set_logical_mode_do_spe(module_id, mapper_32do)
    set_logical_mode_di_tcp(di202, modules)

    device = SpeWriteRead(device_address=module_id)
    for offset in range(32):
        if offset <= 15:
            mapper_32do.do.out_mask.value = [1 << offset, 0]
        else:
            mapper_32do.do.out_mask.value = [0, 1 << (offset - 16)]

        # set bitmask_output 32do
        device.write_data(
            wr_registers=mapper_32do.do.out_mask.addr,
            data=[*mapper_32do.do.out_mask.value])

        # check bitmask_output 32do
        bitmask = device.read_data(
            rd_registers=mapper_32do.do.outputs_states.addr,
            count=mapper_32do.do.outputs_states.count)[0]


        assert bitmask == mapper_32do.do.out_mask.value, f'number output={offset + 1}'

        # separate bitmask_output
        parts = split_32bit_to_4x8(mapper_32do.do.out_mask.value)
        time.sleep(0.01)

        # Один 32DO подключен к 4 модулям по 8 входов
        module_index = offset // 8

        if module_index < len(modules):
            di202.di.input_states.value = modules[module_index].rd_holding_registers(
                address=di202.di.input_states.addr,
                count=di202.di.input_states.count
            )

            print(f'output_mask = {mapper_32do.do.out_mask.value}, module{module_index + 1} = '
                  f'{di202.di.input_states.value}, parts_module_index = {parts[module_index]}')

            assert parts[module_index] == di202.di.input_states.value, f'number output={offset + 1}'

    check_do_mask(module_id, mapper_32do, di202, modules, [65535, 65535])

    time.sleep(0.1)

    check_do_mask(module_id, mapper_32do, di202, modules, [0, 0])

test_do_pos_output_logic_mode()

def test_do_pos_output_imp_gen_mode():
    # test параметра impgen_count_out!!!!

    # set img_gen mode for 3 outputs
    set_imp_gen_mode_do(mapper_32do, module_id, num_channels=3)

    # set pulse_counting mode for 8 inputs
    set_pulse_counting_mode_202(di202, [modules[0], ], num_channels=8)

    # set filter bounce off for 20 inputs
    set_filter_off_di(di202, [modules[0], ], num_channels=20)


    for channel in range(1, 4):
        # for data_test_freq, data_test_num in ((1, 3),(10, 10), (60000, 65535)):
        for data_test_freq, data_test_num in ((1, 2), (2, 4), (3, 6)):

            set_data_and_check_imp_gen_mode(module_id, modules[0], di202,
                                            mapper_32do, data_test_freq,
                                            data_test_num, num_channels=channel)

test_do_pos_output_imp_gen_mode()

def test_do_pos_output_hs_pwm_duty():

    #set output_mode and frequency 32DO
    set_pwm_fast_mode_do(mapper_32do, module_id, OutMode.PWM_FAST)
    set_pwm_duty_do(mapper_32do, module_id, 1000, num_channels=8)

    set_type_sensor_102(ai102, module5_102, 5)
    set_ain_h_102(ai102, module5_102,10.0)
    time.sleep(2)

    values_voltage_max = read_values_float_102(ai102, module5_102)

    testing_data_duty = [3, 500, 900]
    for testing_duty in testing_data_duty:
        set_pwm_duty_do(mapper_32do, module_id, testing_duty, num_channels=8)

        time.sleep(3)

        values_voltage_current = read_values_float_102(ai102, module5_102)

        for i in range(len(values_voltage_max)):
            current_duty = (values_voltage_current[i] / values_voltage_max[i]) * 1000
            assert math.ceil(current_duty)-1 <= current_duty <= math.ceil(current_duty)+1, f"{testing_duty}"

test_do_pos_output_hs_pwm_duty()

def test_do_pos_output_pwm_period():
    # test duty???
    # duty = 1000 ?

    set_filter_off_di(di202, modules)
    set_period_measure_mode_di(di202, modules)
    reset_pulse_counting_di(di202, modules)  # ?? надо ли

    set_pwm_slow_mode_do(mapper_32do, module_id)
    set_pwm_duty_do(mapper_32do, module_id, pwm_duty=500)

    data_test_pwm_period = (1000, 30000, 60000)
    for pwm_period_value in data_test_pwm_period:
        set_pwm_period_do(mapper_32do, module_id, pwm_period=pwm_period_value)

        time.sleep((pwm_period_value / 1000) + 2)

        # Читаем счетчик всех модулей
        for module in modules:
            result = []
            for channel in range(1, 8 + 1):
                modbus_input_field = getattr(di202, f"di{channel}")

                response = module.rd_holding_registers(address=modbus_input_field.counter_value.addr,
                                                       count=modbus_input_field.counter_value.count)
                result.append(response)
            assert all(
                x in ([pwm_period_value - 1, 0], [pwm_period_value, 0], [pwm_period_value + 1, 0]) for x in result), \
                f"Некорректный результат: {result}"

    set_pwm_duty_do(mapper_32do, module_id, pwm_duty=0)

test_do_pos_output_pwm_period()

def test_do_pos_output_hs_pwm_frequency():































# mapper_32do.do.out_mask.value = [65535, 65535]
# SpeWriteRead(device_address=module_id).write_data(
#     wr_registers=mapper_32do.do.out_mask.addr,
#     data=[*mapper_32do.do.out_mask.value])
# parts = split_32bit_to_4x8(mapper_32do.do.out_mask.value)
# time.sleep(0.01)
#
# result = []
# modules = [module1, module2, module3, module4]
# for module in modules:
#     result.append(module.rd_holding_registers(
#         address=di202.di.input_states.addr,
#         count=di202.di.input_states.count
#     ))
# # print(f'parts = {parts}')
# # print(f'result = {result}')
# time.sleep(1)
# assert parts == result
#
# mapper_32do.do.out_mask.value = [0, 0]
# SpeWriteRead(device_address=module_id).write_data(
#     wr_registers=mapper_32do.do.out_mask.addr,
#     data=[*mapper_32do.do.out_mask.value])
# parts = split_32bit_to_4x8(mapper_32do.do.out_mask.value)
# time.sleep(0.01)
#
# result = []
# modules = [module1, module2, module3, module4]
# for module in modules:
#     result.append(module.rd_holding_registers(
#         address=di202.di.input_states.addr,
#         count=di202.di.input_states.count
#     ))
# assert parts == result


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

# time.sleep(1)


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
# module3 (202 10.77.151.36) и module4 (202 10.77.151.37)

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

