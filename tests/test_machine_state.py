import time
import pytest
from src.baseclasses.modbus_command import ConnectModule
from src.baseclasses.response import Response
from configuration import COM_PORT, IP_ADDRESS, ID
from src.enums.global_enums import StateCode, ControlCode, StatusCode, RegisterNumber

# mu_210 = ConnectModule(comm='tcp', host=IP_ADDRESS, port=502).request_module()
#
# #перезагружаем тестируемый модуль
# mu_210.wr_holding_registers(address=0x1D6, values=[0])
# time.sleep(1)
# mu_210.wr_holding_registers(address=0x1D6, values=[1])
# time.sleep(2)

module_510 = ConnectModule(comm='com', com_settings=[f"COM{COM_PORT}", 115200, 8, 'N', 1]).request_module()
module_510.rd_holding_registers(address=0x0102, count=3, id=1)

# проверка режима INIT

@pytest.mark.parametrize('state, data, status', [
    (StateCode.INIT, None, StatusCode.NO_ERROR),
    (StateCode.INVALID_INIT, ControlCode.SAFEOP, StatusCode.INVALID_REQUESTED_STATE_CHANGE),
    (StateCode.INVALID_INIT, ControlCode.INIT, StatusCode.INVALID_REQUESTED_STATE_CHANGE),
    (StateCode.INVALID_INIT, ControlCode.PREOP, StatusCode.INVALID_REQUESTED_STATE_CHANGE),
    (StateCode.INVALID_INIT, ControlCode.BOOTSTRAP, StatusCode.INVALID_REQUESTED_STATE_CHANGE),
    (StateCode.INVALID_INIT, ControlCode.SAFEOP, StatusCode.INVALID_REQUESTED_STATE_CHANGE),
    (StateCode.INVALID_INIT, ControlCode.OP, StatusCode.INVALID_REQUESTED_STATE_CHANGE),
    (StateCode.INVALID_INIT, ControlCode.TEST_VALUE1, StatusCode.INVALID_REQUESTED_STATE_CHANGE),
    (StateCode.INVALID_INIT, ControlCode.TEST_VALUE2, StatusCode.INVALID_REQUESTED_STATE_CHANGE)
])
def test_init_invalid_state_change(data, state, status):
    """INIT - проверка возведения ошибки INVALID_REQUESTED_STATE_CHANGE при попытке перевести модуль
    в неправильное состояние SAFEOP и далее проверка отсутствия перехода с INVALID_REQUESTED_STATE_CHANGE
    в какое-либо другое состояние"""
    Response(module_510, ID).write_data(data, wr_registers=RegisterNumber.CONTROL).\
        assert_state_status_code(state, status, rd_registers=RegisterNumber.STATE, count=3)

@pytest.mark.parametrize('state, data, status', [
    (StateCode.INIT, ControlCode.RESET_ERRORS, StatusCode.NO_ERROR),
    (StateCode.INVALID_INIT, ControlCode.OP, StatusCode.INVALID_REQUESTED_STATE_CHANGE),
    (None, ControlCode.RESET_ERRORS, None),
    (StateCode.PREOP, ControlCode.PREOP, StatusCode.NO_ERROR)
])
def test_init_reset_invalid_state_change(data, state, status):
    """INIT - проверка сброса ошибки и перехода на корректное состояние PREOP"""
    # 31-37 - ждем реализации bootstrap
    # data_test_state_x102 = (1, 17, None, 3)
    # data_test_status_x104 = (0, 17, None, 0)
    Response(module_510, ID).write_data(data, wr_registers=RegisterNumber.CONTROL).\
        assert_state_status_code(state, status, rd_registers=RegisterNumber.STATE, count=3)

# проверка режима PREOP

@pytest.mark.parametrize('state, data, status', [
    (StateCode.PREOP, None, StatusCode.NO_ERROR),
    (StateCode.INVALID_PREOP, ControlCode.OP, StatusCode.INVALID_REQUESTED_STATE_CHANGE),
    (StateCode.INVALID_PREOP, ControlCode.INIT, StatusCode.INVALID_REQUESTED_STATE_CHANGE),
    (StateCode.INVALID_PREOP, ControlCode.PREOP, StatusCode.INVALID_REQUESTED_STATE_CHANGE),
    (StateCode.INVALID_PREOP, ControlCode.BOOTSTRAP, StatusCode.INVALID_REQUESTED_STATE_CHANGE),
    (StateCode.INVALID_PREOP, ControlCode.SAFEOP, StatusCode.INVALID_REQUESTED_STATE_CHANGE),
    (StateCode.INVALID_PREOP, ControlCode.OP, StatusCode.INVALID_REQUESTED_STATE_CHANGE),
    (StateCode.INVALID_PREOP, ControlCode.TEST_VALUE1, StatusCode.INVALID_REQUESTED_STATE_CHANGE),
    (StateCode.INVALID_PREOP, ControlCode.TEST_VALUE2, StatusCode.INVALID_REQUESTED_STATE_CHANGE)
])
def test_preop_invalid_state_change(data, state, status):
    """PREOP - проверка возведения ошибки INVALID_REQUESTED_STATE_CHANGE при попытке перевести модуль
    в неправильное состояние OP и далее проверка отсутствия перехода с INVALID_REQUESTED_STATE_CHANGE
    в какое-либо другое состояние"""
    Response(module_510, ID).write_data(data, wr_registers=RegisterNumber.CONTROL).\
        assert_state_status_code(state, status, rd_registers=RegisterNumber.STATE, count=3)

@pytest.mark.parametrize('state, data, status', [
    (StateCode.PREOP, ControlCode.RESET_ERRORS, StatusCode.NO_ERROR),
    (StateCode.INVALID_PREOP, ControlCode.BOOTSTRAP, StatusCode.INVALID_REQUESTED_STATE_CHANGE),
    (None, ControlCode.RESET_ERRORS, None),
    (StateCode.PREOP, ControlCode.PREOP, StatusCode.NO_ERROR),
    (StateCode.SAFEOP, ControlCode.SAFEOP, StatusCode.NO_ERROR)
])
def test_preop_reset_invalid_state_change(data, state, status):
    """PREOP - возведение ошибки при переходе на BOOTSTRAP, сброс ошибки и
      переход на корректное состояние SAFEOP"""
    Response(module_510, ID).write_data(data, wr_registers=RegisterNumber.CONTROL).\
        assert_state_status_code(state, status, rd_registers=RegisterNumber.STATE, count=3)

# проверка SAFEOP #191-224

@pytest.mark.parametrize('state, data, status', [
    (StateCode.SAFEOP, None, StatusCode.NO_ERROR),
    (StateCode.INVALID_SAFEOP, ControlCode.BOOTSTRAP, StatusCode.INVALID_REQUESTED_STATE_CHANGE),
    (StateCode.INVALID_SAFEOP, ControlCode.INIT, StatusCode.INVALID_REQUESTED_STATE_CHANGE),
    (StateCode.INVALID_SAFEOP, ControlCode.PREOP, StatusCode.INVALID_REQUESTED_STATE_CHANGE),
    (StateCode.INVALID_SAFEOP, ControlCode.BOOTSTRAP, StatusCode.INVALID_REQUESTED_STATE_CHANGE),
    (StateCode.INVALID_SAFEOP, ControlCode.SAFEOP, StatusCode.INVALID_REQUESTED_STATE_CHANGE),
    (StateCode.INVALID_SAFEOP, ControlCode.OP, StatusCode.INVALID_REQUESTED_STATE_CHANGE),
    (StateCode.INVALID_SAFEOP, ControlCode.TEST_VALUE1, StatusCode.INVALID_REQUESTED_STATE_CHANGE),
    (StateCode.INVALID_SAFEOP, ControlCode.TEST_VALUE2, StatusCode.INVALID_REQUESTED_STATE_CHANGE),
    (StateCode.SAFEOP, ControlCode.RESET_ERRORS, StatusCode.NO_ERROR),
    (StateCode.OP, ControlCode.OP, StatusCode.NO_ERROR)
])
def test_safeop_invalid_state_change_reset(data, state, status):
    """SAFEOP - проверка возведения ошибки INVALID_REQUESTED_STATE_CHANGE при попытке перевести модуль
    в неправильное состояние BOOTSTRAP, проверка отсутствия перехода с INVALID_REQUESTED_STATE_CHANGE
    в какое-либо другое состояние, сброс ошибки и переход на корректное состояние OP"""
    Response(module_510, ID).write_data(data, wr_registers=RegisterNumber.CONTROL).\
        assert_state_status_code(state, status, rd_registers=RegisterNumber.STATE, count=3)

# проверка OP  231-324
@pytest.mark.parametrize('state, data, status', [
    (StateCode.OP, None, StatusCode.NO_ERROR),
    (StateCode.INVALID_OP, ControlCode.BOOTSTRAP, StatusCode.INVALID_REQUESTED_STATE_CHANGE),
    (StateCode.INVALID_OP, ControlCode.INIT, StatusCode.INVALID_REQUESTED_STATE_CHANGE),
    (StateCode.INVALID_OP, ControlCode.PREOP, StatusCode.INVALID_REQUESTED_STATE_CHANGE),
    (StateCode.INVALID_OP, ControlCode.BOOTSTRAP, StatusCode.INVALID_REQUESTED_STATE_CHANGE),
    (StateCode.INVALID_OP, ControlCode.SAFEOP, StatusCode.INVALID_REQUESTED_STATE_CHANGE),
    (StateCode.INVALID_OP, ControlCode.OP, StatusCode.INVALID_REQUESTED_STATE_CHANGE),
    (StateCode.INVALID_OP, ControlCode.TEST_VALUE1, StatusCode.INVALID_REQUESTED_STATE_CHANGE),
    (StateCode.INVALID_OP, ControlCode.TEST_VALUE2, StatusCode.INVALID_REQUESTED_STATE_CHANGE),
    (StateCode.OP, ControlCode.RESET_ERRORS, StatusCode.NO_ERROR),
])
def test_op_invalid_state_change_reset(data, state, status):
    """OP - проверка возведения ошибки INVALID_REQUESTED_STATE_CHANGE при попытке перевести модуль
    в неправильное состояние BOOTSTRAP, проверка отсутствия перехода с INVALID_REQUESTED_STATE_CHANGE
    в какое-либо другое состояние, сброс ошибки и переход на корректное состояние OP"""
    Response(module_510, ID).write_data(data, wr_registers=RegisterNumber.CONTROL).\
        assert_state_status_code(state, status, rd_registers=RegisterNumber.STATE, count=3)

# 262 - 271

@pytest.mark.parametrize('state, data, status', [
    (StateCode.OP, None, StatusCode.NO_ERROR),
    (StateCode.INIT, ControlCode.INIT, StatusCode.NO_ERROR),
    (StateCode.PREOP, ControlCode.PREOP, StatusCode.NO_ERROR),
    (StateCode.SAFEOP, ControlCode.SAFEOP, StatusCode.NO_ERROR),
    (StateCode.OP, ControlCode.OP, StatusCode.NO_ERROR),
    (StateCode.PREOP, ControlCode.PREOP, StatusCode.NO_ERROR),
    (StateCode.SAFEOP, ControlCode.SAFEOP, StatusCode.NO_ERROR),
    (StateCode.OP, ControlCode.OP, StatusCode.NO_ERROR),
])
def test_op_state_change(data, state, status):
    """Проверка перехода по всем состояниями без ошибок начиная с OP"""
    Response(module_510, ID).write_data(data, wr_registers=RegisterNumber.CONTROL).\
        assert_state_status_code(state, status, rd_registers=RegisterNumber.STATE, count=3)


@pytest.mark.parametrize('state, data, status', [
    (StateCode.OP, None, StatusCode.NO_ERROR),
    (StateCode.INVALID_OP, ControlCode.TEST_VALUE1, StatusCode.UNKNOW_REQUEST_STATE),
    (StateCode.INVALID_OP, ControlCode.INIT, StatusCode.UNKNOW_REQUEST_STATE),
    (StateCode.INVALID_OP, ControlCode.PREOP, StatusCode.UNKNOW_REQUEST_STATE),
    (StateCode.INVALID_OP, ControlCode.SAFEOP, StatusCode.UNKNOW_REQUEST_STATE),
    (StateCode.INVALID_OP, ControlCode.OP, StatusCode.UNKNOW_REQUEST_STATE),
    (StateCode.INVALID_OP, ControlCode.TEST_VALUE1, StatusCode.UNKNOW_REQUEST_STATE),
    (StateCode.INVALID_OP, ControlCode.TEST_VALUE2, StatusCode.UNKNOW_REQUEST_STATE),
    (StateCode.OP, ControlCode.RESET_ERRORS, StatusCode.NO_ERROR),
    (StateCode.INVALID_OP, ControlCode.TEST_VALUE2, StatusCode.UNKNOW_REQUEST_STATE), # при записи 1000 не возникает ошибка
    (StateCode.OP, ControlCode.RESET_ERRORS, StatusCode.NO_ERROR),
    (StateCode.SAFEOP, ControlCode.SAFEOP, StatusCode.NO_ERROR)
])
def test_op_unknow_state_change(data, state, status):
    """Проверка возведения ошибки UNKNOW_REQUEST_STATE путем перехода в невалидное состояние.
    и переход на следующее состояние SAFEOP"""
    Response(module_510, ID).write_data(data, wr_registers=RegisterNumber.CONTROL).\
        assert_state_status_code(state, status, rd_registers=RegisterNumber.STATE, count=3)

# 302....

#329 - 379
@pytest.mark.parametrize('state, data, status', [
    (StateCode.SAFEOP, None, StatusCode.NO_ERROR),
    (StateCode.INVALID_SAFEOP, ControlCode.TEST_VALUE1, StatusCode.UNKNOW_REQUEST_STATE),
    (StateCode.INVALID_SAFEOP, ControlCode.INIT, StatusCode.UNKNOW_REQUEST_STATE),
    (StateCode.INVALID_SAFEOP, ControlCode.PREOP, StatusCode.UNKNOW_REQUEST_STATE),
    (StateCode.INVALID_SAFEOP, ControlCode.SAFEOP, StatusCode.UNKNOW_REQUEST_STATE),
    (StateCode.INVALID_SAFEOP, ControlCode.OP, StatusCode.UNKNOW_REQUEST_STATE),
    (StateCode.INVALID_SAFEOP, ControlCode.TEST_VALUE1, StatusCode.UNKNOW_REQUEST_STATE),
    (StateCode.INVALID_SAFEOP, ControlCode.TEST_VALUE2, StatusCode.UNKNOW_REQUEST_STATE),
    (StateCode.SAFEOP, ControlCode.RESET_ERRORS, StatusCode.NO_ERROR),
    (StateCode.INVALID_SAFEOP, ControlCode.TEST_VALUE2, StatusCode.UNKNOW_REQUEST_STATE), # не отработал ответ [8, 1000, 0]
    (StateCode.SAFEOP, ControlCode.RESET_ERRORS, StatusCode.NO_ERROR), # не отработал , ответ [8, 16, 0]
    (StateCode.SAFEOP, ControlCode.SAFEOP, StatusCode.NO_ERROR)
])
def test_safeop_unknow_state_change(data, state, status):
    """Проверка возведения ошибки UNKNOW_REQUEST_STATE путем перехода в невалидное состояние"""
    Response(module_510, ID).write_data(data, wr_registers=RegisterNumber.CONTROL).\
        assert_state_status_code(state, status, rd_registers=RegisterNumber.STATE, count=3)

#385 -
# @pytest.mark.parametrize('state, data, status', [
#     (StateCode.SAFEOP, None, StatusCode.NO_ERROR),
#     (StateCode.INVALID_SAFEOP, ControlCode.TEST_VALUE1, StatusCode.UNKNOW_REQUEST_STATE),
#     (StateCode.INVALID_SAFEOP, ControlCode.INIT, StatusCode.UNKNOW_REQUEST_STATE),
#     (StateCode.INVALID_SAFEOP, ControlCode.PREOP, StatusCode.UNKNOW_REQUEST_STATE),
#     (StateCode.INVALID_SAFEOP, ControlCode.SAFEOP, StatusCode.UNKNOW_REQUEST_STATE),
#     (StateCode.INVALID_SAFEOP, ControlCode.OP, StatusCode.UNKNOW_REQUEST_STATE),
#     (StateCode.INVALID_SAFEOP, ControlCode.TEST_VALUE1, StatusCode.UNKNOW_REQUEST_STATE),
#     (StateCode.INVALID_SAFEOP, ControlCode.TEST_VALUE2, StatusCode.UNKNOW_REQUEST_STATE),
#     (StateCode.SAFEOP, ControlCode.RESET_ERRORS, StatusCode.NO_ERROR),
#     (StateCode.INVALID_SAFEOP, ControlCode.TEST_VALUE2, StatusCode.UNKNOW_REQUEST_STATE),
#     (StateCode.SAFEOP, ControlCode.RESET_ERRORS, StatusCode.NO_ERROR)
# ])
# def test_safeop_unknow_state_change(data, state, status):
#     """Проверка возведения ошибки UNKNOW_REQUEST_STATE путем перехода в невалидное состояние"""
#     Response(module_510, ID).write_data(data, wr_registers=RegisterNumber.CONTROL).\
#         assert_state_status_code(state, status, rd_registers=RegisterNumber.STATE, count=3)