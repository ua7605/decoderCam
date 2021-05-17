import time

from pydust import core


class DUSTController(object):
    """
        The DUSTController class to make an object of the DUST core to make it possible to use DUST communication.
    """

    @staticmethod
    def load_from_config(configuration):
        """
        To make a DUST object directly via a configuration file.
        :param configuration: An absolute path to the configuration file in this case a Toml file.

        """
        dust_config = configuration["DUST"]

        name = dust_config["application_name"]
        config_file = dust_config["config_file"]
        module_dir = dust_config["module_dir"]
        return DUSTController(name=name,
                              config_file=config_file,
                              dust_module_dir=module_dir)

    def __init__(self, name, config_file="configuration.json", dust_module_dir="./modules"):
        """
        :param name: The name of the core, needs to match the block name in the config file
        :param config_file: An absolute path to the configuration file
        :param dust_module_dir: An absolute path to the module folder

        """
        # initialises the core with the given block name and the directory where the modules are located (default
        # "./modules")
        print("config_file: ", config_file)
        print("dust_module_dir: ", dust_module_dir)
        self.dust_core = core.Core(name, dust_module_dir)

        # start a background thread responsible for tasks that should always be running in the same thread
        self.dust_core.cycle_forever()

        # load the core, this includes reading the libraries in the modules directory to check addons and transports
        # are available
        self.dust_core.setup()

        # set the path to the configuration file
        self.dust_core.set_configuration_file(config_file)

        # connects all channels
        self.dust_core.connect()

        # Let DUST launch properly
        time.sleep(1)
        print("DUST is launched properly")

    def shutdown(self):
        """
        Shutdowns the DUST core.
        """
        self.dust_core.disconnect()
        self.dust_core.cycle_stop()

    def publish(self, topic, message):
        """
        Publish data over a specific topic/channel over DUST.

        :param topic: The name of the channel, as defined in the config file.
        :param message: The message to be sent
        """
        self.dust_core.publish(topic, message)

    def register_listener(self, topic, func):
        """
        Register a callback when a message has been received over a specific DUST channel. Every time a message on that
        topic will be received the function (func) will be executed.

        :param topic: The name of the channel, as defined in the config file.
        :param func: function that needs to be executed when a DUST message has been received
        """
        self.dust_core.register_listener(topic, func)
