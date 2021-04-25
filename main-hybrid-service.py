import sys
import time
import toml
# import logging

from DUST.agent_listener_dust import AgentListenerDust
from DUST.CAM_Message_generator.cam_generator import CamGenerator
from tools.startup_phase import Startup
from tools.startup_phase import Keyword

if __name__ == "__main__":

    # logging.basicConfig(format='%(asctime)s %(message)s')
    configuration_toml_file = "config.toml"
    current_phase = Startup.CONFIG_FILE_CHECK.value

    if Startup.CONFIG_FILE_CHECK.value.__eq__(current_phase):

        try:
            with open(configuration_toml_file) as file:
                config_file = toml.load(f=file)
                current_phase = Startup.CONFIG_FILE_READING.value
                # logging.warning("Configuration file is successfully being read")
        except:
            # print("File doesn't exists: "+configuration_toml_file)
            sys.exit()

    if Startup.CONFIG_FILE_READING.value.__eq__(current_phase):

        dust_config = config_file["DUST"]
        name = dust_config["application_name"]

        usage_config = config_file["usage"]
        decoder: str = usage_config["cam_decoder"]
        cam_generator: str = usage_config["cam_generator"]
        is_service_sp_vehicle: str = usage_config["special_vehicle_service"]
        true = Keyword.true.name
        false = Keyword.false.name

        if decoder.__eq__(true) and cam_generator.__eq__(false) and is_service_sp_vehicle.__eq__(false):
            # logging.warning("The decoder will be starting up")

            agent_dust = AgentListenerDust(configuration_toml=config_file)
            agent_dust.start()
            while True:
                time.sleep(1)

        elif decoder.__eq__(false) and cam_generator.__eq__(true):
            # logging.warning("The message generator service will be started")
            agent_dust = AgentListenerDust(configuration_toml=config_file)
            message_generator = CamGenerator(AgentListener=agent_dust)
            if is_service_sp_vehicle.__eq__(Keyword.true.name):
                message_generator.start_special_vehicle_service_massaging()
            else:
                message_generator.start_custom_massaging()
            message_generator.start_custom_massaging()

        elif decoder.__eq__(true) and cam_generator.__eq__(false) and is_service_sp_vehicle.__eq__(true):
            agent_dust = AgentListenerDust(configuration_toml=config_file)
            # TODO: Make this more generic so solve the problem of the bit string field in the ASN file.
            print("CUSTOM SERVICE RUNNING")
            agent_dust.start_c()
            while True:
                time.sleep(1)

        elif decoder.__eq__(true) and cam_generator.__eq__(true):
            # logging.warning("The message generator service and CAM decoding service will be started")
            agent_dust = AgentListenerDust(configuration_toml=config_file)
            agent_dust.start()
            message_generator = CamGenerator(AgentListener=agent_dust)
            if is_service_sp_vehicle.__eq__(Keyword.true.name):
                message_generator.start_special_vehicle_service_massaging_old()
            else:
                message_generator.start_custom_massaging()
            message_generator.start_custom_massaging()
        else:
            # logging.warning("Application stopped")
            sys.exit()
