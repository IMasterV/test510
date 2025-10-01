from baseclasses.response import SpeWriteRead
from enums.do32_enums import OutMode
from baseclasses.modbus_operations import ModbusFeatures

import time

def split_32bit_to_4x8(mask):
    """
    Делит 32-битную маску [low, high] на 4 части по 8 бит.
    Возвращает список из 4 масок [[x,0], [x,0], [x,0], [x,0]]
    для модулей DI1..DI4.
    """
    low, high = mask
    full = (high << 16) | low  # собираем одно число из 32 бит
    parts = []
    for i in range(4):
        part = (full >> (i * 8)) & 0xFF  # берём по 8 бит
        parts.append([part, 0])  # храним в формате [val, 0]
    return parts

def check_do_mask(address, db_32do, db_202, connected_modules, value):
    # Записываем значение в out_mask
    db_32do.do.out_mask.value = value
    SpeWriteRead(device_address=address).write_data(
        wr_registers=db_32do.do.out_mask.addr,
        data=value
    )
    time.sleep(0.01)

    # Преобразуем 32-битное значение в 4x8
    parts = split_32bit_to_4x8(value)

    # Читаем состояние всех модулей
    result = [
        module.rd_holding_registers(
            address=db_202.di.input_states.addr,
            count=db_202.di.input_states.count
        )
        for module in connected_modules
    ]

    # Проверяем совпадение
    assert parts == result


def set_logical_mode_do_spe(dev_addr, db_32do, num_channels=32):
    """Устанавливает Logical mode для 32DO."""
    for channel in range(1, num_channels + 1):
        modbus_output_field = getattr(db_32do, f"do{channel}")
        modbus_output_field.out_mode.value = OutMode.LOGICAL
        SpeWriteRead(device_address=dev_addr).write_data(
            wr_registers=modbus_output_field.out_mode.addr,
            data=[modbus_output_field.out_mode.value]
        )


def set_logical_mode_di_tcp(db_202, connected_modules, num_channels=8):
    """Устанавливает Logical mode для 202DI."""
    for channel in range(1, num_channels + 1):
        modbus_input_field = getattr(db_202, f"di{channel}")
        modbus_input_field.input_mode.value = 0
        for module in connected_modules:
            module.wr_holding_registers(
                address=modbus_input_field.input_mode.addr,
                values=[modbus_input_field.input_mode.value]
            )



def set_imp_gen_mode_do(db_32do, dev_addr, num_channels=3):
    """Устанавливает Imp_Gen mode для 32DO."""
    for channel in range(1, num_channels + 1):
        modbus_output_field = getattr(db_32do, f"do{channel}")
        modbus_output_field.out_mode.value = OutMode.IMP_GEN
        SpeWriteRead(device_address=dev_addr).write_data(
            wr_registers=modbus_output_field.out_mode.addr,
            data=[modbus_output_field.out_mode.value]
        )


def set_pulse_counting_mode_202(db_202, connected_modules, num_channels=8):
    """Устанавливает Pulse_counting mode для 202DI."""
    for channel in range(1, num_channels + 1):
        modbus_input_field = getattr(db_202, f"di{channel}")
        modbus_input_field.input_mode.value = 2
        for module in connected_modules:
            module.wr_holding_registers(
                address=modbus_input_field.input_mode.addr,
                values=[modbus_input_field.input_mode.value]
            )

def set_period_measure_mode_di(db_202, connected_modules, num_channels=8):
    """Устанавливает Pulse_counting mode для 202DI."""
    for channel in range(1, num_channels + 1):
        modbus_input_field = getattr(db_202, f"di{channel}")
        modbus_input_field.input_mode.value = 1
        for module in connected_modules:
            module.wr_holding_registers(
                address=modbus_input_field.input_mode.addr,
                values=[modbus_input_field.input_mode.value]
            )

def set_frequency_measure_mode_di(db_202, connected_modules, num_channels=8):
    """Устанавливает Pulse_counting mode для 202DI."""
    for channel in range(1, num_channels + 1):
        modbus_input_field = getattr(db_202, f"di{channel}")
        modbus_input_field.input_mode.value = 3
        for module in connected_modules:
            module.wr_holding_registers(
                address=modbus_input_field.input_mode.addr,
                values=[modbus_input_field.input_mode.value]
            )

def set_filter_off_di(db_202, connected_modules, num_channels=20):
    """Выключает Filter для 202DI."""
    for channel in range(1, num_channels + 1):
        modbus_input_field = getattr(db_202, f"di{channel}")
        modbus_input_field.filter_bounce.value = 0
        for module in connected_modules:
            module.wr_holding_registers(
                address=modbus_input_field.filter_bounce.addr,
                values=[modbus_input_field.filter_bounce.value]
            )


def reset_pulse_counting_di(db_202, connected_modules, num_channels=20):
    """Сброс счетчика импульсов для 202DI."""
    for channel in range(1, num_channels + 1):
        modbus_input_field = getattr(db_202, f"di{channel}")
        modbus_input_field.reset_counter.value = 0
        for module in connected_modules:
            module.wr_holding_registers(
                address=modbus_input_field.reset_counter.addr,
                values=[modbus_input_field.reset_counter.value]
            )


def set_data_and_check_imp_gen_mode(dev_addr, module202, db_202, db_32do, data_imp_gen_freq, data_imp_gen_num, num_channels=3):
    """
    :param db_202:
    :param db_32do:
    :param data_imp_gen_freq:
    :param data_imp_gen_num:
    :param num_channels:
    :return: None
    """
    # reset pulse_counting for 20 inputs
    reset_pulse_counting_di(db_202, [module202, ], num_channels=20)
    time.sleep(0.005)
    device = SpeWriteRead(device_address=dev_addr)

    # добавить сброс в 0
    # reset impgen_num and impgen_freq>>????

    for channel in range(1, num_channels + 1):
        # Сбрасываем задатчик импульсов в 0
        modbus_output_field = getattr(db_32do, f"do{channel}")
        modbus_output_field.impgen_num.value = 0
        device.write_data(wr_registers=modbus_output_field.impgen_num.addr,
                                                          data=[modbus_output_field.impgen_num.value])

    for channel in range(1, num_channels + 1):
        # Задать минимальную частоту
        modbus_output_field = getattr(db_32do, f"do{channel}")
        modbus_output_field.impgen_freq.value = data_imp_gen_freq
        device.write_data(wr_registers=modbus_output_field.impgen_freq.addr,
                                                          data=[modbus_output_field.impgen_freq.value])
        # Задать количество генерируемых импульсов
        modbus_output_field.impgen_num.value = data_imp_gen_num
        device.write_data(wr_registers=modbus_output_field.impgen_num.addr,
                                                          data=[modbus_output_field.impgen_num.value])
    # Ожидаем когда импульсы сгенерируются
    time.sleep((1 / data_imp_gen_freq) * data_imp_gen_num + 0.050)

    for channel in range(1, num_channels + 1):

        # Считываем счетчик импульсов входов
        modbus_output_field = getattr(db_202, f"di{channel}")
        response = module202.rd_holding_registers(address=modbus_output_field.counter_value.addr,
                                                   count=modbus_output_field.counter_value.count)
        try:
            # считанное количество импульсов == [заданному, 0]
            assert response == [data_imp_gen_num, 0], response
        except AssertionError:
            # Сбрасываем задатчик импульсов в 0
            for channel in range(1, num_channels + 1):
                modbus_output_field = getattr(db_32do, f"do{channel}")
                modbus_output_field.impgen_num.value = 0
                device.write_data(wr_registers=modbus_output_field.impgen_num.addr,
                                                                  data=[modbus_output_field.impgen_num.value])

                raise AssertionError(f'response={response}, testing_data_imp_gen_num={[data_imp_gen_num, 0]}')

    # reset impgen_num and impgen_freq>>????

    # Сбрасываем задатчик импульсов в 0
    for channel in range(1, num_channels + 1):
        modbus_output_field = getattr(db_32do, f"do{channel}")
        modbus_output_field.impgen_num.value = 0
        device.write_data(wr_registers=modbus_output_field.impgen_num.addr,
                                                          data=[modbus_output_field.impgen_num.value])


# for do_pos_output_hs_pwm_duty
def set_pwm_fast_mode_do(db_32do, dev_addr, value, num_channels=8):

    for channel in range(1, num_channels+1):
        modbus_output_field = getattr(db_32do, f"do{channel}")
        modbus_output_field.out_mode.value = value
        SpeWriteRead(device_address=dev_addr).write_data(
            wr_registers=modbus_output_field.out_mode.addr,
            data=[modbus_output_field.out_mode.value]
        )



def set_pwm_duty_do(db_32do, address, pwm_duty, num_channels=32):
    """Устанавливает PWM_DUTY для 32DO."""
    for channel in range(1, num_channels + 1):
        modbus_output_field = getattr(db_32do, f"do{channel}")
        modbus_output_field.pwm_duty.value = pwm_duty

        SpeWriteRead(device_address=address).write_data(
            wr_registers=modbus_output_field.pwm_duty.addr,
            data=[modbus_output_field.pwm_duty.value]
        )

def set_type_sensor_102(db_102, device, value, num_channels=8):

    for channel in range(1, num_channels+1):
        modbus_output_field = getattr(db_102, f"ai{channel}")

        modbus_output_field.type_sensor.value = value
        device.wr_holding_registers(address=modbus_output_field.type_sensor.addr,
                                         values=[modbus_output_field.type_sensor.value, 0])


def set_ain_h_102(db_102, device, value, num_channels=8):
    for channel in range(1, num_channels + 1):
        modbus_output_field = getattr(db_102, f"ai{channel}")

        modbus_output_field.ain_h.value = ModbusFeatures.float_to_int16_list(value)
        device.wr_holding_registers(address=modbus_output_field.ain_h.addr,
                                         values=modbus_output_field.ain_h.value)

def read_values_float_102(db_102, device, num_channels=8):
    values_float = []
    for channel in range(1, num_channels+1):
        modbus_output_field = getattr(db_102, f"ai{channel}")

        modbus_output_field.value_float.value = device.rd_holding_registers(
                                        address=modbus_output_field.value_float.addr,
                                         count=modbus_output_field.value_float.count)
        response = ModbusFeatures.int16_list_to_float(modbus_output_field.value_float.value)
        values_float.append(response)
    return values_float




def set_pwm_slow_mode_do(db_32do, address, num_channels=32):
    """Устанавливает PWM_SLOW mode для 32DO."""
    for channel in range(1, num_channels + 1):
        modbus_output_field = getattr(db_32do, f"do{channel}")
        modbus_output_field.out_mode.value = OutMode.PWM_SLOW
        SpeWriteRead(device_address=address).write_data(
            wr_registers=modbus_output_field.out_mode.addr,
            data=[modbus_output_field.out_mode.value]
        )

def set_pwm_period_do(db_32do, address, pwm_period, num_channels=32):
    """Устанавливает PWM Period для 32DO."""
    for channel in range(1, num_channels + 1):
        modbus_output_field = getattr(db_32do, f"do{channel}")
        modbus_output_field.pwm_period.value = pwm_period

        SpeWriteRead(device_address=address).write_data(
            wr_registers=modbus_output_field.pwm_period.addr,
            data=[modbus_output_field.pwm_period.value]
        )
