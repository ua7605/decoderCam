import sys

import toml

from DUST.agent_listener_dust import AgentListenerDust

if __name__ == "__main__":
    configuration_toml_file = sys.argv[0]

    with open(configuration_toml_file) as file:
        config_file = toml.load(f=file)
        is_true = True
    if is_true:
        agent_dust = AgentListenerDust(configuration_toml=configuration_toml_file)
        agent_dust.start()
