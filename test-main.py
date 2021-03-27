import struct

import asn1tools
import json
import os
import time

from appdirs import unicode
from bitstring import xrange


def bitstring2tublebytelen(s):
    n=len(s)
    a2=[ s[_:_+8] for _ in xrange(0,len(s),8)]
    return bytes(struct.pack("B"*len(a2),*map(lambda x: int(x,2),a2))),n


if __name__ == "__main__":
    cam_asn1 = asn1tools.compile_files('./cam121.asn', 'uper')
    f = open("/Users/vincentcharpentier/PycharmProjects/DecdoderCAM/DUST/CAM_Message_generator/cam_custom_template.json", "r")
    template_cam = json.load(f)
    template_cam['cam']['camParameters']['highFrequencyContainer'] = ('basicVehicleContainerHighFrequency', template_cam['cam']['camParameters']['highFrequencyContainer'][1])
    #template_cam['cam']['camParameters']['lowFrequencyContainer'] = ('basicVehicleContainerLowFrequency', template_cam['cam']['camParameters']['lowFrequencyContainer'][1])

    #print( template_cam['cam']['camParameters']['lowFrequencyContainer'][1]['exteriorLights']['lowBeamHeadlightsOn'])

    #template_cam['cam']['camParameters']['lowFrequencyContainer'][1]['exteriorLights'] = bytes("lowBeamHeadlightsOn",encoding='utf8'), template_cam['cam']['camParameters']['lowFrequencyContainer'][1]['exteriorLights']['lowBeamHeadlightsOn']
    #template_cam['cam']['camParameters']['lowFrequencyContainer'][1]['exteriorLights'] = bytes("highBeamHeadlightsOn",encoding='utf8'), template_cam['cam']['camParameters']['lowFrequencyContainer'][1]['exteriorLights']['highBeamHeadlightsOn']
    # template_cam['cam']['camParameters']['lowFrequencyContainer'][1]['exteriorLights'] = bytes("leftTurnSignalOn",encoding='utf8'), template_cam['cam']['camParameters']['lowFrequencyContainer'][1]['exteriorLights']['leftTurnSignalOn']
    # template_cam['cam']['camParameters']['lowFrequencyContainer'][1]['exteriorLights'] = bytes("rightTurnSignalOn",encoding='utf8'), template_cam['cam']['camParameters']['lowFrequencyContainer'][1]['exteriorLights']['rightTurnSignalOn']
    # template_cam['cam']['camParameters']['lowFrequencyContainer'][1]['exteriorLights'] = bytes("daytimeRunningLightsOn",encoding='utf8'), template_cam['cam']['camParameters']['lowFrequencyContainer'][1]['exteriorLights']['daytimeRunningLightsOn']
    # template_cam['cam']['camParameters']['lowFrequencyContainer'][1]['exteriorLights'] = bytes("reverseLightOn", encoding='utf8'), template_cam['cam']['camParameters']['lowFrequencyContainer'][1]['exteriorLights']['reverseLightOn']
    # template_cam['cam']['camParameters']['lowFrequencyContainer'][1]['exteriorLights'] = bytes("fogLightOn",encoding='utf8'), template_cam['cam']['camParameters']['lowFrequencyContainer'][1]['exteriorLights']['fogLightOn']
    # template_cam['cam']['camParameters']['lowFrequencyContainer'][1]['exteriorLights'] = bytes("parkingLightsOn", encoding='utf8'), template_cam['cam']['camParameters']['lowFrequencyContainer'][1]['exteriorLights']['parkingLightsOn']
    template_cam['cam']['camParameters']['specialVehicleContainer'] = ('safetyCarContainer', template_cam['cam']['camParameters']['specialVehicleContainer'][1])
    template_cam['cam']['camParameters']['specialVehicleContainer'][1]['lightBarSirenInUse'] = (bytes(1),1)
    payload = cam_asn1.encode("CAM", template_cam)
    #encoded_cam = bytearray(payload)
    #print(payload)
    decoded_cam = cam_asn1.decode('CAM', payload)
    #json_object_cam_message = json.dumps(decoded_cam)

    print(decoded_cam)
