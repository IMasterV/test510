import time
import pytest
#import argparse

from baseclasses.spe_operations import SpeOperations
from baseclasses.response import SpeWriteRead
from baseclasses.modbus_operations import ConnectModule, ModbusFeatures
from collections import defaultdict
from enums.fai12_enums import InputMode, TypeFilter, Status, TypeBreakage
from enums.global_enums import StateCode, RegisterNumber

# parser = argparse.ArgumentParser()
# # Позиционные аргументы
# parser.add_argument('polling_time', type=float, nargs='?', default=0.5)
# parser.add_argument('just_name', type=int, nargs='?', default=0)

#args = parser.parse_args()



configure_address = [0x1000, 0x1001,
                     0x1002, 0x1004, 0x1005, 0x1006,
                     0x1008, 0x100A, 0x100B, 0x100C,
                     0x100E, 0x1010, 0x1011, 0x1012,
                     0x1014, 0x1016, 0x1017, 0x1018,
                     0x101A, 0x101B,
                     0x101C, 0x101E, 0x101F, 0x1020,
                     0x1022, 0x1024, 0x1025, 0x1026,
                     0x1028, 0x102A, 0x102B, 0x102C,
                     0x102E, 0x1030, 0x1031, 0x1032,
                     0x1034, 0x1035,
                     0x1036, 0x1038, 0x1039, 0x103A,
                     0x103C, 0x103E, 0x103F, 0x1040,
                     0x1042, 0x1044, 0x1045, 0x1046,
                     0x1048, 0x104A, 0x104B, 0x104C]

configure_name = ['filter_type1', 'type_breakage1',
                  'value1', 'status1', 'timestamp1', 'input_mode1',
                  'value2', 'status2', 'timestamp2', 'input_mode2',
                  'value3', 'status3', 'timestamp3', 'input_mode3',
                  'value4', 'status4', 'timestamp4', 'input_mode4',
                  'filter_type2', 'type_breakage2',
                  'value5', 'status5', 'timestamp5', 'input_mode5',
                  'value6', 'status6', 'timestamp6', 'input_mode6',
                  'value7', 'status7', 'timestamp7', 'input_mode7',
                  'value8', 'status8', 'timestamp8', 'input_mode8',
                  'filter_type3', 'type_breakage3',
                  'value9', 'status9', 'timestamp9', 'input_mode9',
                  'value10', 'status10', 'timestamp10', 'input_mode10',
                  'value11', 'status11', 'timestamp11', 'input_mode11',
                  'value12', 'status12', 'timestamp12', 'input_mode12',]
quantity = [1, 1,
            2, 1, 1, 1,
            2, 1, 1, 1,
            2, 1, 1, 1,
            2, 1, 1, 1,
            1, 1,
            2, 1, 1, 1,
            2, 1, 1, 1,
            2, 1, 1, 1,
            2, 1, 1, 1,
            1, 1,
            2, 1, 1, 1,
            2, 1, 1, 1,
            2, 1, 1, 1,
            2, 1, 1, 1]

base_map_region = 0xfe00
base_map_regs = 0xff00

module_id = 3


response = SpeWriteRead(device_address=module_id).read_data(rd_registers=0x102, count=3)
print(response)

def init_preop_safeop_op(device_address, name, mb_address, count, map_region, map_regs):
    mapper_modbus_regs = defaultdict(tuple)
    for state in range(4):
        SpeWriteRead(device_address=device_address).write_data(wr_registers=RegisterNumber.CONTROL, data=[1 << state])

        # configure mapper in preop
        if 1 << state == 2:
            for reg_name, reg_address, reg_quantity in zip(name, mb_address, count):
                mapper_modbus_regs[reg_name] = (map_regs, reg_quantity)

                for offset in range(reg_quantity):
                    SpeWriteRead(device_address=device_address).write_data(wr_registers=map_region,
                                                                           data=[reg_address + offset])
                    map_region += 1
                    map_regs += 1

        if 1 << state == 8:
            return mapper_modbus_regs


my_mapper = init_preop_safeop_op(module_id, configure_name, configure_address,
                                 quantity, base_map_region, base_map_regs)

# адрес, имя, заводской, прошивка
module_name = ModbusFeatures.registers_to_ascii(SpeWriteRead(device_address=module_id).read_data(rd_registers=0x0000, count=16)[0])
firmware_version = ModbusFeatures.registers_to_ascii(SpeWriteRead(device_address=module_id).read_data(rd_registers=0x0010, count=8)[0])
hardware_version = ModbusFeatures.registers_to_ascii(SpeWriteRead(device_address=module_id).read_data(rd_registers=0x0018, count=8)[0])

print(f'address: {module_id}, name: {module_name}, firmware: {firmware_version}, hardware: {hardware_version}')

iterations = range(1, 26)
type_filter = (3, 0, 0, 3, 2, 3, 4, 1, 1, 2, 4, 0, 2, 0, 4, 4, 4, 1, 0, 2, 3, 2, 1, 3, 1)
control = (2, 0, 2, 0, 1, 1, 0, 1, 2, 2, 1, 1, 0, 0, 2, 2, 2, 0, 0, 0, 1, 1, 1, 1, 0)
mode = (2, 5, 4, 1, 1, 3, 3, 2, 5, 3, 4, 1, 2, 2, 5, 2, 1, 3, 3, 4, 4, 5, 4, 5, 1)

num_channels = ('1', '5', '15', '9', '19', '59', '159')

params = [
    (channel, it, tf, ctl, md)
    for channel in num_channels
    for it, tf, ctl, md in zip(iterations, type_filter, control, mode)
]
@pytest.mark.parametrize('channel, it, type_f, ctrl, md', params)
def test_filter_one_channel_break_zero(channel, it, type_f, ctrl, md):
    count_error_assertions = 0
    count_index_error = 0
    config_delay = 0.5
    polling_delay = 0.01
    timeout_delay = 5
    delay = 1


    correct_timestamps = {0: (10, 11, 12, 13), 1: (14, 15, 16, 17), 2: (22, 23, 24, 25),
                          3: (38, 39, 40, 41), 4: (127, 128, 129, 130)}

    for num in range(1, 13):
        SpeWriteRead(device_address=module_id).write_data(wr_registers=my_mapper[f'input_mode{num}'][0],
                                                          data=[InputMode.DISABLE])
    # при переходе с фильтра FIVE на любой другой требуется таймаут
    time.sleep(0.5)
    for num in range(1, 4):
        SpeWriteRead(device_address=module_id).write_data(wr_registers=my_mapper[f'filter_type{num}'][0],
                                                          data=[type_f])
        SpeWriteRead(device_address=module_id).write_data(wr_registers=my_mapper[f'type_breakage{num}'][0],
                                                          data=[ctrl])

    # SpeWriteRead(device_address=module_id).write_data(wr_registers=my_mapper[f'filter_type'][0],
    #                                                   data=[TypeFilter.TWO])
    # SpeWriteRead(device_address=module_id).write_data(wr_registers=my_mapper[f'type_breakage'][0],
    #                                                   data=[TypeBreakage.DISABLE])

    for num in channel:
        SpeWriteRead(device_address=module_id).write_data(wr_registers=my_mapper[f'input_mode{num}'][0],
                                                          data=[InputMode.CURRENT020])
    # SpeWriteRead(device_address=module_id).write_data(wr_registers=my_mapper[f'input_mode1'][0], data=[InputMode.CURRENT020])
    # SpeWriteRead(device_address=module_id).write_data(wr_registers=my_mapper[f'input_mode2'][0], data=[InputMode.DISABLE])
    # SpeWriteRead(device_address=module_id).write_data(wr_registers=my_mapper[f'input_mode3'][0], data=[InputMode.DISABLE])
    # SpeWriteRead(device_address=module_id).write_data(wr_registers=my_mapper[f'input_mode4'][0], data=[InputMode.DISABLE])
    # SpeWriteRead(device_address=module_id).write_data(wr_registers=my_mapper[f'input_mode5'][0], data=[InputMode.DISABLE])
    # SpeWriteRead(device_address=module_id).write_data(wr_registers=my_mapper[f'input_mode6'][0], data=[InputMode.DISABLE])
    # SpeWriteRead(device_address=module_id).write_data(wr_registers=my_mapper[f'input_mode7'][0], data=[InputMode.DISABLE])
    # SpeWriteRead(device_address=module_id).write_data(wr_registers=my_mapper[f'input_mode8'][0], data=[InputMode.DISABLE])
    # SpeWriteRead(device_address=module_id).write_data(wr_registers=my_mapper[f'input_mode9'][0], data=[InputMode.DISABLE])
    # SpeWriteRead(device_address=module_id).write_data(wr_registers=my_mapper[f'input_mode10'][0], data=[InputMode.DISABLE])
    # SpeWriteRead(device_address=module_id).write_data(wr_registers=my_mapper[f'input_mode11'][0], data=[InputMode.DISABLE])
    # SpeWriteRead(device_address=module_id).write_data(wr_registers=my_mapper[f'input_mode12'][0], data=[InputMode.DISABLE])

    print(f'filter = {type_f}, ctrl = {ctrl}, channel = {channel}')

    print('taking data for service operations. Waiting 3 seconds')
    time.sleep(3)

    count_iteration = 0

    for num in range(1, 13):
        input_mode = SpeWriteRead(device_address=module_id).read_data(rd_registers=my_mapper[f'input_mode{num}'][0],
                                                                     count=my_mapper[f'input_mode{num}'][1])[0]

        if input_mode[0] != InputMode.DISABLE:
            print(f'try to request timestamp{num}')
            for _ in range(10):
                try:
                    timestamp = SpeWriteRead(device_address=module_id).read_data(rd_registers=my_mapper[f'timestamp{num}'][0],
                                                                                 count=my_mapper[f'timestamp{num}'][1])[0]

                    while True:
                        response = SpeWriteRead(device_address=module_id).read_data(rd_registers=my_mapper[f'timestamp{num}'][0],
                                                                                    count=my_mapper[f'timestamp{num}'][1])[0]
                        if response != timestamp:
                            print(f'{it}. timestamp{num} = {(response[0] - timestamp[0]) % 65536}')
                            try:
                                assert (response[0] - timestamp[0]) % 65536 in correct_timestamps[type_f]
                            except AssertionError:
                                print('')
                                print(f'Ошибка AssertionError. 1.{timestamp} 2.{response}')
                                print('')
                                print('')
                                print('')
                                count_error_assertions += 1
                            break
                        timestamp = response
                        time.sleep(polling_delay)

                        #asyncio.run(timeout_task(timeout))
                    # добавить обработку
                except IndexError:
                    count_index_error += 1
                    print(f'Повтор через {delay} сек...')
                    time.sleep(delay)
                    # response = SpeWriteRead(device_address=module_id).read_data(rd_registers=my_mapper[f'timestamp{num}'][0], count=1)[0]
                    # print(f'Timestamp = {response[0]}')
                except TimeoutError:
                    print(f'Ошибка {TimeoutError}')
    #return count_error_assertions, count_index_error

#
# test_filter_one_channel_break_zero('9', 1, 0, 1)

# count_errors = 0
# count_no_data = 0
#
#
# start = time.perf_counter()
# for channel in num_channels:
#     for it, tf, ctl, md in zip(iterations, type_filter, control, mode):
#         num_errors, num_no_data = test_filter_one_channel_break_zero(it, channel, tf, ctl, md)
#         print(f'Количество ошибок Assertions = {num_errors}, Количество ошибок no_data = {num_no_data}')
#         count_errors += num_errors
#         count_no_data += num_no_data
#
#
# print(f'Общее количество ошибок Assertions = {count_errors}')
# print(f'Общее количество no_data = {count_no_data}')
#
# end = time.perf_counter()
# print(f'Длительность теста = {end - start}')




    # while True:
    #     response = SpeWriteRead(device_address=module_id).read_data(rd_registers=base_map_regs, count=12)[0]
    #     print(response)
    #     value1 = ModbusFeatures.int16_list_to_float(response[2:4])
    #     value2 = ModbusFeatures.int16_list_to_float(response[7:9])
    #
    #     print(f'{count_iteration}. value1 = {value1}, status1 = {response[4]}')
    #     print(f'{count_iteration}. value2 = {value2}, status2 = {response[9]}')
    #
    #     count_iteration += 1
    #     time.sleep(args.polling_time)

