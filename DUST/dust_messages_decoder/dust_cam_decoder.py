import asn1tools
import json


# TODO: Add a logger, switch every print statement to a log statement
from tools.startup_phase import LightBar


class DUSTCamDecoder(object):

    def __init__(self, file_path_to_output_json_file):
        self.cam = asn1tools.compile_files('./cam121.asn', 'uper')
        self.json_file = file_path_to_output_json_file
        print("Decoder is ready")

    def decode_cam_message(self, message, custom=False):
        # TODO Make it possible to distinguish CAM, DENM and IVI messages
        encoded_cam = bytearray(message)
        decoded_cam = self.cam.decode('CAM', encoded_cam)
        print(decoded_cam)
        if custom:
            #decoded_cam['cam']['camParameters']['specialVehicleContainer'][1]['lightBarSirenInUse'] = 1
            ms = self.decode_parameters_for_special_vehicle_service(decoded_cam)
            json_object_cam_message = json.dumps(decoded_cam)
            self._write_it_to_json_file(cam_message_json_format=json_object_cam_message)
            print("Successfully written to file")

            return ms

        json_object_cam_message = json.dumps(decoded_cam)
        self._write_it_to_json_file(cam_message_json_format=json_object_cam_message)
        return json_object_cam_message

    def _write_it_to_json_file(self, cam_message_json_format):
        with open(self.json_file, 'w') as output_json_file:
            output_json_file.write(cam_message_json_format)
            print("It is written to the file!!!! ")

    def decode_parameters_for_special_vehicle_service(self, decoded_cam):
        speed_value: int = decoded_cam['cam']['camParameters']['highFrequencyContainer'][1]['speed']['speedValue']

        speed_confidence = decoded_cam['cam']['camParameters']['highFrequencyContainer'][1]['speed']['speedConfidence']

        cause_code = decoded_cam['cam']['camParameters']['specialVehicleContainer'][1]['incidentIndication']['causeCode']

        sub_cause_code = decoded_cam['cam']['camParameters']['specialVehicleContainer'][1]['incidentIndication']['subCauseCode']

        traffic_rule = decoded_cam['cam']['camParameters']['specialVehicleContainer'][1]['trafficRule']

        speed_limit = decoded_cam['cam']['camParameters']['specialVehicleContainer'][1]['speedLimit']

        siren_activated, light_bar_activated = self._decode_status_light_bar_siren_in_use(light_bar_siren_in_use=decoded_cam['cam']['camParameters']['specialVehicleContainer'][1]['lightBarSirenInUse'], decode_cam=decoded_cam)

        message: str = str(speed_value)+","+str(speed_confidence)+","+str(cause_code)+","+str(sub_cause_code)+","+traffic_rule+","+str(speed_limit)+","+str(siren_activated)+","+str(light_bar_activated)
        print(message)
        return message

    def _decode_status_light_bar_siren_in_use(self, light_bar_siren_in_use, decode_cam):

        if light_bar_siren_in_use.__eq__(LightBar.SIREN_ACTIVATED_DEC.value):
            siren_activated: int = 1
            light_bar_activated: int = 0
        elif light_bar_siren_in_use.__eq__(LightBar.LIGHT_BAR_ACTIVATED.value):
            siren_activated: int = 0
            light_bar_activated: int = 1
        elif light_bar_siren_in_use.__eq__(LightBar.BOTH.value):
            siren_activated: int = 1
            light_bar_activated: int = 1
        elif light_bar_siren_in_use.__eq__(LightBar.NONE.value):
            siren_activated: int = 0
            light_bar_activated: int = 0
        else:
            siren_activated: int = 0
            light_bar_activated: int = 0
        decode_cam['cam']['camParameters']['specialVehicleContainer'][1]['lightBarSirenInUse'] = \
            {
            'lightBarActivated': light_bar_activated,
            'sirenActivated': siren_activated
            }
        return siren_activated, light_bar_activated


