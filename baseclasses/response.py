from baseclasses.modbus_operations import ModbusFeatures, ModbusRequest
from baseclasses.spe_operations import SpeOperations


class SpeWriteRead:
    def __init__(self, device_address):
        self.device_address = device_address
        self.rr = SpeOperations()

    def write_data(self, wr_registers, data):
        myrequest = ModbusRequest(self.device_address, wr_registers).generate_modbus_write_request(data)
        response = tuple(self.rr.auto_request_response(requests=[myrequest], num=1))

        # myrequest2 = ModbusFeatures.create_modbus_rtu_request(device_address=self.device_address,
        #                                                       function_code=0x10,
        #                                                       register_address=wr_registers,
        #                                                       data_count=data)
        #
        # response = tuple(self.rr.auto_request_response(requests=[bytes(myrequest2)], num=1))
        #print(response)
        return response

    def read_data(self, rd_registers, count, num=1):
        myrequest = ModbusRequest(self.device_address, rd_registers).generate_modbus_read_request(count)
        response = tuple(self.rr.auto_request_response(requests=[myrequest], num=num))


        # myrequest1 = ModbusFeatures.create_modbus_rtu_request(device_address=self.device_address,
        #                                                       function_code=0x03,
        #                                                       register_address=rd_registers,
        #                                                       data_count=count)
        #
        # # num = 1 -> [0]
        # response = tuple(self.rr.auto_request_response(requests=[bytes(myrequest1)], num=1))[0]
        return response