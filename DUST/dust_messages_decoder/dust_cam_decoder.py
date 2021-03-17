import asn1tools
import json


class DUSTCamDecoder(object):

    def __init__(self):
        self.cam = asn1tools.compile_files('./cam121.asn', 'uper')

    def decode_cam_message(self, message):
        encoded_cam = bytearray.fromhex(message)
        decoded_cam = self.cam.decode('CAM', encoded_cam)
        json_object_cam_message = json.dumps(decoded_cam)
        return json_object_cam_message


