import os

class base_encode:
    def generate(type):
        match type:
            case 0:
                from no_data_encode  import no_data_encode
                return no_data_encode()
            case 1:
                from xor_data_encode import xor_data_encode
                XOR_KEY=int(os.getenv("XOR_KEY")).to_bytes(1, byteorder='big')
                return xor_data_encode(XOR_KEY)
            case _:
                 raise NotImplementedError("encoder not supported")

    #data is byte
    def encode(self, data):
        raise NotImplementedError("Subclasses should implement this method")