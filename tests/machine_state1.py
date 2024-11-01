import time
from pymodbus import (
    Framer)
from pymodbus.client import (ModbusSerialClient, ModbusTcpClient)
from src.baseclasses.modbus_command import ModbusFunction, MyFirstClass
from src.baseclasses.response import Response
def request_module(comm, host='', port=0, com_settings = None, framer=Framer.SOCKET):
    """Run sync client."""
    # activate debugging
    #pymodbus_apply_logging_config("DEBUG")
    if comm == 'tcp':
        client = ModbusTcpClient(
                    host,
                    port=port,
                    framer=framer,
                    timeout=10,
                    retries=4,
                    # retry_on_empty=False,y
                    # source_address=("localhost", 0),
                )
        print(f'connect to {host}')
        client.connect()
        return ModbusFunction(client)

    if comm == 'com':
        client = ModbusSerialClient(
            com_settings[0],
            #framer=framer,
            # timeout=10,
            # retries=3,
            # retry_on_empty=False,
            # close_comm_on_error=False,.
            # strict=True,
            baudrate=com_settings[1],
            bytesize=com_settings[2],
            parity=com_settings[3],
            stopbits=com_settings[4],
            # handle_local_echo=False,
        )
        print(f"connect to {com_settings[0]}")
        client.connect()
        return ModbusFunction(client)


#подключаемся к модулю 210
mu_210 = request_module(comm='tcp', host=ip_address, port=502, framer=Framer.SOCKET)

#перезагружаем модуль 510
mu_210.wr_holding_registers(address=470, values=[0], id=1)
time.sleep(1)
mu_210.wr_holding_registers(address=470, values=[1], id=1)

# try:
#     while True:
#         try:
#             port = int(input('Номер COM-порта: '))
#         except ValueError:
#             print('Значение должно быть целочисленным')
#         else:
#             break
#
#     while True:
#         try:
#             id = int(input('Адрес прибора: '))
#         except ValueError:
#             print('Значение должно быть целочисленным')
#         else:
#             break
# except EOFError:
#     mu_210.wr_holding_registers(address=470, values=[0], id=1)
#подключаемся к модулю 510
module_510 = request_module(comm='com', com_settings=[f"COM{com_port}", 115200, 8, 'N', 1], framer=Framer.SOCKET)

a = MyFirstClass()

def test_init_1(some):
    """Проверка INIT"""
    # activate debugging
    # pymodbus_apply_logging_config()

    fsm = module_510.rd_holding_registers(address=0x102, count=3, id=id)
    response = Response(fsm)
    response.assert_state_status_code(1, 0)
    # assert fsm[0] == 1, MachineErrorMessages.WRONG_STATE_CODE.value
    # assert fsm[2] == 0, MachineErrorMessages.WRONG_STATUS_CODE.value
    print('INIT_начало проверки в ошибке INVALID_REQUESTED_STATE_CHANGE (17)')
    # (29811, 29556)
    data_test_x103 = (4, 1, 2, 3, 4, 8, 10, 1000, (0, 49215))
    for i in range(len(data_test_x103)):
        if isinstance(data_test_x103[i], tuple):
            module_510.wr_holding_registers(address=0x103, values=[data_test_x103[i][0], data_test_x103[i][1]], id=id)
        else:
            module_510.wr_holding_registers(address=0x103, values=[data_test_x103[i]], id=id)
        time.sleep(0.1)
        fsm = module_510.rd_holding_registers(address=0x102, count=3, id=id)
        assert fsm[0] == 17, MachineErrorMessages.WRONG_STATE_CODE.value
        assert fsm[2] == 17, MachineErrorMessages.WRONG_STATUS_CODE.value
    print('INIT_конец проверки в ошибке INVALID_REQUESTED_STATE_CHANGE (17)', end='\n')



# def test_init_2(some):
#     print('INIT_начало проверки переходов без ошибок')
#     data_test_x103 = (16, 8, 16, 2)
#     data_test_state_x102 = (1, 17, 1, 2)
#     data_test_status_x104 = (0, 17, 0, 0)
#     # 31-37 - ждем реализации bootstrap
#     # data_test_state_x102 = (1, 17, None, 3)
#     # data_test_status_x104 = (0, 17, None, 0)
#     for i in range(len(data_test_x103)):
#         if data_test_state_x102[i] is None:
#             module_510.wr_holding_registers(address=0x103, values=[data_test_x103[i]], id=id)
#             continue
#
#         module_510.wr_holding_registers(address=0x103, values=[data_test_x103[i]], id=id)
#         time.sleep(0.2)
#         fsm = module_510.rd_holding_registers(address=0x102, count=3, id=id)
#         assert fsm[0] == data_test_state_x102[i]
#         assert fsm[2] == data_test_status_x104[i]
#     print('INIT_прерывание (1/2) проверки переходов без ошибок')

def test_preop_1(some):
    print('PREOP_начало проверки переходов без ошибки')
    module_510.wr_holding_registers(address=0x103, values=[8], id=id)
    fsm = module_510.rd_holding_registers(address=0x102, count=3, id=id)
    assert fsm[0] == 18
    assert fsm[2] == 17
    print('PREOP_прерывание (1/2) проверки переходов без ошибки')

    print('PREOP_начало проверки в ошибке INVALID_REQUESTED_STATE_CHANGE (17)')
    data_test_x103 = (1, 2, 3, 4, 8, 10, 1000, (0, 49215))
    for i in range(len(data_test_x103)):
        if isinstance(data_test_x103[i], tuple):
            module_510.wr_holding_registers(address=0x103, values=[data_test_x103[i][0], data_test_x103[i][1]], id=id)
        else:
            module_510.wr_holding_registers(address=0x103, values=[data_test_x103[i]], id=id)
        time.sleep(0.1)
        fsm = module_510.rd_holding_registers(address=0x102, count=3, id=id)
        assert fsm[0] == 18
        assert fsm[2] == 17
    print('PREOP_конец проверки в ошибке INVALID_REQUESTED_STATE_CHANGE (17)')

def test_preop_2(some):
    print('PREOP_возобновление (1/2) проверки переходов без ошибки')
    data_test_x103 = (16, 3, 16, 2, 4)
    data_test_state_x102 = (2, 18, None, 2, 4)
    data_test_status_x104 = (0, 17, None, 0, 0)
    for i in range(len(data_test_x103)):
        if data_test_state_x102[i] is None:
            module_510.wr_holding_registers(address=0x103, values=[data_test_x103[i]], id=id)
            continue

        module_510.wr_holding_registers(address=0x103, values=[data_test_x103[i]], id=id)
        time.sleep(0.2)
        fsm = module_510.rd_holding_registers(address=0x102, count=3, id=id)
        assert fsm[0] == data_test_state_x102[i]
        assert fsm[2] == data_test_status_x104[i]
    print('PREOP_прерывание (2/2) проверки переходов без ошибки')


# def test_safeop(some):
#     print('SAFEOP_начало проверки переходов без ошибки')
#     module_510.wr_holding_registers(address=0x103, values=[3], id=id)
#     fsm = module_510.rd_holding_registers(address=0x102, count=3, id=id)
#     assert fsm[0] == 20
#     assert fsm[2] == 17
#     print('SAFEOP_прерывание (1/2) проверки переходов без ошибки')
#
#     print('SAFEOP_начало проверки в ошибке INVALID_REQUESTED_STATE_CHANGE (17)')
#     data_test_x103 = (1, 2, 3, 4, 8, 10, 1000, (0, 49215))
#     for i in range(len(data_test_x103)):
#         if isinstance(data_test_x103[i], tuple):
#             module_510.wr_holding_registers(address=0x103, values=[data_test_x103[i][0], data_test_x103[i][1]], id=id)
#         else:
#             module_510.wr_holding_registers(address=0x103, values=[data_test_x103[i]], id=id)
#         time.sleep(0.1)
#         fsm = module_510.rd_holding_registers(address=0x102, count=3, id=id)
#         assert fsm[0] == 20
#         assert fsm[2] == 17
#     print('SAFEOP_конец проверки в ошибке INVALID_REQUESTED_STATE_CHANGE (17)')
#
#     print('SAFEOP_возобновление (1/2) проверки переходов без ошибки')
#     module_510.wr_holding_registers(address=0x103, values=[8], id=id)
#     time.sleep(0.5)
#     fsm = module_510.rd_holding_registers(address=0x102, count=3, id=id)
#     assert fsm[0] == 8
#     assert fsm[2] == 0
#     print('SAFEOP_прерывание (2/2) проверки переходов без ошибки')
#
#     mu_210.wr_holding_registers(address=470, values=[0], id=1)
#test_init()

# def test_bootstrap():
#
#     print('BOOTSTRAP_начало проверки в ошибке INVALID_REQUESTED_STATE_CHANGE (17)')
#     data_fmscontrolstate_x103 = [2, 1, 3, 4, 8, 10, 1000, 1.5, 'тест']
#     for i in range(len(data_fmscontrolstate_x103)):
#         test.wr_holding_registers(address=0x103, values=[data_fmscontrolstate_x103[i]], id=id)
#         time.sleep(0.2)
#         fsm = test.rd_holding_registers(address=0x102, count=3, id=id)
#         assert fsm[0] == 17
#         assert fsm[2] == 17
#         time.sleep(0.2)
#     print('BOOTSTRAP_конец проверки в ошибке INVALID_REQUESTED_STATE_CHANGE (17)', end='\n')
#
#     print('BOOTSTRAP_начало проверки переходов без ошибок')
#     data_fmsControlState_x103 = [16, 8, 16, 4, 16, 2, 16, 3]
#     data_fmsCurrentState_x102 = [3, 19, None, 19, None, 19, None, 3]
#     data_fmsStatus_x104 = [0, 17, None, 17, None, 17, None, 0]
#     for i in range(len(data_fmscontrolstate_x103)):
#         if data_fmsCurrentState_x102[i] is None:
#             test.wr_holding_registers(address=0x103, values=[data_fmsControlState_x103[i]], id=id)
#             continue
#
#         test.wr_holding_registers(address=0x103, values=[data_fmsControlState_x103[i]], id=id)
#         time.sleep(0.2)
#         fsm = test.rd_holding_registers(address=0x102, count=3, id=id)
#         assert fsm[0] == data_fmsCurrentState_x102[i]
#         assert fsm[2] == data_fmsStatus_x104[i]
#
#     print('BOOTSTRAP_прерывание проверки переходов без ошибок', end='\n')
#     print('BOOTSTRAP_начало проверки переходов в несуществующие состояния')
#     test.wr_holding_registers(address=0x103, values=[10], id=id)
#     time.sleep(0.2)
#     fsm = test.rd_holding_registers(address=0x102, count=3, id=id)
#     assert fsm[0] == 19
#     assert fsm[2] == 18
#     print('BOOTSTRAP_прерывание проверки переходов в несуществующие состояния')
#     print('BOOTSTRAP_начало проверки в ошибке INVALID_REQUESTED_STATE_CHANGE (18)')
#     data_fmsControlState_x103 = [1, 2, 3, 4, 8, 10, 1000, 1.5, 'тест']
#     for i in range(len(data_fmsControlState_x103)):
#         test.wr_holding_registers(address=0x103, values=[data_fmsControlState_x103[i]], id=id)
#         time.sleep(0.2)
#         fsm = test.rd_holding_registers(address=0x102, count=3, id=id)
#         assert fsm[0] == 19
#         assert fsm[2] == 18
#     print('BOOTSTRAP_конец проверки в ошибке INVALID_REQUESTED_STATE_CHANGE (18)')
