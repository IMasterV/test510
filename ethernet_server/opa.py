import asyncio
import logging
from pymodbus.server.async_io import StartAsyncTcpServer, ModbusProtocol
from pymodbus.client import ModbusSerialClient
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusServerContext
from pymodbus.pdu import ModbusRequest

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()

# Синхронный RTU-клиент
rtu_client = ModbusSerialClient(
    method="rtu",
    port="/dev/ttyUSB0",
    baudrate=9600,
    timeout=1
)

class TcpRtuProxy(ModbusProtocol):
    async def handle(self):
        while True:
            request = await self._recv()  # raw Modbus TCP PDU
            if not request:
                return
            pdu = self.decoder.decode(request)
            if not isinstance(pdu, ModbusRequest):
                continue

            unit = pdu.unit_id
            log.info(f"TCP→RTU (unit={unit}, func={pdu.function_code}) from {self.peername}")

            # Отправляем синхронно в RTU
            if not rtu_client.connect():
                log.error("RTU connection failed")
                return

            response = rtu_client.execute(pdu)  # отправляем и принимаем
            rtu_client.close()

            if response:
                frame = self.encoder.encode(response)
                self.transport.write(frame)
                log.info(f"RTU→TCP sent response for unit={unit}")

async def run_gateway():
    context = ModbusServerContext(slaves=None, single=True)
    identity = ModbusDeviceIdentification()
    identity.VendorName = "TCP→RTU Gateway"
    identity.ProductName = "pymodbus 3.8.6"
    identity.MajorMinorRevision = "3.8.6"

    await StartAsyncTcpServer(
        protocol_factory=TcpRtuProxy,
        context=context,
        identity=identity,
        address=("0.0.0.0", 5020),
    )

if __name__ == "__main__":
    asyncio.run(run_gateway())