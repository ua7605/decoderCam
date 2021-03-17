import asn1tools
import json


class DUSTCamDecoder(object):

    def __init__(self, output_file):
        self.cam = asn1tools.compile_files('./cam121.asn', 'uper')
        self.output_file = output_file

    def decode_cam_message(self, message):
        encoded_cam = bytearray.fromhex(message)
        decoded_cam = self.cam.decode('CAM', encoded_cam)
        json_object_cam_message = json.dumps(decoded_cam)
        return json_object_cam_message

    def _write_it_to_json_file(self, cam_message_json_format):
        with open(self.output_file, 'w') as output_file:
            output_file.write(cam_message_json_format)
