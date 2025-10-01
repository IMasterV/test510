import pytest
import sys

sys.path.append('/home/root/scripts')
from md_dataclasses.mb_32do import System, Do32
from md_dataclasses.mb_202 import Di202
from md_dataclasses.mb_102 import Ai102
from baseclasses.mapper import Mapper
from baseclasses.modbus_operations import ModbusFeatures
from baseclasses.response import SpeWriteRead
from baseclasses.modbus_operations import ConnectModule

from tests.do.configuration import MODULE_ID, IP_MODULE_202_1, IP_MODULE_202_2, IP_MODULE_202_3, IP_MODULE_202_4, IP_MODULE_102

@pytest.fixture(scope="session")
def configure_params_and_mapper():
    params_di202 = Di202()
    params_ai102 = Ai102()

    conf_32do = Do32()
    mapper_32do = Do32()

    build = Mapper(MODULE_ID)
    build.build_map_struct(conf_32do, mapper_32do)

    return params_di202, params_ai102, mapper_32do, conf_32do

@pytest.fixture(scope="session", autouse=True)
def read_system_params():
    system_params = System
    device = SpeWriteRead(device_address=MODULE_ID)

    system_params.name.value = ModbusFeatures.registers_to_ascii(device.read_data(rd_registers=system_params.name.addr,
                                                                           count=system_params.name.count)[0])

    system_params.firmware_ver.value = ModbusFeatures.registers_to_ascii(device.read_data(
        rd_registers=system_params.firmware_ver.addr,
        count=system_params.firmware_ver.count)[0])

    system_params.hardware_ver.value = ModbusFeatures.registers_to_ascii(device.read_data(
        rd_registers=system_params.hardware_ver.addr,
        count=system_params.hardware_ver.count)[0])

    # добавить проверку на имя
    print(f'address: {MODULE_ID}, name: {system_params.name.value}, '
          f'firmware: {system_params.firmware_ver.value}, hardware: {system_params.hardware_ver.value}')


@pytest.fixture(scope="session")
def connect_tcp_modules():
    module1 = ConnectModule(comm='tcp', host=IP_MODULE_202_1).request_module()
    module2 = ConnectModule(comm='tcp', host=IP_MODULE_202_2).request_module()
    module3 = ConnectModule(comm='tcp', host=IP_MODULE_202_3).request_module()
    module4 = ConnectModule(comm='tcp', host=IP_MODULE_202_4).request_module()
    module5_102 = ConnectModule(comm='tcp', host=IP_MODULE_102).request_module()

    return module1, module2, module3, module4, module5_102

@pytest.fixture(scope="class")
def env_for_test(configure_params_and_mapper, connect_tcp_modules):
    di202, ai102, mapper_32do, _ = configure_params_and_mapper
    module202_1, module202_2, module202_3, module202_4, module102 = connect_tcp_modules
    #modules_di = [module202_1, module202_2, module202_3, module202_4]

    return {
        'di202': di202,
        'ai102': ai102,
        'mapper_32do': mapper_32do,
        'module202_1': module202_1,
        'module202_2': module202_2,
        'module202_3': module202_3,
        'module202_4': module202_4,
        'module102': module102,
        #'modules_di': modules_di
    }