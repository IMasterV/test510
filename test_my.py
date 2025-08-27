import time
import pytest
import asyncio
import threading
import argparse

from baseclasses.spe_operations import SpeOperations
from baseclasses.response import SpeWriteRead
from baseclasses.modbus_operations import ConnectModule, ModbusFeatures
from collections import defaultdict
from enums.fai12_enums import InputMode, TypeFilter, Status
from enums.global_enums import StateCode, RegisterNumber
from baseclasses.mapper import Mapper







# async def timeout_task(seconds):
#     await asyncio.sleep(seconds)
#     raise TimeoutError("Время ожидания истекло")
#
# async def wait_for_timestamp_change(timestamp):
#     while True:
#         response = SpeWriteRead(device_address=4).read_data(
#             rd_registers=mapper_modbus_regs['timestamp1'], count=1
#         )[0]
#
#         if response != timestamp:
#             print(abs(response[0] - timestamp[0]))
#             assert abs(response[0] - timestamp[0]) in (10, 11, 12)
#             return
#
#         timestamp = response
#         await asyncio.sleep(0.1)  # чтобы не крутить цикл на 100%
#
# #Запуск
# async def monitor_with_timeout(timeout, timestamp):
#     await asyncio.wait_for(wait_for_timestamp_change(timestamp), timeout=timeout)
parser = argparse.ArgumentParser()
# Позиционные аргументы
parser.add_argument('polling_time', type=float, default=0.5)
parser.add_argument('just_name', type=int, default=0)

args = parser.parse_args()

print(args.polling_time)


response = SpeWriteRead(device_address=4).read_data(rd_registers=0x102, count=3)
print(response)


configure_address = [0x1000, 0x1001, 0x1002, 0x1004, 0x1005, 0x1006, 0x1008, 0x100A, 0x100B, 0x100C]
configure_name = ['filter_type', 'type_breakage', 'value1', 'status1', 'timestamp1', 'input_mode1',
                  'value2', 'status2', 'timestamp2', 'input_mode2']
quantity = [1, 1, 2, 1, 1, 1, 2, 1, 1, 1]

base_map_region = 0xfe00
base_map_regs = 0xff00

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

my_mapper = init_preop_safeop_op(configure_name, configure_address, quantity, base_map_region, base_map_regs)
#print(my_mapper)

default_values = SpeWriteRead(device_address=4).read_data(rd_registers=base_map_regs, count=sum(quantity))[0]
print(default_values)



# for i in range(10):
#     if i % 2 == 0:
#         SpeWriteRead(device_address=4).write_data(wr_registers=my_mapper['input_mode1'][0],
#                                                       data=[InputMode.CURRENT020])
#     else:
#         SpeWriteRead(device_address=4).write_data(wr_registers=my_mapper['input_mode1'][0],
#                                                       data=[InputMode.DISABLE])
#
#
#     # status = SpeWriteRead(device_address=4).read_data(rd_registers=my_mapper['status1'][0], count=my_mapper['status1'][1])[0]
#     # all(map(lambda x: True if x == 0 else False, status))
#
#     # taking data for service operations
#     status = SpeWriteRead(device_address=4).read_data(rd_registers=my_mapper['status1'][0], count=my_mapper['status1'][1])[0]
#     while status[0] != Status.NO_ERRORS:
#         status = SpeWriteRead(device_address=4).read_data(rd_registers=my_mapper['status1'][0], count=my_mapper['status1'][1])[0]
#         print(status)
#         time.sleep(0.5)

#time.sleep(3)

# SpeWriteRead(device_address=4).write_data(wr_registers=my_mapper['input_mode2'][0],
#                                           data=[InputMode.DISABLE])
# time.sleep(3)
# # подумать на json-файлом!!!!
# # 25 combinations

# [(3, 2, 3, '1'), ('filter', 'control', 'mode', 'inputs')]
#
# @pytest.mark.parametrize('filter, control, mode, timestamp', [
#     (TypeFilter.One, 0, 'input_mode1', 'timestamp1', (10, 11, 12)),
# ])

#num_channels = ('1', '5', '15', '9', '19', '59', '159')
num_channels = ('1', )

# 25 combinations
# type_filter = (0, 1, 2, 3, 4)
# control = (0, 0, 0, 0, 0)
# mode = (4, 4, 4, 4, 4)

type_filter = (0, 1, 2, 3)
control = (0, 0, 0, 0)
mode = (4, 4, 4, 4)

# SpeWriteRead(device_address=4).write_data(wr_registers=my_mapper[f'input_mode1'][0], data=[4])
#
# for _ in range(10):
#     # asyncio.run(monitor_with_timeout(timeout, timestamp))
#     try:
#         timestamp = SpeWriteRead(device_address=4).read_data(rd_registers=my_mapper['timestamp1'][0], count=1)[0]
#         while True:
#             response = SpeWriteRead(device_address=4).read_data(rd_registers=my_mapper['timestamp1'][0], count=1)[0]
#             if response != timestamp:
#                 print(abs(response[0] - timestamp[0]))
#                 # assert abs(response[0] - timestamp[0]) in (10, 11, 12)
#                 break
#             timestamp = response


# type_filter = (3, 0, 0, 3, 2, 3, 4, 1, 1, 2, 4, 0, 2, 0, 4, 4, 4, 1, 0, 2, 3, 2, 1, 3, 1)
# control = (2, 0, 2, 0, 1, 1, 0, 1, 2, 2, 1, 1, 0, 0, 2, 2, 2, 0, 0, 0, 1, 1, 1, 1, 0)
# mode = (2, 5, 4, 1, 1, 3, 3, 2, 5, 3, 4, 1, 2, 2, 5, 2, 1, 3, 3, 4, 4, 5, 4, 5, 1)
#timestamp = ((9, 10, 11, 12), )
# для каждой комбинации опеределить timestampы

params = [
    (channel, tf, ctl, md)
    for channel in num_channels
    for tf, ctl, md in zip(type_filter, control, mode)
]

@pytest.mark.parametrize('channel, type_f, ctrl, md', params)
def test_filter_one_channel_break_zero(channel, type_f, ctrl, md):
    config_delay = 0.5
    polling_delay = 0.001
    timeout_delay = 5


    #SpeWriteRead(device_address=4).write_data(wr_registers=base_map_regs, data=default_values)

    SpeWriteRead(device_address=4).write_data(wr_registers=my_mapper['filter_type'][0], data=[type_f])
    SpeWriteRead(device_address=4).write_data(wr_registers=my_mapper['type_breakage'][0], data=[ctrl])
    for _ in range(30):
        rd_status = SpeWriteRead(device_address=4).read_data(rd_registers=my_mapper[f'status1'][0], count=my_mapper[f'status1'][1])[0]
        print(f'rd_status = {rd_status}')
        time.sleep(0.2)

    #после изменения режима status входа показывает NO ERROR!!!
    for number in channel:
        SpeWriteRead(device_address=4).write_data(wr_registers=my_mapper[f'input_mode{number}'][0],
                                                  data=[md])
        time.sleep(config_delay)

    # taking data for service operations
    #time.sleep(0.5)
    for number in channel:
        rd_status = SpeWriteRead(device_address=4).read_data(rd_registers=my_mapper[f'status{number}'][0], count=my_mapper[f'status{number}'][1])[0]
        #print(f'rd_status = {rd_status}')

        while rd_status[0] != Status.NO_ERRORS:
            rd_status = SpeWriteRead(device_address=4).read_data(rd_registers=my_mapper[f'status{number}'][0], count=my_mapper[f'status{number}'][1])[0]
            time.sleep(config_delay)
            print(f'status = {rd_status[0]}')
            if (rd_status[0] != Status.BREAK) or (rd_status[0] != Status.VALUE_TOO_LOW):
                break

    # for _ in range(10):
    #     timestamp = SpeWriteRead(device_address=4).read_data(rd_registers=my_mapper['timestamp1'][0], count=1)[0]
    #     print(timestamp)
    #     time.sleep(0.1)

    # max_tries = 3
    delay = 0.1
    # timeout = 3
    time.sleep(3)
    for _ in range(10):
        #asyncio.run(monitor_with_timeout(timeout, timestamp))
        try:
            timestamp = SpeWriteRead(device_address=4).read_data(rd_registers=my_mapper['timestamp1'][0], count=1)[0]
            while True:
                response = SpeWriteRead(device_address=4).read_data(rd_registers=my_mapper['timestamp1'][0], count=1)[0]
                if response != timestamp:
                    print(abs(response[0] - timestamp[0]))
                    #assert abs(response[0] - timestamp[0]) in (10, 11, 12)
                    break
                timestamp = response
                time.sleep(polling_delay)

                #asyncio.run(timeout_task(timeout))
            # добавить обработку
        except IndexError:
            print(f'Повтор через {delay} сек...')
            time.sleep(delay)
            response = SpeWriteRead(device_address=4).read_data(rd_registers=my_mapper['timestamp1'][0], count=1)[0]
            print(f'Timestamp = {response[0]}')
        except TimeoutError:
            print(f'Ошибка {TimeoutError}')


#test_filter_one_channel_break_zero()








#
# type_fil = SpeWriteRead(device_address=4).read_data(rd_registers=my_mapper['filter_type'][0], count=my_mapper['filter_type'][1])[0]
# print(f'filter = {type_fil}')
#
# type_b = SpeWriteRead(device_address=4).read_data(rd_registers=my_mapper['type_breakage'][0], count=my_mapper['type_breakage'][1])[0]
# print(f'type_breakage = {type_b}')
#
# value1 = SpeWriteRead(device_address=4).read_data(rd_registers=my_mapper['value1'][0], count=my_mapper['value1'][1])[0]
# print(f'value1 = {value1}')
#
# SpeWriteRead(device_address=4).write_data(wr_registers=my_mapper['input_mode1'][0],
#                                           data=[InputMode.DISABLE])
#
# status1 = SpeWriteRead(device_address=4).read_data(rd_registers=my_mapper['status1'][0], count=my_mapper['status1'][1])[0]
# print(f'status1 = {status1}')
#
# timestamp1 = SpeWriteRead(device_address=4).read_data(rd_registers=my_mapper['timestamp1'][0], count=my_mapper['timestamp1'][1])[0]
# print(f'timestamp1 = {timestamp1}')
#
#
#
# value1 = SpeWriteRead(device_address=4).read_data(rd_registers=my_mapper['value2'][0], count=my_mapper['value2'][1])[0]
# print(f'value2 = {value1}')
#
# status1 = SpeWriteRead(device_address=4).read_data(rd_registers=my_mapper['status2'][0], count=my_mapper['status2'][1])[0]
# print(f'status2 = {status1}')
#
# timestamp1 = SpeWriteRead(device_address=4).read_data(rd_registers=my_mapper['timestamp2'][0], count=my_mapper['timestamp2'][1])[0]
# print(f'timestamp2 = {timestamp1}')
#
# SpeWriteRead(device_address=4).write_data(wr_registers=my_mapper['filter_type'][0], data=[0])
# SpeWriteRead(device_address=4).write_data(wr_registers=my_mapper['type_breakage'][0], data=[0])
# SpeWriteRead(device_address=4).write_data(wr_registers=my_mapper['input_mode1'][0], data=[0])

























#
#
# def init_preop_safeop_op(configure_address, map_region):
#     for i in range(4):
#         SpeWriteRead(device_address=4).write_data(wr_registers=RegisterNumber.CONTROL, data=[1 << i])
#
#         # configure mapper in preop
#         if 1 << i == 2:
#             # SpeWriteRead(device_address=4).write_data(wr_registers=map_region[0], data=conf_regs)
#             for j in range(len(configure_address)):
#                 SpeWriteRead(device_address=4).write_data(wr_registers=map_region[j], data=[configure_address[j]])
#
#
# init_preop_safeop_op(configure_address, map_region)
#
#
# default_values=[]
# for i in
#     SpeWriteRead(device_address=4).read_data(rd_registers=map_regs[0], count=len(map_regs))[0]
#
# print(default_values)
# SpeWriteRead(device_address=4).write_data(wr_registers=mapper_modbus_regs['input_mode1'],
#                                               data=[InputMode.CURRENT020])
# # taking data for service operations
# # запрашивать статус значения канала!!! изменить константу
# time.sleep(3)












# response = SpeWriteRead(device_address=4).read_data(rd_registers=RegisterNumber.STATE, count=3)
# print(response)
# SpeWriteRead(device_address=4).write_data(wr_registers=RegisterNumber.CONTROL, data=[StateCode.INIT])
# SpeWriteRead(device_address=4).write_data(wr_registers=RegisterNumber.CONTROL, data=[StateCode.PREOP])
# # configure mapper
# for i in range(len(configure_address)):
#     SpeWriteRead(device_address=4).write_data(wr_registers=map_region[i], data=[configure_address[i]])
#
# SpeWriteRead(device_address=4).write_data(wr_registers=RegisterNumber.CONTROL, data=[StateCode.SAFEOP])
# SpeWriteRead(device_address=4).write_data(wr_registers=RegisterNumber.CONTROL, data=[StateCode.OP])
# # конфигурация длинее маппера . Увеличить адреса маппера - вроде совпадает
# SpeWriteRead(device_address=4).write_data(wr_registers=table_modbus_regs['filter_type'], data=[InputMode.DISABLE])
# SpeWriteRead(device_address=4).write_data(wr_registers=MapperFai12.INPUT_MODE1, data=[InputMode.CURRENT020])
# inputmode = SpeWriteRead(device_address=4).read_data(rd_registers=table_modbus_regs['inputmode1'], count=1)[0]
# print(inputmode)
# # taking data for service operations
# time.sleep(2)
#
# timestamp = SpeWriteRead(device_address=4).read_data(rd_registers=Fai12Regs.TIMESTAMP1, count=1)[0]
# print(timestamp)
# # while True:
# #     response = SpeWriteRead(device_address=4).read_data(rd_registers=Fai12Regs.TIMESTAMP1, count=1)[0]
# #     print(response)
# #     if response != timestamp:
# #         print(abs(response[0] - timestamp[0]))
# #         break
# #     timestamp = response
# #
# # #return to INIT
# SpeWriteRead(device_address=4).write_data(wr_registers=RegisterNumber.CONTROL, data=[StateCode.INIT])






# conf_regs = [Fai12Regs.FILTER_TYPE, Fai12Regs.TYPE_BREAKAGE,
#              Fai12Regs.INPUT_MODE1, Fai12Regs.INPUT_MODE5, Fai12Regs.INPUT_MODE9]






#map_regs = [i for i in range(0xff00, 0xff00 + len(Fai12Regs))]





# name_regs = ['filter_type', 'type_breakage', 'input1_mode', 'input2_mode', 'input3_mode', 'input4_mode',
#              'input5_mode', 'input6_mode', 'input7_mode', 'input8_mode', 'input9_mode',
#              'input10_mode', 'input11_mode', 'input12_mode']
# table_modbus_regs = defaultdict(int)
# for i in zip(name_regs, map_regs):
#     table_modbus_regs[i[0]] = i[1]


# #init, preop, safeop, op
# for i in range(4):
#     SpeWriteRead(device_address=4).write_data(wr_registers=0x0103, data=[1 << i])
#
#     # configure mapper in preop
#     if 1 << i == 2:
#         #SpeWriteRead(device_address=4).write_data(wr_registers=map_region[0], data=conf_regs)
#         for j in range(len(conf_regs)):
#             SpeWriteRead(device_address=4).write_data(wr_registers=map_region[j], data=[conf_regs[j]])
#
# SpeWriteRead(device_address=4).write_data(wr_registers=table_modbus_regs['filter_type'], data=[0])
# SpeWriteRead(device_address=4).write_data(wr_registers=table_modbus_regs['input1_mode'], data=[4])
#
# response = SpeWriteRead(device_address=4).read_data(rd_registers=4101, count=1)
# print(f'timestamp1 = {response}')
# # taking data for service operations
# time.sleep(2)
#
# timestamp = SpeWriteRead(device_address=4).read_data(rd_registers=4101, count=1)[0]
# while True:
#     response = SpeWriteRead(device_address=4).read_data(rd_registers=4101, count=1)[0]
#
#     if response != timestamp:
#         print(abs(response[0] - timestamp[0]))
#         break
#     timestamp = response
#
# #return to INIT
# SpeWriteRead(device_address=4).write_data(wr_registers=0x0103, data=[1])
#
#
# # @pytest.mark.parametrize('state, data, status', [
# #     (StateCode.INIT, ControlCode.INIT, StatusCode.NO_ERROR),
# #     (StateCode.PREOP, ControlCode.PREOP, StatusCode.NO_ERROR),
# #     (StateCode.INIT, ControlCode.INIT, StatusCode.NO_ERROR)
# # ])
# def test_filter_one_channel_break_zero():
#     SpeWriteRead(device_address=1).write_data(wr_registers=0x0103, data=[data])
#     response = SpeWriteRead(device_address=1).read_data(rd_registers=RegisterNumber.STATE, count=3)
#
#     assert response[0]['register_values'][0] == state
#     assert response[0]['register_values'][2] == status













# SpeWriteRead(device_address=4).write_data(wr_registers=0x0103, data=[2])
# for j in range(len(conf_regs)):
#     SpeWriteRead(device_address=4).write_data(wr_registers=map_region[j], data=[conf_regs[j]])
#     time.sleep(0.5)
# #SpeWriteRead(device_address=4).write_data(wr_registers=map_region[0], data=[4102])
#
# SpeWriteRead(device_address=4).write_data(wr_registers=0x0103, data=[4])
# SpeWriteRead(device_address=4).write_data(wr_registers=0x0103, data=[8])
#
# response = SpeWriteRead(device_address=4).read_data(rd_registers=map_regs[0], count=1)
# print(f'mode input1 = {response}')
# SpeWriteRead(device_address=4).write_data(wr_registers=map_regs[0], data=[4])
# response = SpeWriteRead(device_address=4).read_data(rd_registers=map_regs[0], count=1)
# print(f'mode input1 = {response}')
# response = SpeWriteRead(device_address=4).read_data(rd_registers=4101, count=1)
# print(f'timestamp1 = {response}')
# time.sleep(4)
# response = SpeWriteRead(device_address=4).read_data(rd_registers=4101, count=1)
# print(f'timestamp1 = {response}')
# time.sleep(3)
# response = SpeWriteRead(device_address=4).read_data(rd_registers=4101, count=1)
# print(f'timestamp1 = {response}')


# SpeWriteRead(device_address=4).write_data(wr_registers=table_modbus_regs['input1_mode'], data=[4])
# for i in range(20):
#     response = SpeWriteRead(device_address=4).read_data(rd_registers=4101, count=1)
#     print(response)
#     time.sleep(0.5)

#
#
#
#
#
#
# SpeWriteRead(device_address=4).write_data(wr_registers=0xff02, data=[4])
# SpeWriteRead(device_address=4).write_data(wr_registers=0xff03, data=[4])
# SpeWriteRead(device_address=4).write_data(wr_registers=0xff04, data=[4])
# time.sleep(3)
#
# regs_timestamps_inputs = [4101, 4107, ]
# # timestamp input 1
# response = SpeWriteRead(device_address=4).read_data(rd_registers=4101, count=1, num=100)
#
# for i in range(len(response)):
#     if i == 0:
#         continue
#
#     if response[i] != response[i - 1]:
#         print(response[i][0] - response[i - 1][0])






#SpeWriteRead(device_address=4).write_data(wr_registers=0x1000, data=[0])




#
#
# response = SpeWriteRead(device_address=4).read_data(rd_registers=0xFF00, count=1)
# print(response)
#
# SpeWriteRead(device_address=4).write_data(wr_registers=0xFF00, data=[1])
#
# response = SpeWriteRead(device_address=4).read_data(rd_registers=0xFF00, count=1)
# print(response)

#
# response = SpeWriteRead(device_address=4).read_data(rd_registers=0xFF00, count=1)
# print(response)



# for i in range(10):
#     response = SpeWriteRead(device_address=4).read_data(rd_registers=4101, count=1, num=500)
#     new_list = []
#     for i in range(len(response)):
#         if i == 0:
#             continue
#         if response[i][1] != response[i - 1][1]:
#             new_list.append(i)
#
#     print(sum(map(lambda x: x[0], response[new_list[0]:new_list[1]])))


# for i in range(1000):
#     response = SpeWriteRead(device_address=4).read_data(rd_registers=4101, count=1)
#     print(f'{i} - {response}')
#     time.sleep(0.5)

# for i in range(len(response)):
#     print(response[i]['register_values'])




# response = SpeWriteRead(device_address=4).read_data(rd_registers=4102, count=1)
# print(response)

# response = SpeWriteRead(device_address=4).read_data(rd_registers=16, count=8)
# print(ModbusFeatures.registers_to_ascii(response[0]['register_values']))







# req = [
#     bytes([0x01, 0x03, 0x00, 0x00, 0x00, 0x10, 0x44, 0x06]),
#     bytes([0x02, 0x03, 0x00, 0x00, 0x00, 0x10, 0x44, 0x35]),
#     bytes([0x03, 0x03, 0x00, 0x00, 0x00, 0x10, 0x45, 0xE4]),
#     bytes([0x04, 0x03, 0x00, 0x00, 0x00, 0x10, 0x44, 0x53]),
# ]
#
# myrequest = ModbusFeatures.create_modbus_rtu_request(device_address=2, function_code=3, register_address=0x0102, data_count=3)
# rr = SpeOperations()
#
# #myrequest2 = ModbusFeatures.create_modbus_rtu_request(device_address=1, function_code=16, register_address=0x0103, data_count=[1])
#
# print(tuple(rr.auto_request_response(requests=[bytes(myrequest)], num=1)))



# module_210 = ConnectModule(comm='tcp', host='10.2.25.5', port=502).request_module()
#
# module_210.rd_holding_registers(address=0xF000, count=8, id=1)
#
# module_210.wr_holding_registers