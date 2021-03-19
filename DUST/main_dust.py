import sys

import toml

from DUST.agent_listener_dust import AgentListenerDust
if __name__ == "__main__":
    configuration_toml_file = sys.argv[0]
    with open(configuration_toml_file) as file:
        config_file = toml.load(file)

    agent_dust = AgentListenerDust(configuration_toml=config_file)
    agent_dust.start()


