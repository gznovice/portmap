from data_encode import base_encode

KEY_LENGTH = 1

class xor_data_encode(base_encode):
    #key should be one byte
    def __init__(self, key):
        self.key = key
        if(len(key) != KEY_LENGTH):
            raise ValueError("should be 1 length bytes")

    def encode(self, data):
        # XOR each byte of the data with the key
        result = bytearray()
    
        for i in range(len(data)):
            result.append(data[i] ^ self.key[0])

        return bytes(result)