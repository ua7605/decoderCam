import sys
import time

import toml

from DUST.agent_listener_dust import AgentListenerDust
from DUST.CAM_Message_generator.cam_generator import CamGenerator

if __name__ == "__main__":

    configuration_toml_file = "../config.toml"
    with open(configuration_toml_file) as file:
        config_file = toml.load(f=file)
        is_true = True
        dust_config = config_file["DUST"]
        name = dust_config["application_name"]
        print("The NAME IS: ", name)
        print("Toml file is successful being read")

        usage_config = config_file["usage"]
        decoder = usage_config["cam_decoder"]
        cam_generator = usage_config["cam_generator"]

    if decoder == "true":
        agent_dust = AgentListenerDust(configuration_toml=config_file)
        agent_dust.start()
    elif cam_generator == "true":
        agent_dust = AgentListenerDust(configuration_toml=config_file)
        message_generator = CamGenerator(AgentListener=agent_dust)
        message_generator.start_custom_massaging()
    print("Agent is started correct! and is listening and can sent")
    while True:
        time.sleep(1)

