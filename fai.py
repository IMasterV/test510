from baseclasses.response import SpeWriteRead
from baseclasses.modbus_operations import ConnectModule, ModbusFeatures

import json
import re
import time
from md_dataclasses.modbus_database import Fai12, System
from baseclasses.mapper import Mapper
from enums.fai12_enums import InputMode
#from md_dataclasses import fields

from baseclasses.response import SpeWriteRead
from baseclasses.modbus_operations import ConnectModule, ModbusFeatures


conf_fai12 = Fai12()
mapper_fai12 = Fai12()
system_params = System

module_id = 1

build = Mapper(module_id)

build.build_map_struct(conf_fai12, mapper_fai12)


system_params.fsm_current_state.value = SpeWriteRead(device_address=module_id).read_data(
                                                        rd_registers=system_params.fsm_current_state.addr,
                                                               count=system_params.fsm_current_state.count)[0]
print(system_params.fsm_current_state.value)


# DATA TEST
# iterations = range(1, 26)
# type_filter = (3, 0, 0, 3, 2, 3, 4, 1, 1, 2, 4, 0, 2, 0, 4, 4, 4, 1, 0, 2, 3, 2, 1, 3, 1)
# control = (2, 0, 2, 0, 1, 1, 0, 1, 2, 2, 1, 1, 0, 0, 2, 2, 2, 0, 0, 0, 1, 1, 1, 1, 0)
# modes = (2, 5, 4, 1, 1, 3, 3, 2, 5, 3, 4, 1, 2, 2, 5, 2, 1, 3, 3, 4, 4, 5, 4, 5, 1)

# type_filter = (1, 2, 0)
# control = (1, 0, 0)
# modes = (2, 5, 4)
type_filter = (0,1,2,3)
control = (0,0,0,0)
modes = (2,2,2,2)
# две ошибки
# 1 - когда ctrl = 2 добавляется везде одна миллисекунда формула 7 + (6+6)*4
# когда ctrl = 0 формула 6 + (6+0)*4
# 2 - режим фильтра = 4 подвисает (timeout полагаю из-за частого опроса)

#num_channels = ('12', '5', '15', '9', '19', '59', '159')
num_channels = ('1235',)
#, '15', '9', '19', '59', '159'
# ctrl 2: 21, 22, 23
# ctrl 1:
timeout_tf_channel = {0: 6, 1: 10, 2: 18, 3: 34, 4: 122}
timestamp_ctrl_channel = {0: 0, 1: 0, 2: 6}

# 6 + (timeout_tf + 0)*num_channel

correct_timestamps = {0: (10, 11, 12, 13), 1: (14, 15, 16, 17), 2: (22, 23, 24, 25),
                      3: (38, 39, 40, 41), 4: (127, 128, 129, 130)}


###################################


# def wait_for_timestamp_update(device_address, field, correct_values, tf, input_num):
#
#     for _ in range(10):
#         try:
#             modbus_input_field.timestamp.value = SpeWriteRead(device_address=module_id).read_data(
#                 rd_registers=modbus_input_field.timestamp.addr,
#                 count=modbus_input_field.timestamp.count)[0]
#
#             while True:
#                 response = SpeWriteRead(device_address=module_id).read_data(
#                     rd_registers=modbus_input_field.timestamp.addr,
#                     count=modbus_input_field.timestamp.count)[0]
#
#                 if response != modbus_input_field.timestamp.value:
#                     print(f'it. timestamp{num} = {(response[0] - modbus_input_field.timestamp.value[0]) % 65536}')
#                     try:
#                         assert (response[0] - modbus_input_field.timestamp.value[0]) % 65536 in correct_timestamps[tf]
#                     except AssertionError:
#                         print('')
#                         print(f'Ошибка AssertionError')
#                         # count_error_assertions += 1
#                 return

system_params.name.value = ModbusFeatures.registers_to_ascii(SpeWriteRead(device_address=module_id).
                                                read_data(rd_registers=system_params.name.addr,
                                                          count=system_params.name.count)[0])

system_params.firmware_ver.value = ModbusFeatures.registers_to_ascii(SpeWriteRead(device_address=module_id).
                                                     read_data(rd_registers=system_params.firmware_ver.addr,
                                                               count=system_params.firmware_ver.count)[0])

system_params.hardware_ver.value = ModbusFeatures.registers_to_ascii(SpeWriteRead(device_address=module_id).
                                                     read_data(rd_registers=system_params.hardware_ver.addr,
                                                               count=system_params.hardware_ver.count)[0])

print(f'address: {module_id}, name: {system_params.name.value}, '
      f'firmware: {system_params.firmware_ver.value}, hardware: {system_params.hardware_ver.value}')

count_error_assertions = 0
count_index_error = 0
count_timeout_error = 0

TIMEOUT_SECONDS = 10


def get_group_number(channel: int) -> int:
    if 1 <= channel <= 4:
        return 1
    elif 5 <= channel <= 8:
        return 2
    elif 9 <= channel <= 12:
        return 3
    else:
        raise ValueError(f"Некорректный канал: {channel}")

# def parse_params(text: str):
#     pattern = r"tf=(\d+),\s*ctrl=(\d+),\s*mode=(\d+),\s*num_channel=(\w+)"
#     match = re.search(pattern, text)
#     if not match:
#         raise ValueError(f"Не удалось разобрать строку: {text}")
#
#     tf, ctrl, mode, num_channel = match.groups()
#     return int(tf), int(ctrl), int(mode), num_channel
#
#
# def unique_by_num_channel(steps):
#     seen = set()
#     for case in steps:
#         *_, num_channel = parse_params(case["step"])
#         if num_channel not in seen:
#             seen.add(num_channel)
#             yield case
#
# @pytest.mark.parametrize("case", unique_by_num_channel(test_steps))
# def test_cyclic_time(case):
#     text = "Установить tf=0, ctrl=0, mode=2, num_channel=1235, input=1"
#     tf, ctrl, mode, num_channel = parse_params(text)

test_steps = []
for num_channel in num_channels:
    for i, (tf, ctrl, mode) in enumerate(zip(type_filter, control, modes), start=1):
        # выключение режимов аналоговых входов

        groups = {
            1: {"voltage": 0, "current": 0},
            2: {"voltage": 0, "current": 0},
            3: {"voltage": 0, "current": 0},
        }

        writer = SpeWriteRead(device_address=module_id)
        for channel in range(1, 13):
            modbus_input_field = getattr(mapper_fai12, f"input{channel}")
            writer.write_data(wr_registers=modbus_input_field.mode.addr,
                                                              data=[InputMode.DISABLE])

        # драйвер полностью пересобирает очередь
        time.sleep(0.05)

        # ЗАПИСЬ ТЕСТОВЫХ ДАННЫХ
        # настройка фильтра и обрыва для каждой группы
        for channel in range(1, 4):
            modbus_group_field = getattr(mapper_fai12, f"group{channel}")
            writer.write_data(wr_registers=modbus_group_field.typeFilter.addr,
                                                              data=[tf])

            writer.write_data(wr_registers=modbus_group_field.typeBreakage.addr,
                                                              data=[ctrl])

        # установка режимов для тестируемых входов
        for channel in num_channel:
            channel = int(channel)
            modbus_input_field = getattr(mapper_fai12, f"input{channel}")
            writer.write_data(wr_registers=modbus_input_field.mode.addr,
                                                              data=[mode])

            group_id = get_group_number(channel)

            if mode in (InputMode.VOLTAGE01, InputMode.VOLTAGE010):
                groups[group_id]["voltage"] += 1
            elif mode in (InputMode.CURRENT020, InputMode.CURRENT420, InputMode.CURRENT05):
                groups[group_id]["current"] += 1


        print('taking data for service operations. Waiting 3 seconds')
        time.sleep(3)

        # проверяем все режимы входов
        for channel in range(1, 13):
            modbus_input_field = getattr(mapper_fai12, f"input{channel}")
            modbus_input_field.mode.value = SpeWriteRead(device_address=module_id).read_data(
                                                            rd_registers=modbus_input_field.mode.addr,
                                                                count=modbus_input_field.mode.count)[0]

            # если режим входа включен, то начинаем чтение timestamps
            if modbus_input_field.mode.value[0] != InputMode.DISABLE:
                group_id = get_group_number(channel)
                #
                expected_timestamp = 6 + (timeout_tf_channel[tf] + timestamp_ctrl_channel[ctrl]) * \
                                     groups[group_id]["voltage"] + \
                                     timeout_tf_channel[tf] * groups[group_id]["current"]

                print(
                    f'try to request timestamp{channel}, tf={tf}, ctrl={ctrl}, mode={mode} num_channels='
                    f'{groups[group_id]["voltage"] + groups[group_id]["current"]}')

                test_steps.append({
                    "step": f"Установить tf={tf}, ctrl={ctrl}, mode={mode}, num_channel={num_channel}, input={channel}",
                    "expected": f"Ожидаемое время = {expected_timestamp}"
                })
                for j in range(10):
                    try:
                        modbus_input_field.timestamp.value = SpeWriteRead(device_address=module_id).read_data(
                                                                rd_registers=modbus_input_field.timestamp.addr,
                                                                    count=modbus_input_field.timestamp.count)[0]

                        start_time = time.time()
                        # ожидаем когда timestamp изменится
                        while True:
                            response = SpeWriteRead(device_address=module_id).read_data(
                                rd_registers=modbus_input_field.timestamp.addr,
                                count=modbus_input_field.timestamp.count)[0]

                            if response != modbus_input_field.timestamp.value:
                                try:
                                    #assert (response[0] - modbus_input_field.timestamp.value[0]) % 65536 in correct_timestamps[tf]
                                    assert (response[0] - modbus_input_field.timestamp.value[0]) % 65536 >= (expected_timestamp - 4) and (
                                                       response[0] - modbus_input_field.timestamp.value[0]) % 65536 <= expected_timestamp

                                except AssertionError:
                                    print(f'{j}. Error: AssertionError, {(response[0] - modbus_input_field.timestamp.value[0]) % 65536}')
                                    print(f'checktimestamp == {expected_timestamp}')

                                    # print(f'Start Timestamp = {modbus_input_field.timestamp.value[0]}')
                                    # print(f'Current Timestamp = {response[0]}')
                                    #print(f'Timestamp = {}')
                                    count_error_assertions += 1
                                break

                            if time.time() - start_time > TIMEOUT_SECONDS:
                                count_timeout_error += 1
                                raise TimeoutError(f'{j}. receive timestamp{channel} timeout')

                    except IndexError as e:
                        print(f'{j}. Error: {e}, repeat in 1 seconds')
                        time.sleep(1)
                        count_index_error += 1
                        # ошибку index error заложить в SpeWrite!!!
                    except TimeoutError as e:
                        print(f'{j}. Error: {e}, repeat in 1 seconds')
                        time.sleep(1)
                        break


print(f'count_assert = {count_error_assertions}, count_index = {count_index_error}, count_timeout = {count_timeout_error}')
print(test_steps)






#for num in range(1, 13):









