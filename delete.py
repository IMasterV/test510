import time

import pytest

correct_timestamps = {0: (10, 11, 12), 1: (14, 15, 16), 2: (22, 23, 24),
                      3: (38, 39, 40), 4: (127, 128, 129)}
type_filter = (3, 0, 0, 3, 2, 3, 4, 1, 1, 2, 4, 0, 2, 0, 4, 4, 4, 1, 0, 2, 3, 2, 1, 3, 1)
control = (2, 0, 2, 0, 1, 1, 0, 1, 2, 2, 1, 1, 0, 0, 2, 2, 2, 0, 0, 0, 1, 1, 1, 1, 0)
mode = (2, 5, 4, 1, 1, 3, 3, 2, 5, 3, 4, 1, 2, 2, 5, 2, 1, 3, 3, 4, 4, 5, 4, 5, 1)
num_channels = ('1', '5', '15', '9', '19', '59', '159')
#timestamp = ((9, 10, 11, 12), )
# для каждой комбинации опеределить timestampы

params = [
    (channel, tf, ctl, md)
    for channel in num_channels
    for tf, ctl, md in zip(type_filter, control, mode)
]

@pytest.mark.parametrize('channel, type_f, ctrl, md', params)
def test_filter_one_channel_break_zero(channel, type_f, ctrl, md):
    time.sleep(1)
    print(f'channel = {channel}, type_f = {type_f}, ctrl={ctrl}, md= {md}')