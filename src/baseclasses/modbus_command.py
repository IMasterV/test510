import time
#from pymodbus import framer, pymodbus_apply_logging_config
from pymodbus.client import (ModbusSerialClient, ModbusTcpClient)
from pymodbus.pdu import ExceptionResponse
#from pymodbus.transaction import (ModbusAsciiFramer, ModbusRtuFramer)
from pymodbus import (
    framer,
    #Framer,
    ExceptionResponse,
    ModbusException,
    pymodbus_apply_logging_config)

class ModbusFunction():
    """Functions Modbus"""

    def __init__(self, client):
        self.client = client

    def rd_holding_registers(self, address, count, id=1):
        print("get and verify data")
        try:
            value = self.client.read_holding_registers(address=address, count=count, slave=id)
        except ModbusException as exc:
            print(f"Received ModbusException({exc}) from library")
            self.client.close()
            return
        if value.isError():  # pragma no cover
            print(f"Received Modbus library error({value})")
            self.client.close()
            return (value.isError())
        else:
            print(value.registers)
            return value.registers

    def wr_holding_registers(self, address, values, id=1):
        print("set and verify data")
        try:
            value = self.client.write_registers(address=address, values=values, slave=id)

        except ModbusException as exc:
            print(f"Received ModbusException({exc}) from library")
            self.client.close()
            return
        if value.isError():  # pragma no cover
            print(f"Received Modbus library error({value})")
            self.client.close()
            return (value.isError())
        else:
            return value.registers


class ConnectModule():
    def __init__(self, comm, host='', port=0, com_settings=None, framer= framer):
        if isinstance(comm, str):
            if comm == 'tcp' or comm == 'com':
                self._comm = comm
            else:
                raise AttributeError('Значение comm должно быть com или tcp')
        else:
            raise AttributeError('Значение comm должно быть типа str')
        self.host = host
        self.port = port
        self.com_settings = com_settings
        self.framer = framer

    @property
    def comm(self):
        return self._comm

    @comm.setter
    def comm(self, comm):
        if isinstance(comm, str):
            if comm == 'tcp' or comm == 'com':
                self._comm = comm
            else:
                raise AttributeError('Значение comm должно быть com или tcp')
        else:
            raise AttributeError('Значение comm должно быть типа str')

    def request_module(self):

        """Run sync client."""
        # activate debugging
        # pymodbus_apply_logging_config("DEBUG")
        if self._comm == 'tcp':
            client = ModbusTcpClient(
                self.host,
                port=self.port,
                framer=self.framer,
                timeout=10,
                retries=4,
                # retry_on_empty=False,y
                # source_address=("localhost", 0),
            )
            print(f'connect to {self.host}')
            client.connect()
            return ModbusFunction(client)

        if self._comm == 'com':
            client = ModbusSerialClient(
                self.com_settings[0],
                # framer=framer,
                # timeout=10,
                # retries=3,
                # retry_on_empty=False,
                # close_comm_on_error=False,.
                # strict=True,
                baudrate=self.com_settings[1],
                bytesize=self.com_settings[2],
                parity=self.com_settings[3],
                stopbits=self.com_settings[4],
                # handle_local_echo=False,
            )
            print(f"connect to {self.com_settings[0]}")
            client.connect()
            return ModbusFunction(client)