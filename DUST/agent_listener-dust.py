from DUST.dust_Controller import DUSTController
from DUST.dust_messages_decoder.dust_cam_decoder import DUSTCamDecoder


# With this everything DUST related will started so just make a object of this class and interact with the agent.
class AgentListenerDust(object):
    def __init__(self, configuration_toml):
        self.dust_comm: DUSTController = DUSTController.load_from_config(configuration=configuration_toml)
        output_file = configuration_toml["output_files"]
        self.dust_cam_decoder: DUSTCamDecoder = DUSTCamDecoder(file_path_to_output_json_file=output_file["json_output_file_path"])
        self.json_cam_message = None

    def _register_listener(self):
        self.dust_comm.register_listener("ivi_topic_out", self.incoming_DUST_message)

    def incoming_DUST_message(self, data_hex):
        print("Got message on topic")
        self.json_cam_message = self.dust_cam_decoder.decode_cam_message(message=data_hex)
        if self.json_cam_message is not None:
            self._sent_cam_data_to_server(json_cam_data=self.json_cam_message)
        else:
            print("There is a problem with it decoding the received message") # TODO in the future change it to a proper logger

    def _sent_cam_data_to_server(self, json_cam_data):
        self.dust_comm.publish(topic="CAM-from-decoder", message=json_cam_data)# Todo Make a DUST channel topic: "CAM-from-decoder" such that the Server can receive it

