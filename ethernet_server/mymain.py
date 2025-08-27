import asyncio
import logging
import sys
from pymodbus.server.async_io import ModbusTcpServer
#from modbus_context import create_context
from pymodbus.datastore import ModbusServerContext, ModbusSlaveContext
from pymodbus.datastore import ModbusSequentialDataBlock

sys.path.append('/home/root/scripts')
#from baseclasses.mapper import Mapper
from baseclasses.response import SpeWriteRead
#from configuration import CONFIGURE_ADDRESS, CONFIGURE_NAME, CONFIGURE_QUANTITY, MODULE_ID

# mb_mapper = Mapper(configure_address=CONFIGURE_ADDRESS, configure_name=CONFIGURE_NAME,
#                    configure_quantity=CONFIGURE_QUANTITY).build_map(module_id=MODULE_ID)

logging.basicConfig(level=logging.INFO)

class LoggingDataBlock(ModbusSequentialDataBlock):
    def __init__(self, unit_id, address, values):
        super().__init__(address, values)
        self.unit_id = unit_id

    def getValues(self, address, count=1):
        values = SpeWriteRead(device_address=self.unit_id).read_data(rd_registers=address,
                                                           count=count)[0]
        super().setValues(address, values)

        values = super().getValues(address, count)
        #print(f"[UnitID {self.unit_id}] READ from address {address} count {count}: values = {values}")
        return values

    def setValues(self, address, values):

        SpeWriteRead(device_address=self.unit_id).write_data(wr_registers=address,
                                                             data=values)

        #print(f"[UnitID {self.unit_id}] WRITE to address {address}: values = {values}")
        super().setValues(address, values)

def create_context():
    slaves = {}
    for unit_id in range(1, 5):
        block_di = LoggingDataBlock(unit_id, 0, [0]*100)
        block_co = LoggingDataBlock(unit_id, 0, [0]*100)
        block_hr = LoggingDataBlock(unit_id, 0, [0]*65535)
        block_ir = LoggingDataBlock(unit_id, 0, [0]*100)

        slave = ModbusSlaveContext(
            di=block_di,
            co=block_co,
            hr=block_hr,
            ir=block_ir,
            zero_mode=True
        )
        slaves[unit_id] = slave

    context = ModbusServerContext(slaves=slaves, single=False)
    return context

async def main():
    context = create_context()
    server = ModbusTcpServer(context, address=("0.0.0.0", 5020))
    await server.serve_forever()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped.")

