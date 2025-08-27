import asyncio
import sys
import logging
import time
import random

sys.path.append('/home/root/scripts')
from baseclasses.mapper import Mapper
from baseclasses.response import SpeWriteRead
from configuration import CONFIGURE_ADDRESS, CONFIGURE_NAME, CONFIGURE_QUANTITY, MODULE_ID
from enums.fai12_enums import TypeFilter, TypeBreakage, InputMode

mb_mapper = Mapper(configure_address=CONFIGURE_ADDRESS, configure_name=CONFIGURE_NAME,
                   configure_quantity=CONFIGURE_QUANTITY).build_map(module_id=MODULE_ID)

async def data_updater(context):

    for uid in range(1, 5):
        slave = context[uid]
        if uid == 3:
            start_reg = 0
            for name, address_count in mb_mapper.items():
                value = SpeWriteRead(device_address=uid).read_data(rd_registers=address_count[0],
                                                                         count=address_count[1])[0]

                if address_count[1] == 1:
                    slave.setValues(3, start_reg, [*value])
                else:
                    slave.setValues(3, start_reg, [value[1], value[0]])

                start_reg += address_count[1]

        else:
            new_value = uid * 2
            slave.setValues(3, 0, [new_value])

    start_reg = 0
    while True:
        for uid in range(1, 5):
            slave = context[uid]

            if uid == 3:

                slave.setValues(3, 1, [random.randint(1, 10)])



            else:

                current_value = slave.getValues(3, 0, count=1)[0]

                print(current_value)

        await asyncio.sleep(0.5)