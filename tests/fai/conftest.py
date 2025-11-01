import pytest
import sys

sys.path.append('/home/root/scripts')
from md_dataclasses.mb_12fai import System, Fai12
from md_dataclasses.mb_202 import Di202
from baseclasses.mapper import Mapper
from baseclasses.modbus_operations import ModbusFeatures
from baseclasses.response import SpeWriteRead
from baseclasses.modbus_operations import ConnectModule

from tests.fai.configuration import MODULE_ID

@pytest.fixture(scope="session")
def configure_params_and_mapper():
    """
    Создание экземпляров классов данных для модулей 12FAI.
    Конфигурация маппера модуля 12FAI по конфигурационным параметрам
    и перевод модуля 12FAI в режим OP.
    :return:
    mapper_12fai: параметры маппера 12fai (addr, count, value)
    conf_12fai: параметры конфигурационные 12fai (addr, count, value)
    """

    # params_di202 = Di202()
    # params_ai102 = Ai102()

    conf_12fai = Fai12()
    mapper_12fai = Fai12()

    Mapper(MODULE_ID).build_map_struct(conf_12fai, mapper_12fai)

    return mapper_12fai, conf_12fai


@pytest.fixture(scope="session", autouse=True)
def read_system_params():
    """
        Чтение сервисных параметров модуля (name, firmware, hardware)
    :return:
    """

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


@pytest.fixture(scope="class")
def env_for_test(configure_params_and_mapper):
    mapper_12fai, _ = configure_params_and_mapper
    #module202_1, module202_2, module202_3, module202_4, module102 = connect_tcp_modules
    #modules_di = [module202_1, module202_2, module202_3, module202_4]

    return {
        'mapper_12fai': mapper_12fai
        #'modules_di': modules_di
    }