import time
import sys
import math
import pytest

sys.path.append('/home/root/scripts')
from baseclasses.response import SpeWriteRead

from tests.do.utils import (split_32bit_to_4x8, set_mode_do32, check_do_mask, set_mode_202, set_filter_off_di,
                            set_data_and_check_imp_gen_mode, set_pwm_duty_do, set_type_sensor_102, set_ain_h_102,
                            read_values_float_102, set_pwm_period_do, reset_pulse_counting_di)

from enums.di202_enums import DInputMode202
from enums.ai102_enums import AInputMode102
from enums.do32_enums import OutMode
from tests.do.configuration import MODULE_ID, MODULE_ID_4

class TestPosDO:
    @pytest.fixture(autouse=True)
    def setup_env(self, env_for_test):
        self.di202 = env_for_test['di202']
        self.ai102 = env_for_test['ai102']
        self.mapper_32do = env_for_test['mapper_32do']
        self.module202_1 = env_for_test['module202_1']
        self.module202_2 = env_for_test['module202_2']
        self.module202_3 = env_for_test['module202_3']
        self.module202_4 = env_for_test['module202_4']
        self.module102 = env_for_test['module102']
        self.modules_di = [self.module202_1, self.module202_2, self.module202_3, self.module202_4]

    def test_do_pos_output_logic_mode(self):

        set_mode_do32(MODULE_ID, self.mapper_32do, OutMode.LOGICAL, num_channels=32)
        set_mode_202(self.di202, self.modules_di, value=DInputMode202.LOGICAL, num_channels=8)

        device = SpeWriteRead(device_address=MODULE_ID)
        for offset in range(32):
            if offset <= 15:
                self.mapper_32do.do.out_mask.value = [1 << offset, 0]
            else:
                self.mapper_32do.do.out_mask.value = [0, 1 << (offset - 16)]

            # set bitmask_output 32do
            device.write_data(
                wr_registers=self.mapper_32do.do.out_mask.addr,
                data=[*self.mapper_32do.do.out_mask.value])

            # check bitmask_output 32do
            bitmask = device.read_data(
                rd_registers=self.mapper_32do.do.outputs_states.addr,
                count=self.mapper_32do.do.outputs_states.count)[0]


            assert bitmask == self.mapper_32do.do.out_mask.value, f'number output={offset + 1}'

            # separate bitmask_output
            parts = split_32bit_to_4x8(self.mapper_32do.do.out_mask.value)
            time.sleep(0.01)

            # Один 32DO подключен к 4 модулям по 8 входов
            module_index = offset // 8

            if module_index < len(self.modules_di):
                self.di202.di.input_states.value = self.modules_di[module_index].rd_holding_registers(
                    address=self.di202.di.input_states.addr,
                    count=self.di202.di.input_states.count
                )

                # print(f'output_mask = {mapper_32do.do.out_mask.value}, module{module_index + 1} = '
                #       f'{di202.di.input_states.value}, parts_module_index = {parts[module_index]}')

                assert parts[module_index] == self.di202.di.input_states.value, f'number output={offset + 1}'

        check_do_mask(MODULE_ID, self.mapper_32do, self.di202, self.modules_di, [65535, 65535])

        time.sleep(0.1)

        check_do_mask(MODULE_ID, self.mapper_32do, self.di202, self.modules_di, [0, 0])

    def test_do_pos_output_imp_gen_mode(self):

        # test параметра impgen_count_out!!!!

        # set img_gen mode for 3 outputs
        set_mode_do32(MODULE_ID, self.mapper_32do, OutMode.IMP_GEN, num_channels=3)

        # set pulse_counting mode for 8 inputs
        set_mode_202(self.di202, [self.module202_1, ], value=DInputMode202.PULSE_COUNTING, num_channels=8)

        # set filter bounce off for 20 inputs
        set_filter_off_di(self.di202, [self.module202_1, ], num_channels=20)

        for channel in range(1, 4):
            # for data_test_freq, data_test_num in ((1, 3),(10, 10), (60000, 65535)):
            for data_test_freq, data_test_num in ((1, 2), (2, 4), (3, 6)):

                set_data_and_check_imp_gen_mode(MODULE_ID, self.module202_1, self.di202,
                                                self.mapper_32do, data_test_freq,
                                                data_test_num, num_channels=channel)

    @pytest.mark.skip(reason="module doesn't connect")
    def test_do_pos_output_hs_pwm_duty(self):

        #set output_mode and frequency 32DO
        set_mode_do32(MODULE_ID_4, self.mapper_32do, OutMode.PWM_FAST, num_channels=8)
        set_pwm_duty_do(self.mapper_32do, MODULE_ID_4, 1000, num_channels=8)

        set_type_sensor_102(self.ai102, self.module102, AInputMode102.VOLTAGE010)
        set_ain_h_102(self.ai102, self.module102,10.0)
        time.sleep(2)

        values_voltage_max = read_values_float_102(self.ai102, self.module102)

        testing_data_duty = [3, 500, 900]
        for testing_duty in testing_data_duty:
            set_pwm_duty_do(self.mapper_32do, MODULE_ID_4, testing_duty, num_channels=8)

            time.sleep(3)

            values_voltage_current = read_values_float_102(self.ai102, self.module102)

            for i in range(len(values_voltage_max)):
                current_duty = (values_voltage_current[i] / values_voltage_max[i]) * 1000
                assert math.ceil(current_duty)-1 <= testing_duty <= math.ceil(current_duty)+1, f"{testing_duty}"

    def test_do_pos_output_pwm_period(self):
        # test duty???
        # duty = 1000 ?

        set_filter_off_di(self.di202, self.modules_di)
        set_mode_202(self.di202, self.modules_di, value=DInputMode202.PERIOD_MEASURE, num_channels=8)
        reset_pulse_counting_di(self.di202, self.modules_di)  # ?? надо ли

        set_mode_do32(MODULE_ID, self.mapper_32do, OutMode.PWM_SLOW, num_channels=32)
        set_pwm_duty_do(self.mapper_32do, MODULE_ID, pwm_duty=500)

        data_test_pwm_period = (1000, 30000, 60000)
        for pwm_period_value in data_test_pwm_period:
            set_pwm_period_do(self.mapper_32do, MODULE_ID, pwm_period=pwm_period_value)

            time.sleep((pwm_period_value / 1000) + 2)

            # Читаем счетчик всех модулей
            for module in self.modules_di:
                result = []
                for channel in range(1, 8 + 1):
                    modbus_input_field = getattr(self.di202, f"di{channel}")

                    response = module.rd_holding_registers(address=modbus_input_field.counter_value.addr,
                                                           count=modbus_input_field.counter_value.count)
                    result.append(response)
                assert all(
                    x in ([pwm_period_value - 1, 0], [pwm_period_value, 0], [pwm_period_value + 1, 0]) for x in result), \
                    f"Некорректный результат: {result}"

        set_pwm_duty_do(self.mapper_32do, MODULE_ID, pwm_duty=0)

        #test_do_pos_output_pwm_period()

































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

