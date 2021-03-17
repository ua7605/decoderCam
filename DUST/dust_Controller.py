import time


# Make sure you comment this out when you are in a production
# from pydust import core


class DustController(object):
    @staticmethod
    def from_config(configuration):
        dust_config = configuration["DUST"]
        name = dust_config["application_name"]
        config_file = dust_config["config_file"]
        module_dir = dust_config["module_dir"]
        return DustController(name=name,
                              config_file=config_file,
                              dust_module_dir=module_dir)

    def __init__(self, name, config_file="configuration.json", dust_module_dir="./modules"):
        # initialises the core with the given block name and the directory where the modules are located (default
        # "./modules")
        self.dust = core.Core(name, dust_module_dir)

        # start a background thread responsible for tasks that should always be running in the same thread
        self.dust.cycle_forever()

        # load the core, this includes reading the libraries in the modules directory to check addons and transports
        # are available
        self.dust.setup()

        # set the path to the configuration file
        self.dust.set_configuration_file(config_file)

        # connects all channels
        self.dust.connect()

        # Let DUST launch properly
        time.sleep(1)

    def shutdown(self):
        self.dust.disconnect()
        self.dust.cycle_stop()

    def publish(self, topic, message):
        self.dust.publish(topic, message)
