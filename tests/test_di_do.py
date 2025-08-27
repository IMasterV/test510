import sys
import pytest
import time

sys.path.append('/home/root/scripts')

from baseclasses.response import SpeWriteRead
from baseclasses.spe_operations import SpeOperations
from baseclasses.modbus_operations import ConnectModule, ModbusFunction, ModbusRequest
from pymodbus.register_write_message import WriteMultipleRegistersRequest, WriteMultipleRegistersResponse

# # from scripts.baseclasses.response import Response
# # from scripts.baseclasses.spe_operations import SpeOperations
# from baseclasses.modbus_operations import ConnectModule, ModbusFunction, ModbusRequest
# from pymodbus.register_write_message import WriteMultipleRegistersRequest, WriteMultipleRegistersResponse

#rr = SpeOperations()

#myrequest = ModbusRequest(2, 0x0103).generate_modbus_write_request([1])
#response = tuple(rr.auto_request_response(requests=[myrequest], num=1))

#response = Response(device_address=2).read_data(rd_registers=0x0102, count=3)
#print(response) 

#response = Response(device_address=2).write_data(wr_registers=0x0103, data=[2])

#response = Response(device_address=2).read_data(rd_registers=0x0102, count=3)
#print(response) 



#myrequest = ModbusRequest(1, 0x0103).generate_modbus_write_request([5])
#print(list(myrequest))

#myrequest = ModbusRequest(2, 0x0033).generate_modbus_read_request(2)
#print(list(myrequest))


#myrequest = [1, 16, 1, 2, 0, 0, 0, 53, 40]
#response = rr.auto_request_response(requests=[myrequest], num=1)
#print(tuple(response))


#Response(device_address=3).write_data(0x0103, 4)


#response = Response(device_address=2).read_data(rd_registers=0x0102, count=2)
#print(response) 


#response = Response(device_address=2).read_data(rd_registers=0x002, count=2)
#print(response)


#module_210 = ConnectModule(comm='tcp', host='10.77.151.35', port=502).request_module()
#module_210.rd_holding_registers(address=0xF000, count=8, id=1)


#reset 510
#module_210.rd_holding_registers(address=470, count=2, id=1)
#module_210.wr_holding_registers(address=470, values=[0, 0], id=1)
#time.sleep(5)
#module_210.wr_holding_registers(address=470, values=[255], id=1)


module_210_412 = ConnectModule(comm='tcp', host='10.77.151.35', port=502).request_module()
module_210_410 = ConnectModule(comm='tcp', host='10.77.151.36', port=502).request_module()
#
response = SpeWriteRead(device_address=2).read_data(rd_registers=0x0102, count=3)
#print(response)

SpeWriteRead(device_address=2).write_data(wr_registers=0x0103, data=[1])
SpeWriteRead(device_address=2).write_data(wr_registers=0x0103, data=[2])
SpeWriteRead(device_address=2).write_data(wr_registers=0x0103, data=[4])
SpeWriteRead(device_address=2).write_data(wr_registers=0x0103, data=[8])

response = SpeWriteRead(device_address=2).read_data(rd_registers=0x0102, count=3)
#print(response)
module_210_412.wr_holding_registers(address=470, values=[0, 0], id=1)
module_210_410.wr_holding_registers(address=470, values=[0], id=1)

def test_32di_412():
    count = 0
    for j in range(2):
        for i in range(16):
            count += 1
            module_210_412.wr_holding_registers(address=470, values=[0, 0], id=1)

            if count > 24:
                return

            #print(f'Номер выхода {count}')
            bitmask_output = [0, 0]
            bitmask_output[j] = 1 << i

            module_210_412.wr_holding_registers(address=470, values=bitmask_output, id=1)
            #time.sleep(0.5)
            response = SpeWriteRead(device_address=2).read_data(rd_registers=0xFF00, count=2)
            #time.sleep(0.5)
            #print(response)
            assert response[0]['register_values'] == bitmask_output

def test_32di_410():
    count = 0
    for i in range(16):
        count += 1
        module_210_410.wr_holding_registers(address=470, values=[0], id=1)

        if count > 8:
            return

        #print(f'Номер выхода {count}')
        bitmask_output = 1 << i

        module_210_410.wr_holding_registers(address=470, values=[bitmask_output], id=1)
        # time.sleep(0.5)
        response = SpeWriteRead(device_address=2).read_data(rd_registers=0xFF00, count=2)
        #print(response)
        #time.sleep(0.5)

        bitmask_output = 1 << i + 8
        assert response[0]['register_values'][1] == bitmask_output

        #module_210_410.wr_holding_registers(address=470, values=[0], id=1)

# test_32di_412()
# test_32di_410()


# module_210_412.wr_holding_registers(address=470, values=[65535, 255], id=1)
# module_210_410.wr_holding_registers(address=470, values=[65535], id=1)
# response = SpeWriteRead(device_address=2).read_data(rd_registers=0xFF00, count=2)
# #time.sleep(0.01)
# print(response)




# def test_di_do():
#     maskoutput = 0
#     #read MaskInput in 0x1000 register
#     response = Response(device_address=2).read_data(rd_registers=0x1000, count=2)
#     print(response)
#
#     #write Output1
#     maskoutput |= (1 << 0)
#     module_210.wr_holding_registers(address=470, values=[maskoutput, 0], id=1)
#
#     response = Response(device_address=2).read_data(rd_registers=0x1000, count=2)
#     print(response)
#
#     #write Output2
#     maskoutput |= (1 << 1)
#     module_210.wr_holding_registers(address=470, values=[maskoutput, 0], id=1)
#     response = Response(device_address=2).read_data(rd_registers=0x1000, count=2)
#     print(response)

    #response = Response(device_address=2).read_data(rd_registers=51, count=2)
    #print(response)

    #time.sleep(3)
    #module_210.wr_holding_registers(address=470, values=[65535, 255], id=1)

    #response = Response(device_address=2).read_data(rd_registers=0x33, count=2)
    #print(response)

#test_di_do()