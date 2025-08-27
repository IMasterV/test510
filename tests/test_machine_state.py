import pytest
import time
import sys

sys.path.append('/home/root/scripts')

from baseclasses.response import SpeWriteRead

#from baseclasses.spe_operations import SpeOperations
#from baseclasses.modbus_operations import ConnectModule, ModbusFeatures
from enums.global_enums import StateCode, ControlCode, StatusCode, RegisterNumber


@pytest.mark.parametrize('state, data, status', [
    (StateCode.INIT, ControlCode.INIT, StatusCode.NO_ERROR),
    (StateCode.PREOP, ControlCode.PREOP, StatusCode.NO_ERROR),
    (StateCode.INIT, ControlCode.INIT, StatusCode.NO_ERROR)
])
def test_init_invalid_state_change(state, data, status):
    SpeWriteRead(device_address=1).write_data(wr_registers=0x0103, data=[data])
    response = SpeWriteRead(device_address=1).read_data(rd_registers=RegisterNumber.STATE, count=3)

    assert response[0]['register_values'][0] == state
    assert response[0]['register_values'][2] == status


#test_init_invalid_state_change()
#myrequest1 = ModbusFeatures.create_modbus_rtu_request(device_address=1, function_code=3, register_address=0x0102, data_count=3)
#rr = SpeOperations()



#myrequest2 = ModbusFeatures.create_modbus_rtu_request(device_address=1, function_code=16, register_address=0x0103, data_count=[1])
#response = rr.auto_request_response(requests=[bytes(myrequest1)], num=1)
#print(tuple(response))




# def init_invalid_state_change():
#     myrequest2 = ModbusFeatures.create_modbus_rtu_request(device_address=1, function_code=16, register_address=0x0103, data_count=[1])
#     response_write = tuple(rr.auto_request_response(requests=[bytes(myrequest2)], num=1))
# #    print(response)
#
#     response = tuple(rr.auto_request_response(requests=[bytes(myrequest1)], num=1))
#     print(response)
#
#     assert response[0][0] == 1
#     assert response[0][2] == 0
#
#     myrequest2 = ModbusFeatures.create_modbus_rtu_request(device_address=1, function_code=16, register_address=0x0103, data_count=[2])
#     response_write = tuple(rr.auto_request_response(requests=[bytes(myrequest2)], num=1))
# #    print(response)
#
#     response = tuple(rr.auto_request_response(requests=[bytes(myrequest1)], num=1))
#     print(response)
#
#     assert response[0][0] == 2
#     assert response[0][2] == 0


#init_invalid_state_change()


