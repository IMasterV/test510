import csv
import struct
import select
from configuration1 import FILENAME, FILESIZE


from pymodbus import (
    framer,
    #Framer,
    ExceptionResponse,
    ModbusException,
    pymodbus_apply_logging_config)

from pymodbus.client import (ModbusSerialClient, ModbusTcpClient)
from pymodbus.framer import ModbusSocketFramer



class ModbusOperationSpe:
    # def __init__(self, requests, num):
    #     self.requests = requests
    #     self.num = num

    # Main function that performs data writing and reading.
    def main(self, requests, num):
        try:
            # Open the file in read/write mode without buffering.
            with open(FILENAME, "r+b", buffering=0) as f:
                for i in range(num + 1):  # Loop with NUM + 1 iterations.
                    # Wait for the file to be ready for writing.
                    select.select([], [f.fileno()], [])

                    # If not the last iteration, write requests.
                    if i != num:
                        for request in requests:
                            f.write(request)  # Write the request to the file.
                        print(f"Added {len(requests)} new requests")  # Log the write operation.

                    # If not the first iteration, read response data.
                    if i != 0:
                        for j in range(len(requests)):
                            response_bytes = f.read(FILESIZE)  # Read data from the file.
                            # Print data in hexadecimal format or a message if no data is available.
                            if not response_bytes:
                                print('no data')
                            else:
                                print(self.parse_modbus_rtu_response([byte for byte in response_bytes]))

        except OSError as e:  # Handle file operation errors.
            print(f"Error: {e.strerror} ({e.errno})")

    @staticmethod
    def create_modbus_rtu_request(device_address, function_code, register_address, data_count):
        # device_address, function_code, register_address, data_count = 1, 3, 0, 16
        # request = create_modbus_rtu_request(device_address, function_code, register_address, data_count)
        def compute_crc(data):
            """
            Computes CRC-16 for a Modbus RTU packet.
            """
            crc = 0xFFFF
            for byte in data:
                crc ^= byte
                for _ in range(8):
                    if crc & 0x0001:
                        crc = (crc >> 1) ^ 0xA001
                    else:
                        crc >>= 1
            return crc.to_bytes(2, byteorder='little')  # CRC (little-endian)
        """
        Creates a Modbus RTU request in byte format.
        :param device_address: Modbus device address
        :param function_code: Modbus function code
        :param register_address: Starting register address
        :param data_count: Number of registers to be transmitted
        :return: Modbus RTU request as a list of bytes (list[int])
        """
        # Validate input ranges
        if not (1 <= device_address <= 32):
            raise ValueError("Device address must be between 1 and 32")
        if not (1 <= function_code <= 21):
            raise ValueError("Function code must be between 1 and 21")
        if not (0 <= register_address <= 65535):
            raise ValueError("Register address must be between 0 and 65535")
        if not (1 <= data_count <= 65535):
            raise ValueError("Data count must be between 1 and 65535")

        # Create packet without CRC
        frame = struct.pack('>B B H H', device_address, function_code, register_address, data_count)

        # Compute CRC-16 and append it to the packet
        frame += compute_crc(frame)

        # Return byte list
        print(f"Request: {list(frame)}")
        return list(frame)

    @classmethod
    def parse_modbus_rtu_response(cls, response):
        #parsed_registers = parse_modbus_rtu_response(modbus_response_bytes)
        """
        Parses a Modbus RTU response and returns an array of register values.

        :param response: Byte array of the Modbus RTU response (list[int] or bytes)
        :return: List of register values (list[int] or list[str], depending on the data)
        """
        # Check minimum response length (address + function + data bytes + CRC)
        if len(response) < 5:
            raise ValueError("Invalid response: packet too short")

        # Extract fields from the response
        device_address = response[0]  # Device address
        function_code = response[1]  # Function code
        byte_count = response[2]  # Number of data bytes
        data = response[3:-2]  # Data without CRC
        crc_received = response[-2:]  # Received CRC

        # Validate that data length matches byte_count
        if len(data) != byte_count:
            raise ValueError("Error: Data byte count does not match header")

        # Parse data into 2-byte Modbus registers
        registers = [struct.unpack(">H", bytes(data[i:i + 2]))[0] for i in range(0, len(data), 2)]

        return registers

    @staticmethod
    def registers_to_ascii(registers):
        # [30797, 12597, 11568, 12851, 20292]
        """
        Converts an array of 16-bit registers to an ASCII string.

        :param registers: List of 16-bit numbers (Modbus registers).
        :return: ASCII string.
        """
        byte_array = bytearray()

        for reg in registers:
            byte_array.extend(reg.to_bytes(2, byteorder='little'))  # Convert register to 2 bytes

        return byte_array.decode("ascii", errors="ignore")  # Decode to string

    @staticmethod
    def read_file_requests():
        bytes_requests = []
        with open('requests.csv', encoding='utf-8') as file:
            rows = csv.reader(file)  # Create reader object
            for row in rows:
                bytes_requests.append(bytes([int(byte, 16) for byte in row]))

        return bytes_requests