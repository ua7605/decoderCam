import sys
import time

import toml

from DUST.agent_listener_dust import AgentListenerDust
from DUST.CAM_Message_generator.cam_generator import CamGenerator
from tools.startup_phase import Startup
from tools.startup_phase import Keyword

if __name__ == "__main__":

    configuration_toml_file = "config.toml"
    current_phase = Startup.CONFIG_FILE_CHECK.value

    print(current_phase)

    if Startup.CONFIG_FILE_CHECK.value.__eq__(current_phase):
        print("Works")
        try:
            with open(configuration_toml_file) as file:
                config_file = toml.load(f=file)
                current_phase = Startup.CONFIG_FILE_READING.value
        except:
            print("File doesn't exists: "+configuration_toml_file)
            sys.exit()

    if Startup.CONFIG_FILE_READING.value.__eq__(current_phase):

        dust_config = config_file["DUST"]
        name = dust_config["application_name"]

        usage_config = config_file["usage"]
        decoder: str = usage_config["cam_decoder"]
        cam_generator: str = usage_config["cam_generator"]

        if decoder.__eq__(Keyword.true.name) and cam_generator.__eq__(Keyword.false.name):
            agent_dust = AgentListenerDust(configuration_toml=config_file)
            agent_dust.start()
            while True:
                time.sleep(1)

        elif decoder.__eq__(Keyword.false.name) and cam_generator.__eq__(Keyword.true.name):
            agent_dust = AgentListenerDust(configuration_toml=config_file)
            message_generator = CamGenerator(AgentListener=agent_dust)
            message_generator.start_custom_massaging()

        elif decoder.__eq__(Keyword.true.name) and cam_generator.__eq__(Keyword.true.name):
            agent_dust = AgentListenerDust(configuration_toml=config_file)
            agent_dust.start()
            message_generator = CamGenerator(AgentListener=agent_dust)
            message_generator.start_custom_massaging()
        else:
            print("Decoder shutdown")
            sys.exit()
    #
    # with open(configuration_toml_file) as file:
    #     config_file = toml.load(f=file)
    #     is_true = True
    #     dust_config = config_file["DUST"]
    #     name = dust_config["application_name"]
    #     print("The NAME IS: ", name)
    #     print("Toml file is successful being read")
    #
    #     usage_config = config_file["usage"]
    #     decoder = usage_config["cam_decoder"]
    #     cam_generator = usage_config["cam_generator"]
    #
    # if decoder == "true":
    #     agent_dust = AgentListenerDust(configuration_toml=config_file)
    #     agent_dust.start()
    # elif cam_generator == "true":
    #     agent_dust = AgentListenerDust(configuration_toml=config_file)
    #     message_generator = CamGenerator(AgentListener=agent_dust)
    #     message_generator.start_custom_massaging()
    # print("Agent is started correct! and is listening and can sent")
    # while True:
    #     time.sleep(1)
    #
