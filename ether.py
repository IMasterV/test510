from baseclasses.mapper import Mapper
from baseclasses.response import SpeWriteRead
from configuration1 import CONFIGURE_ADDRESS, CONFIGURE_NAME, CONFIGURE_QUANTITY

import time

mb_mapper = Mapper(configure_address=CONFIGURE_ADDRESS, configure_name=CONFIGURE_NAME, configure_quantity=CONFIGURE_QUANTITY).build_map(module_id=3)

for _ in range(10):
    response = SpeWriteRead(device_address=3).read_data(rd_registers=mb_mapper['filter_type1'][0], count=mb_mapper['filter_type1'][1])[0][0]
    print(response)
    time.sleep(1)