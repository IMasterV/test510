import sys
import time
import math

sys.path.append('/home/root/scripts')
from md_dataclasses.mb_32do import System, Do32
from md_dataclasses.mb_202 import Di202
from md_dataclasses.mb_102 import Ai102
from baseclasses.mapper import Mapper

from enums.do32_enums import OutMode
from baseclasses.response import SpeWriteRead

from baseclasses.modbus_operations import ConnectModule

from tests.do.configuration import MODULE_ID, MODULE_ID_4, IP_MODULE_202_1, IP_MODULE_202_2, IP_MODULE_202_3, IP_MODULE_202_4, IP_MODULE_102

from tests.do.utils import (split_32bit_to_4x8, set_logical_mode_do_spe, set_logical_mode_di_tcp, check_do_mask,
                            set_imp_gen_mode_do, set_pulse_counting_mode_202, set_filter_off_di, set_data_and_check_imp_gen_mode,
                            set_pwm_fast_mode_do, set_pwm_duty_do, set_type_sensor_102, set_ain_h_102, read_values_float_102,
                            set_pwm_slow_mode_do, set_pwm_period_do, set_period_measure_mode_di, reset_pulse_counting_di,
                            set_frequency_measure_mode_di)

di202 = Di202()
ai102 = Ai102()

conf_32do = Do32()
mapper_32do = Do32()

build = Mapper(MODULE_ID_4)
build.build_map_struct(conf_32do, mapper_32do)

module1 = ConnectModule(comm='tcp', host=IP_MODULE_202_1).request_module()
module2 = ConnectModule(comm='tcp', host=IP_MODULE_202_2).request_module()
module3 = ConnectModule(comm='tcp', host=IP_MODULE_202_3).request_module()
module4 = ConnectModule(comm='tcp', host=IP_MODULE_202_4).request_module()
module5_102 = ConnectModule(comm='tcp', host=IP_MODULE_102).request_module()


def test_do_pos_output_hs_pwm_duty():

    #set output_mode and frequency 32DO
    set_pwm_fast_mode_do(mapper_32do, MODULE_ID_4, OutMode.PWM_FAST)
    set_pwm_duty_do(mapper_32do, MODULE_ID_4, 1000, num_channels=8)

    set_type_sensor_102(ai102, module5_102, 5)
    set_ain_h_102(ai102, module5_102,10.0)
    time.sleep(2)

    values_voltage_max = read_values_float_102(ai102, module5_102)

    testing_data_duty = [3, 500, 900]
    for testing_duty in testing_data_duty:
        print(testing_duty)
        set_pwm_duty_do(mapper_32do, MODULE_ID_4, testing_duty, num_channels=8)

        time.sleep(3)

        values_voltage_current = read_values_float_102(ai102, module5_102)

        for i in range(len(values_voltage_max)):
            current_duty = (values_voltage_current[i] / values_voltage_max[i]) * 1000
            #print(f"{i} - current_duty={current_duty}")
            assert math.ceil(current_duty)-1 <= testing_duty <= math.ceil(current_duty)+1, f"{testing_duty}"


def test_do_pos_output_hs_pwm_frequency():

    device = SpeWriteRead(device_address=MODULE_ID)



    set_filter_off_di(di202, [module1, ], num_channels=8)
    set_frequency_measure_mode_di(di202, [module1, ], num_channels=8)
    reset_pulse_counting_di(di202, [module1, ], num_channels=8)

    #device.read_data(rd_registers=mapper_32do, count=)
    assert 1 == 1

if __name__ == "__main__":
    pass
    #test_do_pos_output_hs_pwm_duty()
    test_do_pos_output_hs_pwm_frequency()



