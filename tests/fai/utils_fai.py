from baseclasses.response import SpeWriteRead
from baseclasses.modbus_operations import ModbusFeatures
from enums.fai12_enums import InputMode
from tests.fai.configuration import TIMEOUT_TF_CHANNEL, TIMEOUT_CTRL_CHANNEL


def set_mode_fai12(address, mapper_fai12, channels, mode):
    writer = SpeWriteRead(device_address=address)
    for channel in channels:
        modbus_input_field = getattr(mapper_fai12, f"input{channel}")
        writer.write_data(wr_registers=modbus_input_field.mode.addr,
                          data=[mode])



def set_tf_ctrl(address, mapper_fai12, groups, tf, ctrl):

    writer = SpeWriteRead(device_address=address)
    for group in groups:
        modbus_group_field = getattr(mapper_fai12, f"group{group}")
        writer.write_data(wr_registers=modbus_group_field.typeFilter.addr,
                          data=[tf])

        writer.write_data(wr_registers=modbus_group_field.typeBreakage.addr,
                          data=[ctrl])


def get_group_number(channel: int) -> int:
    if 1 <= channel <= 4:
        return 1
    elif 5 <= channel <= 8:
        return 2
    elif 9 <= channel <= 12:
        return 3
    else:
        raise ValueError(f"Некорректный канал: {channel}")



def calculate_expected_timestamps(address, mapper_fai12, tf, ctrl):
    counter_turn_on_channels = {
        1: {"voltage": 0, "current": 0},
        2: {"voltage": 0, "current": 0},
        3: {"voltage": 0, "current": 0},
    }

    reader = SpeWriteRead(device_address=address)
    for channel in range(1, 13):

        group_id = get_group_number(channel)

        modbus_input_field = getattr(mapper_fai12, f"input{channel}")
        modbus_input_field.mode.value = reader.read_data(rd_registers=modbus_input_field.mode.addr,
                                                        count=modbus_input_field.mode.count)[0]
        if modbus_input_field.mode.value[0] in (InputMode.VOLTAGE01, InputMode.VOLTAGE010):
            counter_turn_on_channels[group_id]["voltage"] += 1
        elif modbus_input_field.mode.value[0] in (InputMode.CURRENT020, InputMode.CURRENT420, InputMode.CURRENT05):
            counter_turn_on_channels[group_id]["current"] += 1



    channels_and_expected_timestamp = {}
    for channel in range(1, 13):
        # проверяем все режимы входов
        modbus_input_field = getattr(mapper_fai12, f"input{channel}")
        modbus_input_field.mode.value = SpeWriteRead(device_address=address).read_data(
                                                        rd_registers=modbus_input_field.mode.addr,
                                                            count=modbus_input_field.mode.count)[0]

        testing_channel_and_expected_timestamp = {}
        # если режим входа включен, то начинаем чтение timestamps
        if modbus_input_field.mode.value[0] != InputMode.DISABLE:
            group_id = get_group_number(channel)
            # выполняет расчет ожидаемого времени измерения канала по формуле
            expected_timestamp = 6 + (TIMEOUT_TF_CHANNEL[tf] + TIMEOUT_CTRL_CHANNEL[ctrl]) * \
                                 counter_turn_on_channels[group_id]["voltage"] + \
                                 TIMEOUT_TF_CHANNEL[tf] * counter_turn_on_channels[group_id]["current"]

            channels_and_expected_timestamp.setdefault(channel, expected_timestamp)
    return channels_and_expected_timestamp




def read_timestamp(address, mapper_fai12, channel):

    modbus_input_field = getattr(mapper_fai12, f"input{channel}")
    modbus_input_field.timestamp.value = SpeWriteRead(device_address=address).read_data(
        rd_registers=modbus_input_field.timestamp.addr,
        count=modbus_input_field.timestamp.count)[0]

    return modbus_input_field.timestamp.value[0]