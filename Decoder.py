import asn1tools
import json
import mpu.io

from csvReader import CsvReader


class CamDecoder():

    def __init__(self, file_path, output_file_path):
        # With this we load in the appropriate asn file for the decoder.
        self.cam = asn1tools.compile_files('./cam121.asn', 'uper')
        self.file_path = file_path
        self.output_file_path = output_file_path
        self.csv_reader = CsvReader(self.file_path)

    def encode(self):

        cam_message_hexadecimal_string = self.csv_reader.read_csv_file()
        encoded = bytearray.fromhex(cam_message_hexadecimal_string)
        decoded = self.cam.decode('CAM', encoded)
        self.to_json_format(decoded)

        return decoded

    def to_json_format(self, decoded_message):
        JSON_format = json.dumps(decoded_message)
        print("Below the decoded JSON format")
        print(JSON_format)
        self.write_to_json_file(JSON_format)

    def write_to_json_file(self, cam_message):
        # mpu.io.write('/Users/vincentcharpentier/School/Master/MAP/Decoder/outputfileCAM.json', cam_message)
        with open(self.output_file_path, 'w') as outfile:
            outfile.write(cam_message)