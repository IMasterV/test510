import time
import pytest
from src.baseclasses.modbus_command import ConnectModule
from src.baseclasses.response import Response
from configuration import COM_PORT, IP_ADDRESS, ID

mu_210 = ConnectModule(comm='tcp', host=IP_ADDRESS, port=502).request_module()

#перезагружаем тестируемый модуль
mu_210.wr_holding_registers(address=0x1D6, values=[0])
time.sleep(1)
mu_210.wr_holding_registers(address=0x1D6, values=[1])
time.sleep(2)

module_510 = ConnectModule(comm='com', com_settings=[f"COM{COM_PORT}", 115200, 8, 'N', 1]).request_module()

@pytest.mark.parametrize('state, data, status', [
    (1, None, 0), (17, 4, 17), (17, 1, 17), (17, 2, 17), (17, 3, 17), (17, 4, 17),
    (17, 8, 17), (17, 10, 17), (17, 1000, 17), (17, (0, 49215), 17)
])
def test_init_1(data, state, status):
    """INIT_проверка отсутствия перехода"""
    Response(module_510, ID).write_data(data, wr_registers=0x103).\
        assert_state_status_code(state, status, rd_registers=0x102, count=3)

@pytest.mark.parametrize('state, data, status', [
    (1, 16, 0),  (17, 8, 17), (None, 16, None), (2, 2, 0)
])
def test_init_2(data, state, status):
    """INIT_начало проверки переходов без ошибок"""
    # 31-37 - ждем реализации bootstrap
    # data_test_state_x102 = (1, 17, None, 3)
    # data_test_status_x104 = (0, 17, None, 0)
    Response(module_510, ID).write_data(data, wr_registers=0x103).\
        assert_state_status_code(state, status, rd_registers=0x102, count=3)




#Response(module_510, ID).assert_state_status_code(state=1, status=0, rd_registers=0x102, count=3)
# def test_init_1():
#     """INIT_проверка отсутствия перехода"""
#     massiv = (4, 1, 2, 3, 4, 8, 10, 1000, (0, 49215))
#
#     Response(module_510, ID).assert_state_status_code(state=1, status=0, rd_registers=0x102, count=3)
#     for data in massiv:
#         Response(module_510, ID).write_data(data, wr_registers=0x103)\
#             .assert_state_status_code(state=17, status=17, rd_registers=0x102, count=3)

# def test_init_2():
#     """INIT_начало проверки переходов без ошибок"""
#     massiv = ((16, 1, 0), (8, 17, 17), (16, None, None), (2, 2, 0))
#     # 31-37 - ждем реализации bootstrap
#     # data_test_state_x102 = (1, 17, None, 3)
#     # data_test_status_x104 = (0, 17, None, 0)
#     for data, state, status in massiv:
#         if state is None:
#             Response(module_510, ID).write_data(data, wr_registers=0x103)
#         else:
#             Response(module_510, ID).write_data(data, wr_registers=0x103)\
#                 .assert_state_status_code(state, status, rd_registers=0x102, count=3)
#
# def test_preop_1():
#     """PREOP_начало проверки переходов без ошибки"""
#     massiv = (1, 2, 3, 4, 8, 10, 1000, (0, 49215))
#
#     print('PREOP_начало проверки переходов без ошибки')
#     Response(module_510, ID).write_data(data=8, wr_registers=0x103) \
#         .assert_state_status_code(state=18, status=17, rd_registers=0x102, count=3)
#
#     print('PREOP_начало проверки в ошибке INVALID_REQUESTED_STATE_CHANGE (17)')
#     for data in massiv:
#         Response(module_510, ID).write_data(data, wr_registers=0x103)\
#                 .assert_state_status_code(state=18, status=17, rd_registers=0x102, count=3)
#
# test_init_1()
# test_init_2()
# test_preop_1()
# def test_preop_2(some):
#     print('PREOP_возобновление (1/2) проверки переходов без ошибки')
#     data_test_x103 = (16, 3, 16, 2, 4)
#     data_test_state_x102 = (2, 18, None, 2, 4)
#     data_test_status_x104 = (0, 17, None, 0, 0)
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
#     print('PREOP_прерывание (2/2) проверки переходов без ошибки')


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
