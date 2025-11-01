import time
import sys
import math
import pytest

sys.path.append('/home/root/scripts')
from tests.fai.utils_fai import set_mode_fai12, set_tf_ctrl, calculate_expected_timestamps, read_timestamp
from tests.fai.configuration import MODULE_ID, TIMEOUT_TIMESTAMP
from baseclasses.response import SpeWriteRead



from md_dataclasses.mb_12fai import Fai12, System
from baseclasses.mapper import Mapper
from enums.fai12_enums import InputMode


num_combination = ([1,2,3],)
type_filter = (0,1,2,3)
control = (0,0,0,0)
modes = (2,2,2,2)

# conf_fai12 = Fai12()
# mapper_fai12 = Fai12()
# system_params = System
#
# module_id = 4
#
# build = Mapper(module_id)
#
# build.build_map_struct(conf_fai12, mapper_fai12)
#
# response = SpeWriteRead(device_address=4).read_data(rd_registers=0x102, count=3)[0]
# print(response)

#SpeWriteRead(device_address=4).write_data(wr_registers=0x103, data=[20])

# writer = SpeWriteRead(device_address=4)
# print(mapper_fai12.input1.mode.addr)
# modbus_input_field = getattr(mapper_fai12, f"input1")
#writer.write_data(wr_registers=modbus_input_field.mode.addr, data=[1])


class TestPosFAI:
    @pytest.fixture(autouse=True)
    def setup_env(self, env_for_test):
        self.mapper_12fai = env_for_test['mapper_12fai']

    @pytest.mark.parametrize(
        "channel_list,tf,ctrl,mode",
        [
            (channel_list, tf, ctrl, mode)
            for channel_list in num_combination
            for tf, ctrl, mode in zip(type_filter, control, modes)
        ]
        # Не используем кастомные id - пусть pytest генерирует сам
    )
    def test_timestamp_fai(self, channel_list, tf, ctrl, mode):

        # выключение режимов аналоговых входов
        set_mode_fai12(MODULE_ID, self.mapper_12fai,
                       channels=range(1,13), mode=InputMode.DISABLE)

        # драйвер полностью пересобирает очередь
        time.sleep(0.05)

        # устанавливаем тип фильтра и контроль обрыва
        set_tf_ctrl(MODULE_ID, self.mapper_12fai,
                    groups=range(1, 4), tf=tf, ctrl=ctrl)

        # установка режимов для тестируемых входов
        set_mode_fai12(MODULE_ID, self.mapper_12fai,
                       channels=channel_list, mode=mode)

        print('taking data for service operations. Waiting 3 seconds')
        time.sleep(3)

        testing_data = calculate_expected_timestamps(MODULE_ID, self.mapper_12fai, tf, ctrl)

        for channel, expected_timestamp in testing_data.items():
            #print(f'channel = {channel}, expected = {expected_timestamp}')
            for j in range(10):
                try:
                    current_timestamp = read_timestamp(MODULE_ID, self.mapper_12fai, channel)

                    start_time = time.time()
                    while True:
                        response = read_timestamp(MODULE_ID, self.mapper_12fai, channel)

                        if response != current_timestamp:
                            try:
                                # сравниваем ожидаемое время с фактическим
                                assert (response - current_timestamp) % 65536 >= (
                                            expected_timestamp - 4) and (
                                               response - current_timestamp) % 65536 <= expected_timestamp+1
                            # если ожидаемое циклическое время не равно фактическому увеличиваем счетчик ошибок
                            # и выходим из цикла while и сравниваем следующее прочитанное время измерение
                            except AssertionError:
                                print(f'{j}.AssertionError, current_timestamp = {(response - current_timestamp) % 65536}, '
                                      f'expected_timestamp = {expected_timestamp}, channel = {channel}')
                                raise AssertionError(f'{j}.AssertionError, current_timestamp = {(response - current_timestamp) % 65536}, '
                                      f'expected_timestamp = {expected_timestamp}, channel = {channel}')
                                #count_error_assertions += 1
                            break

                        if time.time() - start_time > TIMEOUT_TIMESTAMP:
                            #count_timeout_error += 1
                            raise TimeoutError(f'{j}. receive timestamp{channel} timeout')
                # если ошибка чтения timestamp (ответ пустой), пробуем еще раз через 1 секунду
                except IndexError as e:
                    print(f'{j}. Error: {e}, repeat in 1 seconds')
                    time.sleep(1)
                    #count_index_error += 1
                    # ошибку index error заложить в SpeWrite!!!
                # если timestamp не изменяется за время TIMEOUT_TIMESTAMP, пробуем еще раз через 1 секунду
                except TimeoutError as e:
                    print(f'{j}. Error: {e}, repeat in 1 seconds')
                    time.sleep(1)
                    break
