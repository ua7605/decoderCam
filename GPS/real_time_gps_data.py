import gpsd
import time

from DUST.agent_listener_dust import AgentListenerDust


class GPS(object):
    @staticmethod
    def load_from_config(configuration, agent_listener_dust: AgentListenerDust):
        gps_config = configuration["GPS"]
        gps_host_ip: str = gps_config["GPS_host_ip"]
        gps_port: int = gps_config["GPS_port"]

        return GPS(host_ip=gps_host_ip,
                   port=gps_port,
                   dust_communication=agent_listener_dust)

    def __init__(self, host_ip: str, port: int, dust_communication: AgentListenerDust):
        print("Connecting to GPS....")
        gpsd.connect(host=host_ip, port=port)
        print("Connected to GPS ! ", host_ip, " port: ", port)
        self.dust_agent: AgentListenerDust = dust_communication

    def track(self):
        while True:
            pack = gpsd.get_current()
            payload: str = str(pack.lat)+","+str(pack.lon)
            print('payload = ', payload)
            self.dust_agent._sent_gps_data_to_server(payload)
            time.sleep(1)