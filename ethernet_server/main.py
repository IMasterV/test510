import asyncio
import logging
from pymodbus.server.async_io import ModbusTcpServer
from pymodbus.device import ModbusDeviceIdentification
from modbus_context import create_context
from pymodbus.datastore import ModbusServerContext
from updater import data_updater

logging.basicConfig(level=logging.INFO)

async def main():
    #context = create_context()
    context = ModbusServerContext(slaves=None, single=True)
    # Задача обновления регистров
    #asyncio.create_task(data_updater(context))

    # Информация о сервере
    identity = ModbusDeviceIdentification()
    identity.VendorName = "MyCompany"
    identity.ProductCode = "MC"
    identity.VendorUrl = "http://mycompany.local"
    identity.ProductName = "ModbusServer"
    identity.ModelName = "ModbusTCP"
    identity.MajorMinorRevision = "1.0"

    # Создаём и запускаем сервер
    server = ModbusTcpServer(
        context,
        identity=identity,
        address=("0.0.0.0", 5020),
    )

    await server.serve_forever()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped.")

