from DUST.dust_Controller import DUSTController


class AgentListenerDust(object):
    def __init__(self, configuration_file_toml):
        self.dust_comm: DUSTController = DUSTController.load_from_config(configuration=configuration_file_toml)

    def _register_listener(self):
        self.dust_comm.register_listener("ivi_topic_out", self.incoming_DUST_message) # Todo Make in the DUST configuration.json a topic with name cam-data-received-to-cam-server

    def incoming_DUST_message(self, data_hex):
        print("Got message on topic")
