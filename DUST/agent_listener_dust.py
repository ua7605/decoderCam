import time
import threading
import gpsd

from DUST.dust_Controller import DUSTController
from DUST.dust_messages_decoder.dust_cam_decoder import DUSTCamDecoder


# Tested on Testbed and it works!
# With this everything DUST related will started so just make a object of this class and interact with the agent.
class AgentListenerDust(object):
    special_vehicle: int = 10

    def __init__(self, configuration_toml):
        self.dust_comm: DUSTController = DUSTController.load_from_config(configuration=configuration_toml)
        output_file = configuration_toml["output_files"]
        self.dust_cam_decoder: DUSTCamDecoder = DUSTCamDecoder(
            file_path_to_output_json_file=output_file["json_output_file_path"])
        self.json_cam_message = None

    def _register_listener(self):
        self.dust_comm.register_listener("ivi_topic_out", self.incoming_DUST_message)
        print("listening on topic: ", "ivi_topic_out")

    def incoming_DUST_message(self, data_byte):
        print("Message received!")
        self.json_cam_message, _ = self.dust_cam_decoder.decode_cam_message(message=data_byte)
        print("The decoded message is: ", self.json_cam_message)

        if self.json_cam_message is not None:
            self._sent_cam_data_to_server(json_cam_data=self.json_cam_message)
        else:
            print(
                "There is a problem with it decoding the received message")  # TODO in the future change it to a proper logger

    def _sent_cam_data_to_server(self, json_cam_data):
        print("data will be sent to the server!")
        # declare a bytes-like payload object
        payload = json_cam_data.encode("ascii")
        self.dust_comm.publish(topic="CAM-topic-decoder",
                               message=payload)  # Todo Make a DUST channel topic: "CAM-topic-decoder" such that the Server can receive it is done

    def _sent_gps_data_to_server(self, gps_data: str):
        payload = gps_data.encode("ascii")
        self.dust_comm.publish(topic="GPS",
                               message=payload)
        #print("GPS data has been sent over topic: GPS with: " + gps_data)




    def _sent_special_vehicle_data_to_server(self, json_cam_data):
        print("data of !!!SPECIAL vehicle!!! will be sent to the server!")
        # declare a bytes-like payload object
        payload = json_cam_data.encode("ascii")
        self.dust_comm.publish(topic="special-vehicle-topic-decoder",
                               message=payload)

    def _sent_custom_message_to_camino(self, payload):
        self.dust_comm.publish(topic="cam_topic_in", message=payload)

    def _keep_dust_agent_live(self):
        with True:
            time.sleep(1)

    def start(self):
        print("Starting to listen")
        self._register_listener()

    def start_c(self):
        print("Starting to listen")
        self._register_listener_custom_message()

    def sent_custom_message(self, payload):
        self._sent_custom_message_to_camino(payload)

    def _register_listener_custom_message(self):
        self.dust_comm.register_listener("ivi_topic_out", self.incoming_DUST_custom_message)
        print("listening on topic: ", "ivi_topic_out")

    def incoming_DUST_custom_message(self, data_byte):
        print("Message received!")
        station_type: int
        self.json_cam_message, station_type = self.dust_cam_decoder.decode_cam_message(message=data_byte, custom=True)

        if self.json_cam_message is not None:
            if station_type.__eq__(self.special_vehicle):
                self._sent_special_vehicle_data_to_server(json_cam_data=self.json_cam_message)
            # TODO: for every station_type make a DUST channel so the server can listen on every DUST channel topic
            #  and start his monitory
            else:
                print("Not send special vehicle data")
                self._sent_cam_data_to_server(json_cam_data=self.json_cam_message)
        else:
            print(
                "There is a problem with it decoding the received message")  # TODO in the future change it to a proper logger

