import asn1tools
import json
import os
import time

from tools.startup_phase import LightBar


class CamGenerator(object):
    dir_name = os.path.dirname(__file__)

    def __init__(self, dir_name=dir_name):
        self.cam_asn1 = asn1tools.compile_files('/Users/vincentcharpentier/PycharmProjects/DecdoderCAM/cam121.asn',
                                                'uper')
        template_cam_json = '/Users/vincentcharpentier/PycharmProjects/DecdoderCAM/DUST/CAM_Message_generator/cam_custom_template.json'  # "#os.path.join(dir_name, "cam_template.json")  # "cam_template.json")
        self.f = open(
            '/Users/vincentcharpentier/PycharmProjects/DecdoderCAM/DUST/CAM_Message_generator/cam_custom_template.json',
            "r")
        self.template_cam = json.load(self.f)

    def start_v2_custom_massaging(self, dir_name=dir_name):
        i = 1

        self._light_bar_siren_in_use(
            message=self.template_cam['cam']['camParameters']['specialVehicleContainer'][1]['lightBarSirenInUse'])
        is_run = True
        while is_run:
            custom = self.template_cam
            stationID = custom['header']['stationID']
            stationType = custom['cam']['camParameters']['basicContainer']['stationType']
            print("Het stationID = ", stationID, " Het stationType = ", stationType)
            custom['cam']['camParameters']['basicContainer']['referencePosition']['altitude']['altitudeValue'] = i
            custom['cam']['camParameters']['highFrequencyContainer'] = (
            'basicVehicleContainerHighFrequency', custom['cam']['camParameters']['highFrequencyContainer'][1])

            custom['cam']['camParameters']['specialVehicleContainer'] = (
            'safetyCarContainer', custom['cam']['camParameters']['specialVehicleContainer'][1])
            payload = self.cam_asn1.encode("CAM", custom)
            time.sleep(1)
            i += 1
            print("sent to CAMINO")
            print(custom)
            print("----------Decoder----------")
            decoded_cam = self.cam_asn1.decode('CAM', payload)
            sire, light_bar = self.decode_status_light_bar_siren_in_use(
                light_bar_siren_in_use=decoded_cam['cam']['camParameters']['specialVehicleContainer'][1][
                    'lightBarSirenInUse'], decode_cam=decoded_cam)
            print("Siren: ", sire, " lightbar ", light_bar)
            json_object_cam_message = json.dumps(decoded_cam)

            is_run = True
            # print(decoded_cam)

    def _light_bar_siren_in_use(self, message):
        print("message: ", message)

        light_bar_active = message['lightBarActivated']
        siren_activated = message['sirenActivated']

        if light_bar_active == 1 and siren_activated == 0:
            self.template_cam['cam']['camParameters']['specialVehicleContainer'][1][
                'lightBarSirenInUse'] = LightBar.LIGHT_BAR_ACTIVATED.value
        elif light_bar_active == 0 and siren_activated == 1:
            self.template_cam['cam']['camParameters']['specialVehicleContainer'][1][
                'lightBarSirenInUse'] = LightBar.SIREN_ACTIVATED.value
        elif light_bar_active == 1 and siren_activated == 1:
            self.template_cam['cam']['camParameters']['specialVehicleContainer'][1][
                'lightBarSirenInUse'] = LightBar.BOTH.value
        else:
            self.template_cam['cam']['camParameters']['specialVehicleContainer'][1][
                'lightBarSirenInUse'] = LightBar.NONE.value

        # self.template_cam['cam']['camParameters']['specialVehicleContainer'][1]['lightBarSirenInUse'] = (b'\xC0', 2)

    def decode_status_light_bar_siren_in_use(self, light_bar_siren_in_use, decode_cam):

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


if __name__ == "__main__":
    obj = CamGenerator()
    obj.start_v2_custom_massaging()
