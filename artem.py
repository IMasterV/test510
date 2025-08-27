import time
import argparse

from baseclasses.spe_operations import SpeOperations
from baseclasses.response import SpeWriteRead
from baseclasses.modbus_operations import ConnectModule, ModbusFeatures
from collections import defaultdict
from enums.fai12_enums import InputMode, TypeFilter, Status
from enums.global_enums import StateCode, RegisterNumber

parser = argparse.ArgumentParser()
# РџРѕР·РёС†РёРѕРЅРЅС‹Рµ Р°СЂРіСѓРјРµРЅС‚С‹
parser.add_argument('num_request', type=int, nargs='?', default=1)
parser.add_argument('polling_time', type=float, nargs='?', default=0.005)
parser.add_argument('just_name', type=int, nargs='?', default=0)

args = parser.parse_args()

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
                  'value12', 'status12', 'timestamp12', 'input_mode12', ]
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

# SpeWriteRead(device_address=module_id).write_data(wr_registers=RegisterNumber.CONTROL, data=[StateCode.INIT])
# SpeWriteRead(device_address=module_id).write_data(wr_registers=RegisterNumber.CONTROL, data=[StateCode.PREOP])
# SpeWriteRead(device_address=module_id).write_data(wr_registers=RegisterNumber.CONTROL, data=[StateCode.SAFEOP])
# while True:
#     try:
#         response = SpeWriteRead(device_address=module_id).read_data(rd_registers=configure_address[0], count=1)[
#             0]
#         time.sleep(args.polling_time)
#     except IndexError:
#         print('отсутствуют данные')
#     except KeyboardInterrupt:
#         end = time.perf_counter()



def init_preop_safeop_op(device_address, name, mb_address, count, map_region, map_regs):
    mapper_modbus_regs = defaultdict(tuple)
    for state in range(4):
        SpeWriteRead(device_address=device_address).write_data(wr_registers=RegisterNumber.CONTROL, data=[1 << state])

        # configure mapper in preop
        if 1 << state == 2:
            for reg_name, reg_address, reg_quantity in zip(name, mb_address, count):
                mapper_modbus_regs[reg_name] = (map_regs, reg_quantity)
                mb_configure_reg = reg_address

                for offset in range(reg_quantity):
                    SpeWriteRead(device_address=device_address).write_data(wr_registers=map_region,
                                                                           data=[mb_configure_reg + offset])

                    map_region += 1
                    map_regs += 1

        if 1 << state == 8:
            return mapper_modbus_regs

my_mapper = init_preop_safeop_op(module_id, configure_name, configure_address,
                                 quantity, base_map_region, base_map_regs)

# Р°РґСЂРµСЃ, РёРјСЏ, Р·Р°РІРѕРґСЃРєРѕР№, РїСЂРѕС€РёРІРєР°
module_name = ModbusFeatures.registers_to_ascii(
    SpeWriteRead(device_address=module_id).read_data(rd_registers=0x0000, count=16)[0])
firmware_version = ModbusFeatures.registers_to_ascii(
    SpeWriteRead(device_address=module_id).read_data(rd_registers=0x0010, count=8)[0])
hardware_version = ModbusFeatures.registers_to_ascii(
    SpeWriteRead(device_address=module_id).read_data(rd_registers=0x0018, count=8)[0])

print(f'address {module_id}, name: {module_name}, firmware: {firmware_version}, hardware: {hardware_version}')

my_filter = TypeFilter.ONE
my_breakage = 0
mode1 = InputMode.VOLTAGE01
mode2 = InputMode.CURRENT420
count_ai_error = 0

start = time.perf_counter()
if args.just_name == 0:
    SpeWriteRead(device_address=module_id).write_data(wr_registers=my_mapper[f'filter_type1'][0], data=[my_filter])
    SpeWriteRead(device_address=module_id).write_data(wr_registers=my_mapper[f'type_breakage1'][0], data=[my_breakage])
    SpeWriteRead(device_address=module_id).write_data(wr_registers=my_mapper[f'input_mode1'][0], data=[mode1])
    SpeWriteRead(device_address=module_id).write_data(wr_registers=my_mapper[f'input_mode2'][0], data=[mode2])
    # SpeWriteRead(device_address=module_id).write_data(wr_registers=my_mapper[f'input_mode3'][0], data=[mode1])
    # SpeWriteRead(device_address=module_id).write_data(wr_registers=my_mapper[f'input_mode4'][0], data=[mode1])
    # SpeWriteRead(device_address=module_id).write_data(wr_registers=my_mapper[f'filter_type2'][0], data=[my_filter])
    # SpeWriteRead(device_address=module_id).write_data(wr_registers=my_mapper[f'type_breakage2'][0], data=[my_breakage])
    # SpeWriteRead(device_address=module_id).write_data(wr_registers=my_mapper[f'input_mode5'][0], data=[mode1])
    # SpeWriteRead(device_address=module_id).write_data(wr_registers=my_mapper[f'input_mode6'][0], data=[mode1])
    # SpeWriteRead(device_address=module_id).write_data(wr_registers=my_mapper[f'input_mode7'][0], data=[mode1])
    # SpeWriteRead(device_address=module_id).write_data(wr_registers=my_mapper[f'input_mode8'][0], data=[mode1])
    # SpeWriteRead(device_address=module_id).write_data(wr_registers=my_mapper[f'filter_type3'][0], data=[my_filter])
    # SpeWriteRead(device_address=module_id).write_data(wr_registers=my_mapper[f'type_breakage3'][0], data=[my_breakage])
    # SpeWriteRead(device_address=module_id).write_data(wr_registers=my_mapper[f'input_mode9'][0], data=[mode1])
    # SpeWriteRead(device_address=module_id).write_data(wr_registers=my_mapper[f'input_mode10'][0], data=[mode1])
    # SpeWriteRead(device_address=module_id).write_data(wr_registers=my_mapper[f'input_mode11'][0], data=[mode1])
    # SpeWriteRead(device_address=module_id).write_data(wr_registers=my_mapper[f'input_mode12'][0], data=[mode1])

    print(f'filter: {my_filter}, breakage: {my_breakage}, input mode1: {mode1}, input mode2: {mode2}')

    print('taking data for service operations. Waiting 3 seconds')
    print('')
    time.sleep(3)
    # for _ in range(10):
    #     response = SpeWriteRead(device_address=module_id).read_data(rd_registers=base_map_regs, count=66)
    #     #print(sum(quantity))
    #     print(response)


    count_iteration = 0
    try:
        print('Start of exchange...')
        while True:
            try:
                #for i in range(args.num_request):
                response = SpeWriteRead(device_address=module_id).read_data(rd_registers=configure_address[0], count=sum(quantity))[0]
                # value1 = ModbusFeatures.int16_list_to_float(response[2:4])
                # value2 = ModbusFeatures.int16_list_to_float(response[7:9])

                # value1_test = SpeWriteRead(device_address=module_id).read_data(rd_registers=my_mapper[f'value1'][0],
                #                                                             count=my_mapper[f'value1'][1])[0]
                # print(f'value1 = {value1_test}')
                # value2_test = SpeWriteRead(device_address=module_id).read_data(rd_registers=my_mapper[f'value2'][0],
                #                                                             count=my_mapper[f'value2'][1])[0]
                # print(f'value2 = {value2_test}')

                # print(f'{count_iteration}. value1 = {value1}, status1 = {response[4]}')
                # print(f'{count_iteration}. value2 = {value2}, status2 = {response[9]}')
                if response[4] == 14 or response[9] == 14:
                   count_ai_error += 1
                   time_error = time.perf_counter()
                   print(f'time = {time_error - start}, Timestamp1 = {response[5]}, AI1 Error = {response[4]}, count_error = {count_ai_error}')
                   print(f'time = {time_error - start}, Timestamp2 = {response[10]}, AI2 Error = {response[9]}, count_error = {count_ai_error}')

                count_iteration += 1
                time.sleep(args.polling_time)
            except IndexError:
                print('отсутствуют данные')
    except KeyboardInterrupt:
        end = time.perf_counter()
        print(f' Testing time = {end - start}, count_iteration = {count_iteration}, count_ai_error = {count_ai_error}')