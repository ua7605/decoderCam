import time

from DUST.dust_Controller import DUSTController
from DUST.dust_messages_decoder.dust_cam_decoder import DUSTCamDecoder


class AgentListenerDust(object):
    """
        A DUST agent that will manage everything DUST related.
    """
    special_vehicle: int = 10

    def __init__(self, configuration_toml):
        """
        :param configuration_toml: An absolute path to the configuration Toml file.
        """
        self.dust_comm: DUSTController = DUSTController.load_from_config(configuration=configuration_toml)
        output_file = configuration_toml["output_files"]
        self.dust_cam_decoder: DUSTCamDecoder = DUSTCamDecoder(
            file_path_to_output_json_file=output_file["json_output_file_path"])
        self.json_cam_message = None

    def _register_listener(self):
        """
        The DUST agent will listen on the DUST topic 'ivi_topic_out' when messages are beining received on that topic
        it will exicuted the function 'incoming_DUST_message'
        """
        self.dust_comm.register_listener("ivi_topic_out", self.incoming_DUST_message)
        print("listening on topic: ", "ivi_topic_out")

    def incoming_DUST_message(self, data_byte):
        """
        The when a DUST message is being received from CAMINO the decoder will start decoding it.
        """
        print("Message received!")
        self.json_cam_message, _ = self.dust_cam_decoder.decode_cam_message(message=data_byte)
        print("The decoded message is: ", self.json_cam_message)

        if self.json_cam_message is not None:
            self._sent_cam_data_to_server(json_cam_data=self.json_cam_message)
        else:
            print(
                "There is a problem with it decoding the received message")

    def _sent_cam_data_to_server(self, json_cam_data):
        """
        To sent specific decode data to the webserver. Such that CAMAF can monitor it.
        :param json_cam_data: the json message that needs to be sent to the CAM server.
        """
        print("data will be sent to the server!")
        # declare a bytes-like payload object
        payload = json_cam_data.encode("ascii")
        self.dust_comm.publish(topic="CAM-topic-decoder",
                               message=payload)

    def _sent_gps_data_to_server(self, gps_data: str):
        """
        To sent the gps data of the vehicle that is receiving the CAM messages to the CAM server.
        :param gps_data: the gps data that needs to be sent to the cam server.
        """
        payload = gps_data.encode("ascii")
        self.dust_comm.publish(topic="GPS",
                               message=payload)

    def _sent_special_vehicle_data_to_server(self, json_cam_data):
        """
        To sent specific decode data of special vehicles to the webserver. Such that CAMAF can monitor it.
        :param json_cam_data: the json message that needs to be sent to the CAM server.
        """
        print("data of !!!SPECIAL vehicle!!! will be sent to the server!")
        # declare a bytes-like payload object
        payload = json_cam_data.encode("ascii")
        self.dust_comm.publish(topic="special-vehicle-topic-decoder",
                               message=payload)

    def _sent_custom_message_to_camino(self, payload):
        self.dust_comm.publish(topic="cam_topic_in", message=payload)

    def start(self):
        """
        To start the DUST agent.
        """
        print("Starting to listen")
        self._register_listener()

    def start_c(self):
        """
        To start the DUST agent when the special vehicle services needs to run.
        """
        print("Starting to listen")
        self._register_listener_custom_message()

    def sent_custom_message(self, payload):
        """
        When the decoder is being used to generate custom CAM messages. It will sent it over the specific DUST
        channel.
        """
        self._sent_custom_message_to_camino(payload)

    def _register_listener_custom_message(self):
        """
        When the decoder is being used for the special vehicle services it needs to listen on the channel topics.
        """
        self.dust_comm.register_listener("ivi_topic_out", self.incoming_DUST_custom_message)
        print("listening on topic: ", "ivi_topic_out")

    def incoming_DUST_custom_message(self, data_byte):
        """
        When the decoder is being used for the special vehicle services it will decode the incoming data and will
        only sent the relevant parts of the CAM message to CAMAF. Such that CAMAF can generate a monitor and keep the
        monitor up to date.
        """
        print("Message received!")
        station_type: int
        self.json_cam_message, station_type = self.dust_cam_decoder.decode_cam_message(message=data_byte, custom=True)

        if self.json_cam_message is not None:
            if station_type.__eq__(self.special_vehicle):
                self._sent_special_vehicle_data_to_server(json_cam_data=self.json_cam_message)
            else:
                print("Not send special vehicle data")
                self._sent_cam_data_to_server(json_cam_data=self.json_cam_message)
        else:
            print(
                "There is a problem with it decoding the received message")

    def _keep_dust_agent_live(self):
        """
        Deprecated not more in use.

        """
        with True:
            time.sleep(1)
