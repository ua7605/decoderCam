import asn1tools
import json


class DUSTCamDecoder(object):

    def __init__(self, file_path_to_output_json_file):
        self.cam = asn1tools.compile_files('./cam121.asn', 'uper')
        self.json_file = file_path_to_output_json_file

    def decode_cam_message(self, message):
        # TODO Make it possible to distinguish CAM, DENM and IVI messages
        encoded_cam = bytearray.fromhex(message)
        decoded_cam = self.cam.decode('CAM', encoded_cam)
        json_object_cam_message = json.dumps(decoded_cam)
        self._write_it_to_json_file(cam_message_json_format=json_object_cam_message)
        return json_object_cam_message

    def _write_it_to_json_file(self, cam_message_json_format):
        with open(self.json_file, 'w') as output_json_file:
            output_json_file.write(cam_message_json_format)
