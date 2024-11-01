from src.enums.global_enums import MachineErrorMessages


class Response:

    def __init__(self, module, id):
        self.module = module
        self.id = id

    def write_data(self, data, wr_registers):
        if data is not None:
            if isinstance(data, tuple):
                self.module.wr_holding_registers(address=wr_registers, values=[data[0], data[1]], id=self.id)
            else:
                self.module.wr_holding_registers(address=wr_registers, values=[data], id=self.id)
            return self
        else:
            return self

    def assert_state_status_code(self, state, status, rd_registers, count):
        if state is not None:
            response = self.module.rd_holding_registers(address=rd_registers, count=count, id=self.id)
            assert response[0] == state, MachineErrorMessages.WRONG_STATE_CODE.value
            assert response[2] == status, MachineErrorMessages.WRONG_STATUS_CODE.value