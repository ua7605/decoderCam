import asn1tools
import json
import os
import time

from DUST.agent_listener_dust import AgentListenerDust


class CamGenerator(object):
    dir_name = os.path.dirname(__file__)

    def __init__(self, AgentListener, dir_name=dir_name):
        self.cam_asn1 = asn1tools.compile_files('./cam121.asn', 'uper')
        template_cam_json = os.path.join(dir_name, "cam_template.json")#"cam_template.json")
        f = open(template_cam_json, "r")
        self.template_cam = json.load(f)
        self.agent_listener_dust: AgentListenerDust = AgentListener

    def start_custom_massaging(self):
        #custom_message = self.template_cam
        i = 1
        while True:
            out = self.template_cam
            out['cam']['camParameters']['basicContainer']['referencePosition']['altitude']['altitudeValue'] = i
            #out['cam']['referencePosition']['altitude']['altitudeValue'] = i
            out['cam']['camParameters']['highFrequencyContainer'] = ('basicVehicleContainerHighFrequency', out['cam']['camParameters']['highFrequencyContainer'][0]['basicVehicleContainerHighFrequency'])
            payload = bytes(self.cam_asn1.encode("CAM", out))
            self.agent_listener_dust.sent_custom_message(payload)
            time.sleep(1)
            i += 1
            print("sent to CAMINO")
