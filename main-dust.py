import sys

from DUST.agent_listener_dust import AgentListenerDust

if __name__ == "__main__":
    configuration_toml_file = sys.argv[0]
    agent_dust = AgentListenerDust(configuration_toml=configuration_toml_file)
    agent_dust.start()
