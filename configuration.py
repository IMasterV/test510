FILENAME = "/dev/spe"  # Имя файла
FILESIZE = 256  # Размер буфера для чтения данных

MODULE_ID = 3

CONFIGURE_ADDRESS = [0x1000, 0x1001,
                     0x1002, 0x1004, 0x1005, 0x1006,
                     0x1008, 0x100A, 0x100B, 0x100C,
                     0x100E, 0x1010, 0x1011, 0x1012,
                     0x1014, 0x1016, 0x1017, 0x1018,
                     0x101A, 0x101B,
                     0x101C, 0x101E, 0x101F, 0x1020,
                     0x1022, 0x1024, 0x1025, 0x1026,
                     0x1028, 0x102A, 0x102B, 0x102C,
                     0x102E, 0x1030, 0x1031, 0x1032,
                     0x1034, 0x1035,
                     0x1036, 0x1038, 0x1039, 0x103A,
                     0x103C, 0x103E, 0x103F, 0x1040,
                     0x1042, 0x1044, 0x1045, 0x1046,
                     0x1048, 0x104A, 0x104B, 0x104C]

CONFIGURE_NAME = ['filter_type1', 'type_breakage1',
                  'value1', 'status1', 'timestamp1', 'input_mode1',
                  'value2', 'status2', 'timestamp2', 'input_mode2',
                  'value3', 'status3', 'timestamp3', 'input_mode3',
                  'value4', 'status4', 'timestamp4', 'input_mode4',
                  'filter_type2', 'type_breakage2',
                  'value5', 'status5', 'timestamp5', 'input_mode5',
                  'value6', 'status6', 'timestamp6', 'input_mode6',
                  'value7', 'status7', 'timestamp7', 'input_mode7',
                  'value8', 'status8', 'timestamp8', 'input_mode8',
                  'filter_type3', 'type_breakage3',
                  'value9', 'status9', 'timestamp9', 'input_mode9',
                  'value10', 'status10', 'timestamp10', 'input_mode10',
                  'value11', 'status11', 'timestamp11', 'input_mode11',
                  'value12', 'status12', 'timestamp12', 'input_mode12',]

CONFIGURE_QUANTITY = [1, 1,
            2, 1, 1, 1,
            2, 1, 1, 1,
            2, 1, 1, 1,
            2, 1, 1, 1,
            1, 1,
            2, 1, 1, 1,
            2, 1, 1, 1,
            2, 1, 1, 1,
            2, 1, 1, 1,
            1, 1,
            2, 1, 1, 1,
            2, 1, 1, 1,
            2, 1, 1, 1,
            2, 1, 1, 1]

BASE_MAP_REGION = 0xfe00
BASE_MAP_REGS = 0xff00

