import asyncio
import sys
import logging
import time

sys.path.append('/home/root/scripts')
from baseclasses.mapper import Mapper
from baseclasses.response import SpeWriteRead
from configuration import CONFIGURE_ADDRESS, CONFIGURE_NAME, CONFIGURE_QUANTITY, MODULE_ID
from enums.fai12_enums import TypeFilter, TypeBreakage, InputMode

mb_mapper = Mapper(configure_address=CONFIGURE_ADDRESS, configure_name=CONFIGURE_NAME,
                   configure_quantity=CONFIGURE_QUANTITY).build_map(module_id=MODULE_ID)

async def data_updater(context):


    last_value1 = None
    last_value2 = None
    last_value3 = None
    start_address = 0
    for name, value in mb_mapper.items():
        response = SpeWriteRead(device_address=MODULE_ID).read_data(rd_registers=value[0],
                                                                    count=value[1])[0]
        # [0x00] Slave_ID; 3 holding register, 0 register, [data]
        if value[1] == 1:
            context[0x01].setValues(3, start_address, [*response])

        if value[1] == 2:
            context[0x01].setValues(3, start_address, [response[1], response[0]])
        start_address += value[1]

    while True:
        response = SpeWriteRead(device_address=MODULE_ID).read_data(rd_registers=mb_mapper['filter_type1'][0],
                                                                    count=mb_mapper['filter_type1'][1])[0]
        # #print(response)
        #context[0x00].setValues(3, 3, [response[1], response[0]])
        context[0x01].setValues(3, 0, [response[0]])

        #print(f"[Updater] HR[0] = {response}")

        read_val1 = context[0x01].getValues(3, 0, count=1)[0]
        if read_val1 != last_value1:
            last_value1 = read_val1
            context[0x01].setValues(3, 0, [read_val1])  # HR[0]
            SpeWriteRead(device_address=MODULE_ID).write_data(wr_registers=mb_mapper[f'filter_type1'][0],
                                                              data=[read_val1])
            logging.info(f"[Handler] Кто-то записал HR[0] = {read_val1}")

            response = SpeWriteRead(device_address=MODULE_ID).read_data(rd_registers=mb_mapper['filter_type1'][0],
                                                                        count=mb_mapper['filter_type1'][1])[0]
            logging.info(f"[Handle] Обработка значения: {response[0]}")
        #
        #
        # read_val2 = context[0x00].getValues(3, 1, count=1)[0]
        # if read_val2 != last_value2:
        #     last_value2 = read_val2
        #     context[0x00].setValues(3, 0, [read_val2])  # HR[0]
        #     SpeWriteRead(device_address=MODULE_ID).write_data(wr_registers=mb_mapper[f'type_breakage1'][0],
        #                                                       data=[read_val2])
        #     logging.info(f"[Handler] Кто-то записал HR[1] = {read_val2}")
        #
        #     response = SpeWriteRead(device_address=MODULE_ID).read_data(rd_registers=mb_mapper['type_breakage1'][0],
        #                                                                 count=mb_mapper['type_breakage1'][1])[0]
        #     logging.info(f"[Handle] Обработка значения: {response[0]}")
        #
        # read_val3 = context[0x00].getValues(3, 2, count=1)[0]
        # if read_val3 != last_value3:
        #     last_value3 = read_val3
        #     context[0x00].setValues(3, 0, [read_val3])  # HR[0]
        #     SpeWriteRead(device_address=MODULE_ID).write_data(wr_registers=mb_mapper[f'input_mode1'][0],
        #                                                       data=[read_val3])
        #     logging.info(f"[Handler] Кто-то записал HR[2] = {read_val3}")
        #
        #     response = SpeWriteRead(device_address=MODULE_ID).read_data(rd_registers=mb_mapper['input_mode1'][0],
        #                                                                 count=mb_mapper['input_mode1'][1])[0]
        #     logging.info(f"[Handle] Обработка значения: {response[0]}")



            #await handle_read(read_val)

        # read_val = context[0x00].getValues(3, 3, count=1)[0]
        # if read_val != last_value:
        #     last_value = read_val
        #     context[0x00].setValues(3, 0, [read_val])  # HR[0]
        #     SpeWriteRead(device_address=MODULE_ID).write_data(wr_registers=mb_mapper[f'value1'][0],
        #                                                       data=[read_val])
        #     logging.info(f"[Handler] Кто-то записал HR[0] = {read_val}")
        #
        #     response = SpeWriteRead(device_address=MODULE_ID).read_data(rd_registers=mb_mapper['value1'][0],
        #                                                                 count=mb_mapper['value1'][1])[0]
        #     logging.info(f"[Handle] Обработка значения: {response[0]}")

        await asyncio.sleep(0.5)


async def handle_read(value):

    response = SpeWriteRead(device_address=MODULE_ID).read_data(rd_registers=mb_mapper['filter_type1'][0],
                                                                count=mb_mapper['filter_type1'][1])[0]
    print(f'че это = {response}')
    logging.info(f"[Handle] Обработка значения: {response[0]}")


# SpeWriteRead(device_address=MODULE_ID).write_data(wr_registers=mb_mapper[f'filter_type1'][0],
#                                                   data=[TypeFilter.ONE])
# SpeWriteRead(device_address=MODULE_ID).write_data(wr_registers=mb_mapper[f'type_breakage1'][0],
#                                                   data=[TypeBreakage.DISABLE])
# SpeWriteRead(device_address=MODULE_ID).write_data(wr_registers=mb_mapper[f'input_mode1'][0],
#                                                   data=[InputMode.CURRENT020])