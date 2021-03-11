import asn1tools
import json
import mpu.io

class CamDecoder():

    def __init__(self):

        # With this we load in the appropriate asn file for the decoder.
        self.cam = asn1tools.compile_files('./cam121.asn','uper')

    def encode(self):
        cam_message_hexadecimal_string= '01020000138EC14D00FA9269F00DC028393FFFFFFC23B7743E80'
        encoded = bytearray.fromhex(cam_message_hexadecimal_string)
        decoded = self.cam.decode('CAM',encoded)
        self.to_json_format(decoded)
        return decoded

    def to_json_format(self, decoded_message):
        JSON_format = json.dumps(decoded_message)
        print("Below the decoded JSON format")
        print(JSON_format)
        print("Normally it is stored in a JSON file")
        self.write_to_json_file(JSON_format)


    def write_to_json_file(self, cam_message):
        #mpu.io.write('/Users/vincentcharpentier/School/Master/MAP/Decoder/outputfileCAM.json', cam_message)
        file_paht = '/Users/vincentcharpentier/School/Master/MAP/Decoder/CAMv1.json'
        with open(file_paht, 'w') as outfile:
            outfile.write(cam_message)





