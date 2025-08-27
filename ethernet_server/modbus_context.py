from pymodbus.datastore import ModbusSequentialDataBlock, ModbusServerContext, ModbusSlaveContext

# Инициализация регистров (по 100 регистров на каждый тип)
def create_context():
    slaves = {
        uid: ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [0]*100),  # Discrete Inputs
        co=ModbusSequentialDataBlock(0, [0]*100),  # Coils
        hr=ModbusSequentialDataBlock(0, [0]*100),  # Holding Registers
        ir=ModbusSequentialDataBlock(0, [0]*100),  # Input Registers
        zero_mode=True
        )
        for uid in range(1, 5)
    }
    context = ModbusServerContext(slaves=slaves, single=False)
    return context





