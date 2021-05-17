import time
import toml

from DUST.agent_listener_dust import AgentListenerDust

if __name__ == "__main__":
    """
    this main is meant to be used if you want to read out the CAMINO log files for CAM then you need to start this main.
    """

    configuration_toml_file = "../config.toml"
    with open(configuration_toml_file) as file:
        config_file = toml.load(f=file)
        is_true = True
        dust_config = config_file["DUST"]
        name = dust_config["application_name"]
        print("The NAME IS: ", name)
        print("Toml file is successful being read")
    if is_true:
        agent_dust = AgentListenerDust(configuration_toml=config_file)
        agent_dust.start()
    print("Agent is started correct! and is listening and can sent")
    while True:
        time.sleep(1)

