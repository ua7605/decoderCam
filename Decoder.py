import asn1tools
import json
class CamDecoder():

    def __init__(self):

        # With this we load in the appropriate asn file for the decoder.
        self.cam = asn1tools.compile_files('./cam121.asn','uper')

    def encode(self):
        message_hexadecimal_string = '01020000138EC14D00FA9269F00DC028393FFFFFFC23B7743E80'
        encoded = bytearray.fromhex(message_hexadecimal_string)
        decoded = self.cam.decode('CAM',encoded)
        self.to_json_format(decoded)
        return decoded

    def to_json_format(self, decodedmessage):
        JSON_format = json.dumps(decodedmessage)
        print("Hieronder staat het JSON formaat")
        print(JSON_format)

   #def write



