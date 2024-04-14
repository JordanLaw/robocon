import serial

class data_connect:
    def __init__(self):
        self.data_read = [0, 0, 0, 0, 0, 0, 0]

    def data_can_read(self, ser):

        message1 = 0
        message2 = 0
        message3 = 0
        message4 = 0

        while True:
            value_read = ser.read(1)
            if value_read == b'A':
                value_read = ser.read(1)
                # print(value_read)
                if value_read == b'T':
                    value_read = ser.read(4)
                    # print(value_read)
                    if value_read[0] + value_read[1] + value_read[2] + value_read[3] == 32:
                        value_read = ser.read(11)
                        # print(value_read)
                        bytes_fr = value_read[2:5]
                        bytes_fl = value_read[6:9]
                        self.data_read[0] = int.from_bytes(bytes_fr, byteorder='big', signed=True)
                        self.data_read[1] = int.from_bytes(bytes_fl, byteorder='big', signed=True)
                        message1 = 1

                    elif value_read[0] + value_read[1] + value_read[2] + value_read[3] == 64:
                        value_read = ser.read(5)
                        self.data_read[4] = value_read[1]
                        self.data_read[5] = value_read[2]
                        # data_read[6] = value_read[3]
                        # data_read[7] = value_read[4]
                        message2 = 1

                    elif value_read[0] + value_read[1] + value_read[2] + value_read[3] == 96:
                        value_read = ser.read(11)
                        bytes_br = value_read[2:5]
                        bytes_bl = value_read[6:9]
                        self.data_read[2] = int.from_bytes(bytes_br, byteorder='big', signed=True)
                        self.data_read[3] = int.from_bytes(bytes_bl, byteorder='big', signed=True)
                        message3 = 1

                    elif value_read[0] + value_read[1] + value_read[2] + value_read[3] == 128:
                        value_read = ser.read(5)
                        # print(value_read)
                        # data_read[4] = value_read[1]
                        # data_read[5] = value_read[2]
                        self.data_read[6] = value_read[1]
                        self.data_read[7] = value_read[2]
                        message4 = 1

            if message1 == 1 and message2 == 1 and message3 == 1 and message4 == 1:
                break