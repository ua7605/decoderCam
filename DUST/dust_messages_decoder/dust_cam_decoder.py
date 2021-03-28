import asn1tools
import json


# TODO: Add a logger, switch every print statement to a log statement
class DUSTCamDecoder(object):

    def __init__(self, file_path_to_output_json_file):
        self.cam = asn1tools.compile_files('./cam121.asn', 'uper')
        self.json_file = file_path_to_output_json_file
        print("Decoder is ready")

    def decode_cam_message(self, message, custom=False):
        # TODO Make it possible to distinguish CAM, DENM and IVI messages
        encoded_cam = bytearray(message)
        print("A: Do you come still here?")
        print(encoded_cam)
        print("B: Do you come still here?")
        decoded_cam = self.cam.decode('CAM', encoded_cam)
        print("C: Do you come still here?")
        print(decoded_cam)
        if custom:
            decoded_cam['cam']['camParameters']['specialVehicleContainer'][1]['lightBarSirenInUse'] = 1
            json_object_cam_message = json.dumps(decoded_cam)
            self._write_it_to_json_file(cam_message_json_format=json_object_cam_message)
            print("Successfully written to file")

            return self.get_parameters_for_special_vehicle_service(decoded_cam)

        json_object_cam_message = json.dumps(decoded_cam)
        print("D: Do you come still here?")
        self._write_it_to_json_file(cam_message_json_format=json_object_cam_message)
        print("E: Do you come still here?")
        return json_object_cam_message

    def _write_it_to_json_file(self, cam_message_json_format):
        with open(self.json_file, 'w') as output_json_file:
            output_json_file.write(cam_message_json_format)
            print("It is written to the file!!!! ")

    def get_parameters_for_special_vehicle_service(self, decoded_cam):
        print("In parsing!!!!!!!!!")
        speed_value: int = decoded_cam['cam']['camParameters']['highFrequencyContainer'][1]['speed']['speedValue']
        print(speed_value)

        speed_confidence = decoded_cam['cam']['camParameters']['highFrequencyContainer'][1]['speed']['speedConfidence']
        print(str(speed_confidence))

        cause_code = decoded_cam['cam']['camParameters']['specialVehicleContainer'][1]['incidentIndication']['causeCode']
        print(cause_code)

        sub_cause_code = decoded_cam['cam']['camParameters']['specialVehicleContainer'][1]['incidentIndication']['subCauseCode']
        print(sub_cause_code)

        traffic_rule = decoded_cam['cam']['camParameters']['specialVehicleContainer'][1]['passToLeft']
        print(str(traffic_rule))

        speed_limit = decoded_cam['cam']['camParameters']['specialVehicleContainer'][1]['speedLimit']
        print(str(speed_limit))

        message: str = str(speed_value)+","+str(speed_confidence)+","+str(cause_code)+","+str(sub_cause_code)+","+traffic_rule+","+str(speed_limit)
        print(message)
        return message
