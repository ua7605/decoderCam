import asn1tools
import json
import os
import time

from DUST.agent_listener_dust import AgentListenerDust
from tools.startup_phase import LightBar


class CamGenerator(object):
    """
    When the decoder is being used as a CAM message generator an object of this class needs to be made.
    The content of the CAM messages that will be sent can be specified in the "cam_template.json" file.
    """
    dir_name = os.path.dirname(__file__)

    def __init__(self, AgentListener, dir_name=dir_name):
        """

        :param AgentListener: the DUST agent.
        :param dir_name: current directory were this python file is located.
        """
        self.cam_asn1 = asn1tools.compile_files('./cam121.asn', 'uper')
        template_cam_json = os.path.join(dir_name, "cam_template.json")  # "cam_template.json")
        f = open(template_cam_json, "r")
        self.template_cam = json.load(f)
        self.agent_listener_dust: AgentListenerDust = AgentListener

    def start_custom_massaging(self):
        """
        To start the sending CUSTOM CAM message from the template.
        """
        # custom_message = self.template_cam
        i = 1
        while True:
            out = self.template_cam
            out['cam']['camParameters']['basicContainer']['referencePosition']['altitude']['altitudeValue'] = i

            out['cam']['camParameters']['highFrequencyContainer'] = (
                'basicVehicleContainerHighFrequency', out['cam']['camParameters']['highFrequencyContainer'][1])
            payload = bytes(self.cam_asn1.encode("CAM", out))
            self.agent_listener_dust.sent_custom_message(payload)
            time.sleep(1)
            i += 1
            print("sent to CAMINO")
            print(out)

    def start_special_vehicle_service_massaging(self, dir_name=dir_name):
        """
        When CAM messages needs to be generated for special vehicles use the "cam_custom_template.json" file to set the
        content you want that being sent.
        :param dir_name: were the python file is located.
        """
        i = 1
        template_cam_json = os.path.join(dir_name, "cam_custom_template.json")  # "cam_template.json")
        f = open(template_cam_json, "r")
        self.template_cam = json.load(f)
        self._service_setup()

        while True:
            custom = self.template_cam
            custom['cam']['camParameters']['basicContainer']['referencePosition']['altitude']['altitudeValue'] = i

            # Just for testing to mimic the effect if multiple awarness message are being received from multiple special
            # vehicles
            # custom['header']['stationID'] = i

            payload = bytes(self.cam_asn1.encode("CAM", custom))
            self.agent_listener_dust.sent_custom_message(payload)
            time.sleep(1)
            i += 1
            print("sent to CAMINO")
            print(custom)

    def _service_setup(self):
        """
        Makes it possible to make a json file otherwise errors would be generated.
        :return: the correct message to make a json object without errors.
        """
        self.template_cam['cam']['camParameters']['highFrequencyContainer'] = \
            (
                'basicVehicleContainerHighFrequency',
                self.template_cam['cam']['camParameters']['highFrequencyContainer'][1]
            )

        self.template_cam['cam']['camParameters']['specialVehicleContainer'] = \
            (
                'safetyCarContainer', self.template_cam['cam']['camParameters']['specialVehicleContainer'][1]
            )

        self._light_bar_siren_in_use(
            message=self.template_cam['cam']['camParameters']['specialVehicleContainer'][1]['lightBarSirenInUse'])

    def _light_bar_siren_in_use(self, message):
        """
        To add the value of the siren or light if they are active.
        :param message: CAM message
        """
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

    def start_special_vehicle_service_massaging_old(self, dir_name=dir_name):
        """
        DEPRECATED you can ignore this.
        """
        i = 1
        template_cam_json = os.path.join(dir_name, "cam_custom_template.json")  # "cam_template.json")
        f = open(template_cam_json, "r")
        self.template_cam = json.load(f)
        while True:
            custom = self.template_cam
            custom['cam']['camParameters']['basicContainer']['referencePosition']['altitude']['altitudeValue'] = i
            custom['cam']['camParameters']['highFrequencyContainer'] = ('basicVehicleContainerHighFrequency',
                                                                        custom['cam']['camParameters'][
                                                                            'highFrequencyContainer'][1])

            custom['cam']['camParameters']['specialVehicleContainer'] = ('safetyCarContainer',
                                                                         custom['cam']['camParameters'][
                                                                             'specialVehicleContainer'][1])

            custom['cam']['camParameters']['specialVehicleContainer'][1]['lightBarSirenInUse'] = (b'\x40', 2)

            payload = bytes(self.cam_asn1.encode("CAM", custom))
            self.agent_listener_dust.sent_custom_message(payload)
            time.sleep(1)
            i += 1
            print("sent to CAMINO")
            print(custom)
